from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.permissions import IsAdminUser, BlockedUsersCannotAccess
from .models import Ward
from .serializers import WardSerializer

class WardViewSet(viewsets.ModelViewSet):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated(), BlockedUsersCannotAccess()]

