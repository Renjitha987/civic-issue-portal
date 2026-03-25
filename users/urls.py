from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView, ProfileView, BlockUserView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('block/<int:user_id>/', BlockUserView.as_view(), name='block_user'),
]
