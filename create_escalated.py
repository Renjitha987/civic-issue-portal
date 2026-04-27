import os
import django
from django.utils import timezone
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'civic_portal.settings')
django.setup()

from complaints.models import Complaint
from django.contrib.auth import get_user_model
User = get_user_model()
from wards.models import Ward
from departments.models import Department

citizen = User.objects.filter(role='CITIZEN').first()
ward = Ward.objects.first()
department = Department.objects.first()

if citizen and ward:
    complaint = Complaint.objects.create(
        citizen=citizen,
        ward=ward,
        issue_category="Water Supply",
        description="Major water pipe burst flooding the intersection. Urgent attention needed to prevent property damage and water waste.",
        location="Intersection of Elm St and 5th Ave",
        status="Pending",
        priority_level="Critical",
        is_escalated=False,
        department=department
    )
    print(f"Successfully created CRITICAL complaint: {complaint.id}")
else:
    print("Failed to create. No citizen or ward found.")
