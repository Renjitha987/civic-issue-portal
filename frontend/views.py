from django.shortcuts import render
from complaints.models import Complaint
from django.db.models import Case, When, Value, IntegerField, Q


def home(request):
    return render(request, 'frontend/index.html')



def login_page(request):
    return render(request, 'frontend/login.html')

def register_page(request):
    return render(request, 'frontend/register.html')

def admin_dashboard(request):
    selected_category = request.GET.get('category', 'All')
    complaints = Complaint.objects.all().order_by('-date_submitted', '-id')

    if selected_category != 'All':
        complaints = complaints.filter(issue_category=selected_category)

    # Stats Calculation
    stats = {
        'total': complaints.count(),
        'pending': complaints.filter(Q(status='Pending') | Q(status='In Progress')).count(),
        'escalated': complaints.filter(is_escalated=True).count(),
    }

    context = {
        'forwarded_complaints': complaints.filter(status='Forwarded'),
        'pending_complaints': complaints.filter(status='Pending'),
        'resolved_complaints': complaints.filter(status='Resolved'),
        'stats': stats,
        'selected_category': selected_category,
        'categories': ['Electricity', 'Road', 'Waste', 'Health', 'Water']
    }
    return render(request, 'frontend/admin_dashboard.html', context)



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
