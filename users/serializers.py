from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CitizenProfile, WardMemberProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'phone_number', 'role', 'ward', 'is_blocked', 'date_joined']
        read_only_fields = ['id', 'role', 'date_joined']

class CitizenProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = CitizenProfile
        fields = '__all__'

class WardMemberProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = WardMemberProfile
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    aadhaar_id = serializers.CharField(required=False, min_length=12, max_length=12)

    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'phone_number', 'password', 'role', 'ward', 'aadhaar_id', 'address']

    def validate_password(self, value):
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError('Password must contain at least one number.')
        if not any(char in '!@#$%^&*()-_+={}[]|\\:;"\'<>,.?/' for char in value):
            raise serializers.ValidationError('Password must contain at least one special character.')
        return value

    def create(self, validated_data):
        aadhaar_id = validated_data.pop('aadhaar_id', None)
        role = validated_data.get('role', 'CITIZEN')

        if role == 'CITIZEN':
            if not aadhaar_id:
                raise serializers.ValidationError({'aadhaar_id': 'Aadhaar ID is required for citizens.'})
            if not validated_data.get('ward'):
                raise serializers.ValidationError({'ward': 'Ward is required for citizens.'})

        user = User.objects.create_user(**validated_data)
        
        if role == 'CITIZEN':
            CitizenProfile.objects.create(user=user, aadhaar_id=aadhaar_id, ward=user.ward)
        elif role == 'WARD_MEMBER':
            if user.ward:
                WardMemberProfile.objects.create(user=user, ward=user.ward)
            else:
                user.delete()
                raise serializers.ValidationError({'ward': 'Ward is required for Ward Members.'})

        return user
