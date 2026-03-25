from rest_framework import serializers
from .models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    head_name = serializers.CharField(source='head.username', read_only=True)

    class Meta:
        model = Department
        fields = '__all__'
