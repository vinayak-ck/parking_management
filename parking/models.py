from django.db import models
from django.utils import timezone
from datetime import timedelta

class Owner(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name

class Vehicle(models.Model):
    VEHICLE_TYPES = [('car', 'Car'), ('bike', 'Bike'), ('other', 'Other')]
    vehicle_number = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPES)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    def __str__(self): return self.vehicle_number

class ParkingPass(models.Model):
    PASS_TYPES = [
        ('daily', 'Daily'), ('weekly', 'Weekly'), 
        ('monthly', 'Monthly'), ('yearly', 'Yearly')
    ]
    # New Payment Choices
    PAYMENT_METHODS = [('cash', 'Cash'), ('card', 'Card'), ('upi', 'UPI')]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    pass_type = models.CharField(max_length=10, choices=PASS_TYPES)
    issue_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # New Field
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='cash')

    def save(self, *args, **kwargs):
        if not self.expiry_date:
            now = timezone.now()
            days = {'daily': 1, 'weekly': 7, 'monthly': 30, 'yearly': 365}
            self.expiry_date = now + timedelta(days=days.get(self.pass_type, 1))
        
        if self.price == 0.00:
            rates = {'daily': 10.00, 'weekly': 50.00, 'monthly': 200.00, 'yearly': 2000.00}
            self.price = rates.get(self.pass_type, 0.00)
            
        super().save(*args, **kwargs)

class Transaction(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(null=True, blank=True)
    fees_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def calculate_fee(self):
        if not self.exit_time: return 0.00
        # Check if active pass exists
        if ParkingPass.objects.filter(vehicle=self.vehicle, expiry_date__gt=timezone.now()).exists():
            return 0.00
        duration = (self.exit_time - self.entry_time).total_seconds() / 3600
        rate = 5.00 if self.vehicle.vehicle_type in ['car', 'other'] else 2.00
        return round(max(rate, duration * rate), 2)