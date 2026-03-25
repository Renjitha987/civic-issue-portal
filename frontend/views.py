from django.shortcuts import render

def home(request):
    return render(request, 'frontend/index.html')

def login_page(request):
    return render(request, 'frontend/login.html')

def register_page(request):
    return render(request, 'frontend/register.html')

def admin_dashboard(request):
    return render(request, 'frontend/admin_dashboard.html')

def ward_member_dashboard(request):
    return render(request, 'frontend/ward_member_dashboard.html')

def department_head_dashboard(request):
    return render(request, 'frontend/department_head_dashboard.html')

def citizen_dashboard(request):
    return render(request, 'frontend/citizen_dashboard.html')

def submit_complaint(request):
    return render(request, 'frontend/submit_complaint.html')

def track_complaint(request):
    return render(request, 'frontend/track_complaint.html')

def ward_management(request):
    return render(request, 'frontend/ward_management.html')

def department_management(request):
    return render(request, 'frontend/department_management.html')
