# serializers.py
from rest_framework import serializers
from .models import Calendar_Shift,UserProfile

class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar_Shift
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    shifts = ShiftSerializer(many=True, read_only=True)
    class Meta:
        model = UserProfile
        fields = ['id', 'user_name', 'department', 'shifts']