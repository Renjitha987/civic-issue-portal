from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .serializers import RegisterSerializer, UserSerializer
from .permissions import IsAdminUser, IsWardMember

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        token['is_blocked'] = user.is_blocked
        return token
        
    def validate(self, attrs):
        # Accept either username or email from clients and normalize whitespace.
        login_value = attrs.get(self.username_field)
        if isinstance(login_value, str):
            login_value = login_value.strip()
            attrs[self.username_field] = login_value
            if '@' in login_value:
                try:
                    matched_user = User.objects.get(email__iexact=login_value)
                    attrs[self.username_field] = matched_user.get_username()
                except User.DoesNotExist:
                    pass

        data = super().validate(attrs)
        if self.user.is_blocked:
            raise serializers.ValidationError('Your account has been blocked.')
        data['role'] = self.user.role
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

class ProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class BlockUserView(APIView):
    """
    Ward Members can block/unblock users in their ward. Admins can block anyone.
    """
    def post(self, request, user_id):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
            
        if request.user.role not in ['ADMIN', 'WARD_MEMBER']:
            return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
            
        target_user = get_object_or_404(User, id=user_id)
        
        if request.user.role == 'WARD_MEMBER' and target_user.ward != request.user.ward:
            return Response({'error': 'Can only block users within your own ward.'}, status=status.HTTP_403_FORBIDDEN)
            
        target_user.is_blocked = not target_user.is_blocked
        target_user.save()
        
        state = "blocked" if target_user.is_blocked else "unblocked"
        return Response({'message': f'User perfectly {state}.'})
