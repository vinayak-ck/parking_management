from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.db.models import Sum
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Vehicle, Owner, ParkingPass, Transaction
from .serializers import TransactionSerializer, PassSerializer
from datetime import timedelta

# --- 1. HTML View ---
def dashboard_view(request):
    # This matches the folder structure: templates/parking/dashboard.html
    return render(request, 'parking/dashboard.html')

# --- 2. API Endpoints (Must match names in urls.py) ---

@api_view(['POST'])
def api_post_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return Response({'status': 'success', 'message': 'Login successful!'})
    return Response({'status': 'error', 'message': 'Invalid credentials.'})

@api_view(['GET'])
def api_get_dashboard_stats(request):
    now = timezone.now()
    active_passes = ParkingPass.objects.filter(expiry_date__gt=now).count()
    
    today_start = now.replace(hour=0, minute=0, second=0)
    today_txs = Transaction.objects.filter(entry_time__gte=today_start)
    
    vehicles_today = today_txs.values('vehicle').distinct().count()
    earnings = today_txs.aggregate(Sum('fees_paid'))['fees_paid__sum'] or 0
    occupied = Transaction.objects.filter(exit_time__isnull=True).count()
    
    return Response({
        'active_passes_count': active_passes,
        'vehicles_today': vehicles_today,
        'earnings_today': earnings,
        'slots_filled': f"{occupied} / 100"
    })

@api_view(['GET'])
def api_get_recent_transactions(request):
    txs = Transaction.objects.all().order_by('-entry_time')[:5]
    return Response(TransactionSerializer(txs, many=True).data)

@api_view(['GET'])
def api_get_all_transactions(request):
    txs = Transaction.objects.all().order_by('-entry_time')
    return Response(TransactionSerializer(txs, many=True).data)

@api_view(['GET'])
def api_get_expiry_notifications(request):
    now = timezone.now()
    seven_days = now + timedelta(days=7)
    expiring = ParkingPass.objects.filter(expiry_date__gt=now, expiry_date__lte=seven_days)
    
    data = []
    for p in expiring:
        days_left = (p.expiry_date - now).days
        data.append({
            'pass': PassSerializer(p).data,
            'owner_name': p.vehicle.owner.name,
            'vehicle_number': p.vehicle.vehicle_number,
            'days_left': days_left
        })
    return Response(data)

@api_view(['GET'])
def api_get_slots_data(request):
    parked = Transaction.objects.filter(exit_time__isnull=True)
    cars = parked.filter(vehicle__vehicle_type__in=['car', 'other']).count()
    bikes = parked.filter(vehicle__vehicle_type='bike').count()
    return Response({
        'cars_occupied': cars, 
        'bikes_occupied': bikes,
        'total_car_slots': 50,
        'total_bike_slots': 50
    })

@api_view(['POST'])
def api_post_create_pass(request):
    data = request.data
    owner, _ = Owner.objects.get_or_create(name=data.get('owner_name'))
    vehicle, _ = Vehicle.objects.get_or_create(
        vehicle_number=data.get('vehicle_number'),
        defaults={'vehicle_type': data.get('vehicle_type'), 'owner': owner}
    )
    
    if ParkingPass.objects.filter(vehicle=vehicle, expiry_date__gt=timezone.now()).exists():
        return Response({'status': 'error', 'message': 'Active pass already exists.'})
    
    # Pass the payment_method from request to the database
    ParkingPass.objects.create(
        vehicle=vehicle, 
        pass_type=data.get('pass_type'),
        payment_method=data.get('payment_method', 'cash') # Default to cash if missing
    )
    return Response({'status': 'success', 'message': 'Pass created successfully!'})

@api_view(['POST'])
def api_post_vehicle_entry(request):
    v_num = request.data.get('vehicle_number')
    v_type = request.data.get('vehicle_type', 'car')
    
    owner, _ = Owner.objects.get_or_create(name="Guest")
    vehicle, _ = Vehicle.objects.get_or_create(
        vehicle_number=v_num,
        defaults={'vehicle_type': v_type, 'owner': owner}
    )
    
    if Transaction.objects.filter(vehicle=vehicle, exit_time__isnull=True).exists():
        return Response({'status': 'error', 'message': 'Vehicle already inside.'})
    
    Transaction.objects.create(vehicle=vehicle)
    return Response({'status': 'success', 'message': f'Vehicle {v_num} entered.'})

@api_view(['POST'])
def api_post_vehicle_exit(request):
    v_num = request.data.get('vehicle_number')
    try:
        tx = Transaction.objects.filter(vehicle__vehicle_number=v_num, exit_time__isnull=True).latest('entry_time')
        tx.exit_time = timezone.now()
        
        # Fee Calculation
        active_pass = ParkingPass.objects.filter(vehicle=tx.vehicle, expiry_date__gt=timezone.now()).exists()
        fee = 0.00
        
        if not active_pass:
            duration_hours = (tx.exit_time - tx.entry_time).total_seconds() / 3600
            rate = 5.00 if tx.vehicle.vehicle_type in ['car', 'other'] else 2.00
            fee = round(max(rate, duration_hours * rate), 2)
            
        tx.fees_paid = fee
        tx.save()
        # CHANGED $ TO ₹ BELOW
        return Response({'status': 'success', 'message': f'Exited. Fee: ₹{fee}'})
    except Transaction.DoesNotExist:
        return Response({'status': 'error', 'message': 'No active entry found.'})

@api_view(['GET'])
def api_get_all_passes(request):
    passes = ParkingPass.objects.all().order_by('-issue_date')
    return Response(PassSerializer(passes, many=True).data)