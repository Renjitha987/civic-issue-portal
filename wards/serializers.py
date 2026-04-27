from rest_framework import serializers
from .models import Ward, Panchayat

class PanchayatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Panchayat
        fields = '__all__'

class WardSerializer(serializers.ModelSerializer):
    panchayat_name = serializers.CharField(source='panchayat.name', read_only=True, allow_null=True)

    class Meta:
        model = Ward
        fields = ['id', 'ward_name', 'panchayat', 'panchayat_name', 'created_at']

