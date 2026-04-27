from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WardViewSet, PanchayatViewSet

router = DefaultRouter()
router.register(r'wards', WardViewSet)
router.register(r'panchayats', PanchayatViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
