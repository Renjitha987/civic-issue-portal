from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdminUser, BlockedUsersCannotAccess
from .models import Department
from .serializers import DepartmentSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated(), BlockedUsersCannotAccess()]
