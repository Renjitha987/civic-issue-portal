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
    from wards.models import Ward
    from departments.models import Department
    
    q = request.GET.get('q', '')
    selected_category = request.GET.get('category', 'All')
    selected_ward = request.GET.get('ward', 'All')
    selected_priority = request.GET.get('priority', 'All')
    
    complaints = Complaint.objects.all().select_related('ward', 'department', 'citizen', 'assigned_to').order_by('-date_submitted', '-id')

    if q:
        complaints = complaints.filter(Q(description__icontains=q) | Q(issue_category__icontains=q) | Q(location__icontains=q))
    if selected_category != 'All':
        complaints = complaints.filter(issue_category=selected_category)
    if selected_ward != 'All':
        complaints = complaints.filter(ward_id=selected_ward)
    if selected_priority != 'All':
        complaints = complaints.filter(priority_level=selected_priority)

    # Stats Calculation
    stats = {
        'total': complaints.count(),
        'forwarded': complaints.filter(status='Forwarded').count(),
        'pending': complaints.filter(Q(status='Pending') | Q(status='In Progress')).count(),
        'escalated': complaints.filter(is_escalated=True).count(),
    }

    context = {
        'forwarded_complaints': complaints.filter(status='Forwarded'),
        'pending_complaints': complaints.filter(Q(status='Pending') | Q(status='In Progress') | Q(status='Escalated')),
        'resolved_complaints': complaints.filter(status='Resolved'),
        'stats': stats,
        'selected_category': selected_category,
        'selected_ward': selected_ward,
        'selected_priority': selected_priority,
        'q': q,
        'categories': Department.objects.values_list('department_name', flat=True),
        'wards': Ward.objects.all(),
        'priorities': ['Normal', 'Warning', 'Critical']
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
