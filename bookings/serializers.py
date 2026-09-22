from rest_framework import serializers
from .models import Booking
from inventory.serializers import EquipmentSerializer
from users.serializers import CustomUserSerializer

class BookingSerializer(serializers.ModelSerializer):
    user_detail = CustomUserSerializer(source='user', read_only=True)
    equipment_detail = EquipmentSerializer(source='equipment', read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'user_detail', 'equipment', 'equipment_detail', 'quantity', 'start_date', 'end_date', 'status', 'created_at']
