from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('WARD_MEMBER', 'Ward Member'),
        ('CITIZEN', 'Citizen'),
        ('DEPARTMENT_HEAD', 'Department Head'),
    )

    username = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=10, 
        unique=True, 
        validators=[RegexValidator(r'^\d{10}$', 'Phone number must be exactly 10 digits.')]
    )
    email = models.EmailField(unique=True, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CITIZEN')
    ward = models.ForeignKey('wards.Ward', on_delete=models.SET_NULL, null=True, blank=True, related_name='ward_users')
    panchayat = models.ForeignKey('wards.Panchayat', on_delete=models.SET_NULL, null=True, blank=True, related_name='panchayat_users')
    is_blocked = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.username} - {self.role}"

class CitizenProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='citizen_profile')
    aadhaar_id = models.CharField(
        max_length=12, 
        unique=True, 
        validators=[RegexValidator(r'^\d{12}$', 'Aadhaar ID must be exactly 12 digits.')]
    )
    ward = models.ForeignKey('wards.Ward', on_delete=models.SET_NULL, null=True, blank=True, related_name='citizens')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Citizen: {self.user.username}"

class WardMemberProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ward_member_profile')
    ward = models.ForeignKey('wards.Ward', on_delete=models.CASCADE, related_name='ward_members')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ward Member: {self.user.username}"
