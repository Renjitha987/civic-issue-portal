# Civic Issue Complaint Portal 🏙️

A complete, production-ready, advanced-level full-stack web application backend built using Django and Django REST Framework. 
This portal allows citizens to report civic issues and incorporates role-based processing for effective governance.

## Features ✨
- **Role-Based Authentication:** Admin, Department Head, Ward Member, Citizen.
- **Robust Complaint Lifecycle:** Submit, review, forward, and resolve complaints.
- **Escalation Engine:** Automatically escalates tickets sitting unresolved for over 30 days.
- **Auditing & Notifications:** Keeps detailed audit logs of critical changes and dynamically notifies users.
- **Citizen Blocking:** Gives authorization to local Ward Members to block abusive capabilities.

## Tech Stack 🛠️
- **Backend:** Python + Django + Django REST Framework
- **Database:** SQLite
- **Auth:** JWT Authentication (SimpleJWT)
- **Background Jobs:** Django Management Command natively handling escalations.

## Quick Start 🚀

1. **Activate Virtual Environment:**
   Run `.venv/Scripts/activate`
2. **Install Remaining Dependencies** (if necessary):
   Run `pip install -r requirements.txt` (Pillow, Django, DRF, djangorestframework-simplejwt, corsheaders, django-filter)
3. **Run database migrations:**
   Run `python manage.py makemigrations` and `python manage.py migrate`
4. **Generate Sample Data:**
   Run `python manage.py generate_sample_data`
   *(Creates: admin, citizen1, wardmember1, depthead)*
5. **Start Dev Server:**
   Run `python manage.py runserver`

## APIs Provided 🔑
- `/api/users/register/` - Register a user based on role validation and Aadhaar ID
- `/api/users/login/` - Login and fetch JWT access token
- `/api/complaints/` - Browse, create and manage complaints (Scoped by role permissions)
- `/api/complaints/{id}/forward/` - Pass down to Department Head (Admin / Ward Member)
- `/api/complaints/{id}/resolve/` - Mark resolved, ensuring strict workflow remarks are added
- `/api/remarks/` - Internal messaging/remarks on the ticket lifecycle
- `/api/notifications/` - View real-time system alerts
- `/api/audit-logs/` - Dedicated Read-Only Audit tracking
- `/api/wards/` & `/api/departments/` - Backend configurations

## Background Escalations ⏱️
To automate ticket severity updates (Normal -> Warning -> Critical after 30 days), configure a cron service to routinely run:
```bash
python manage.py check_escalations
```
