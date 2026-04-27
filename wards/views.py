from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.permissions import IsAdminUser, BlockedUsersCannotAccess
from .models import Ward, Panchayat
from .serializers import WardSerializer, PanchayatSerializer

class WardViewSet(viewsets.ModelViewSet):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated(), BlockedUsersCannotAccess()]

class PanchayatViewSet(viewsets.ModelViewSet):
    queryset = Panchayat.objects.all()
    serializer_class = PanchayatSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated(), BlockedUsersCannotAccess()]
