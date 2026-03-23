from rest_framework import serializers
from .models import Vehicle, Owner, ParkingPass, Transaction

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ['id', 'name']

class VehicleSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)
    class Meta:
        model = Vehicle
        fields = ['id', 'vehicle_number', 'vehicle_type', 'owner']

class PassSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)
    class Meta:
        model = ParkingPass
        fields = ['id', 'vehicle', 'pass_type', 'issue_date', 'expiry_date', 'price', 'payment_method']

class TransactionSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)
    class Meta:
        model = Transaction
        fields = ['id', 'vehicle', 'entry_time', 'exit_time', 'fees_paid']