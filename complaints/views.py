from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import BlockedUsersCannotAccess
from .models import Complaint, ComplaintForwarding, Remark
from departments.models import Department
from .serializers import ComplaintSerializer, RemarkSerializer
from django.utils import timezone
from django.http import HttpResponse, FileResponse
import csv
import io
from datetime import timedelta
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all()
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

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def weekly_report(self, request):
        if request.user.role != 'ADMIN':
            return Response({'error': 'Unauthorized. Only admins can generate reports.'}, status=status.HTTP_403_FORBIDDEN)

        report_type = request.query_params.get('report_type', 'csv').lower()
        last_week = timezone.now() - timedelta(days=7)
        complaints = Complaint.objects.filter(date_submitted__gte=last_week)

        if report_type == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="weekly_report.csv"'
            writer = csv.writer(response)
            writer.writerow(['ID', 'Citizen', 'Category', 'Status', 'Priority', 'Date Submitted'])
            for c in complaints:
                citizen_name = c.citizen.username if c.citizen else "Anonymous"
                writer.writerow([c.id, citizen_name, c.issue_category, c.status, c.priority_level, c.date_submitted.strftime('%Y-%m-%d %H:%M')])
            return response

        elif report_type == 'pdf':
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()

            elements.append(Paragraph("Civic Issue Portal - Weekly Status Report", styles['Title']))
            elements.append(Paragraph(f"Period: {last_week.strftime('%Y-%m-%d')} to {timezone.now().strftime('%Y-%m-%d')}", styles['Normal']))
            elements.append(Spacer(1, 12))

            data = [['ID', 'Citizen', 'Category', 'Status', 'Priority']]
            for c in complaints:
                citizen_name = c.citizen.username if c.citizen else "Anonymous"
                data.append([str(c.id), citizen_name, c.issue_category, c.status, c.priority_level])

            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table)
            doc.build(elements)
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename='weekly_report.pdf')

        return Response({'error': 'Invalid format. Choose pdf or csv.'}, status=status.HTTP_400_BAD_REQUEST)

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
