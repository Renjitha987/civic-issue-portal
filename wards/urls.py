from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WardViewSet

router = DefaultRouter()
router.register(r'wards', WardViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
