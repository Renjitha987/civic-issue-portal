from django.db import models
from django.conf import settings
from wards.models import Ward
from departments.models import Department

class Complaint(models.Model):
    CATEGORY_CHOICES = (
        ('Waste', 'Waste'),
        ('Electricity', 'Electricity'),
        ('Road', 'Road'),
        ('Health', 'Health'),
        ('Water', 'Water'),
    )
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Forwarded', 'Forwarded'),
        ('Resolved', 'Resolved'),
        ('Escalated', 'Escalated'),
    )
    PRIORITY_CHOICES = (
        ('Normal', 'Normal'),
        ('Warning', 'Warning'),
        ('Critical', 'Critical'),
    )

    citizen = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='filed_complaints')
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='complaints')
    issue_category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    location = models.CharField(max_length=255)
    
    def validate_image_size(file):
        from django.core.exceptions import ValidationError
        max_size_mb = 5
        if file and hasattr(file, 'size') and file.size > max_size_mb * 1024 * 1024:
            raise ValidationError(f"Image size cannot exceed {max_size_mb}MB.")

    image = models.ImageField(upload_to='complaints/images/', blank=True, null=True, validators=[validate_image_size])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_complaints'
    )
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='complaints')
    priority_level = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Normal')
    
    date_submitted = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    escalation_date = models.DateTimeField(null=True, blank=True)
    resolved_date = models.DateTimeField(null=True, blank=True)
    is_escalated = models.BooleanField(default=False)

    def __str__(self):
        return f"Complaint {self.id} - {self.issue_category} ({self.status})"

class ComplaintForwarding(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='forwardings')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='forwardings')
    forwarded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='forwarded_complaints')
    forwarded_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Forwarding for {self.complaint.id} to {self.department.department_name}"

class Remark(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='remarks')
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='remarks_added')
    role = models.CharField(max_length=50)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Remark by {self.added_by.username} on Complaint {self.complaint.id}"
