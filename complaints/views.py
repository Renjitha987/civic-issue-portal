from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import BlockedUsersCannotAccess
from .models import Complaint, ComplaintForwarding, Remark
from departments.models import Department
from .serializers import ComplaintSerializer, RemarkSerializer
from django.utils import timezone

class ComplaintViewSet(viewsets.ModelViewSet):
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated, BlockedUsersCannotAccess]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return Complaint.objects.all()
        elif user.role == 'WARD_MEMBER':
            return Complaint.objects.filter(ward=user.ward)
        elif user.role == 'DEPARTMENT_HEAD':
            from django.db.models import Q
            return Complaint.objects.filter(
                Q(department__head=user) | Q(forwardings__department__head=user)
            ).distinct()
        elif user.role == 'CITIZEN':
            return Complaint.objects.filter(citizen=user)
        return Complaint.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'CITIZEN':
            raise serializers.ValidationError('Only Citizens can create complaints directly.')
        if not hasattr(user, 'ward') or not user.ward:
            raise serializers.ValidationError('Your citizen profile is missing a registered ward. Please update your profile or contact an administrator before filing a complaint.')
        serializer.save(citizen=user, ward=user.ward)

    def perform_update(self, serializer):
        complaint = self.get_object()
        if self.request.user.role == 'CITIZEN' and complaint.status != 'Pending':
            raise serializers.ValidationError('You can only edit pending complaints.')
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.role == 'CITIZEN' and instance.status != 'Pending':
            raise serializers.ValidationError('You can only delete pending complaints.')
        instance.delete()

    @action(detail=True, methods=['get'])
    def image(self, request, pk=None):
        from django.http import FileResponse, Http404
        complaint = self.get_object()
        if complaint.image:
            return FileResponse(complaint.image.open('rb'))
        raise Http404("Image not found")

    @action(detail=True, methods=['post'])
    def forward(self, request, pk=None):
        complaint = self.get_object()
        user = request.user

        if user.role not in ['ADMIN', 'WARD_MEMBER']:
            return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        department_id = request.data.get('department_id')
        remark_message = request.data.get('remark')

        if not department_id or not remark_message:
            return Response({'error': 'department_id and remark are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            return Response({'error': 'Department not found.'}, status=status.HTTP_404_NOT_FOUND)

        complaint.department = department
        complaint.status = 'Forwarded'
        complaint.save()

        ComplaintForwarding.objects.create(
            complaint=complaint,
            department=department,
            forwarded_by=user
        )

        Remark.objects.create(
            complaint=complaint,
            added_by=user,
            role=user.role,
            message=remark_message
        )

        return Response({'status': 'Complaint forwarded successfully.'})

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        complaint = self.get_object()
        user = request.user
        
        if user.role == 'CITIZEN':
            return Response({'error': 'Citizens cannot resolve complaints.'}, status=status.HTTP_403_FORBIDDEN)

        remark_message = request.data.get('remark')
        if not remark_message:
            return Response({'error': 'A remark is required to resolve a complaint.'}, status=status.HTTP_400_BAD_REQUEST)

        complaint.status = 'Resolved'
        complaint.resolved_date = timezone.now()
        complaint.save()

        Remark.objects.create(
            complaint=complaint,
            added_by=user,
            role=user.role,
            message=remark_message
        )

        return Response({'status': 'Complaint marked as resolved.'})

class RemarkViewSet(viewsets.ModelViewSet):
    serializer_class = RemarkSerializer
    permission_classes = [IsAuthenticated, BlockedUsersCannotAccess]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return Remark.objects.all()
        elif user.role == 'WARD_MEMBER':
            return Remark.objects.filter(complaint__ward=user.ward)
        elif user.role == 'DEPARTMENT_HEAD':
            from django.db.models import Q
            return Remark.objects.filter(
                Q(complaint__department__head=user) | Q(complaint__forwardings__department__head=user)
            ).distinct()
        elif user.role == 'CITIZEN':
            return Remark.objects.filter(complaint__citizen=user)
        return Remark.objects.none()

    def perform_create(self, serializer):
        complaint = serializer.validated_data['complaint']
        user = self.request.user

        if user.role == 'CITIZEN' and complaint.citizen != user:
            raise serializers.ValidationError('You can only comment on your own complaints.')
        elif user.role == 'WARD_MEMBER' and complaint.ward != user.ward:
            raise serializers.ValidationError('You can only comment on complaints in your ward.')

        if user.role in ['WARD_MEMBER', 'DEPARTMENT_HEAD'] and complaint.status == 'Pending':
            complaint.status = 'In Progress'
            complaint.save()

        serializer.save(added_by=user, role=user.role)

    def perform_update(self, serializer):
        from rest_framework.exceptions import PermissionDenied
        instance = self.get_object()
        user = self.request.user
        if user.role != 'ADMIN' and instance.added_by != user:
            raise PermissionDenied('You can only edit your own remarks.')
        serializer.save()

    def perform_destroy(self, instance):
        from rest_framework.exceptions import PermissionDenied
        user = self.request.user
        if user.role != 'ADMIN' and instance.added_by != user:
            raise PermissionDenied('You can only delete your own remarks.')
        instance.delete()
