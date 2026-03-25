from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ComplaintViewSet, RemarkViewSet

router = DefaultRouter()
router.register(r'complaints', ComplaintViewSet, basename='complaint')
router.register(r'remarks', RemarkViewSet, basename='remark')

urlpatterns = [
    path('', include(router.urls)),
]
