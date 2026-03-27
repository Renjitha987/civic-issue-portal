import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'civic_portal.settings')
django.setup()

from users.models import User

u = User.objects.filter(username__icontains='sneha').first() or User.objects.filter(full_name__icontains='sneha').first()
if u:
    if u.ward:
        print(f"User {u.username} (Full name: {u.full_name}) is in ward: {u.ward.ward_name}")
    else:
        print(f"User {u.username} (Full name: {u.full_name}) has no ward assigned.")
else:
    print("User 'sneha' not found.")
