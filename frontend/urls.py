from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register_page'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/ward_member/', views.ward_member_dashboard, name='ward_member_dashboard'),
    path('dashboard/department_head/', views.department_head_dashboard, name='department_head_dashboard'),
    path('dashboard/citizen/', views.citizen_dashboard, name='citizen_dashboard'),
    path('complaint/submit/', views.submit_complaint, name='submit_complaint'),
    path('complaint/track/', views.track_complaint, name='track_complaint'),
    path('management/wards/', views.ward_management, name='ward_management'),
    path('management/departments/', views.department_management, name='department_management'),
]
