from rest_framework import serializers
from .models import Complaint, ComplaintForwarding, Remark

class RemarkSerializer(serializers.ModelSerializer):
    added_by_name = serializers.CharField(source='added_by.username', read_only=True)

    class Meta:
        model = Remark
        fields = '__all__'
        read_only_fields = ['added_by', 'role']

class ComplaintForwardingSerializer(serializers.ModelSerializer):
    forwarded_by_name = serializers.CharField(source='forwarded_by.username', read_only=True)
    department_name = serializers.CharField(source='department.department_name', read_only=True)

    class Meta:
        model = ComplaintForwarding
        fields = '__all__'
        read_only_fields = ['forwarded_by']

class ComplaintSerializer(serializers.ModelSerializer):
    citizen_name = serializers.CharField(source='citizen.username', read_only=True)
    remarks = RemarkSerializer(many=True, read_only=True)
    forwardings = ComplaintForwardingSerializer(many=True, read_only=True)

    class Meta:
        model = Complaint
        fields = '__all__'
        read_only_fields = ['citizen', 'ward', 'status', 'assigned_to', 'department', 'priority_level', 'escalation_date', 'resolved_date', 'is_escalated']

    def validate_image(self, value):
        if value:
            ext = value.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png']:
                raise serializers.ValidationError('Image must be a JPG, JPEG, or PNG file.')
            max_size_mb = 5
            if hasattr(value, 'size') and value.size > max_size_mb * 1024 * 1024:
                raise serializers.ValidationError(f"Image size cannot exceed {max_size_mb}MB.")
        return value

    def validate_description(self, value):
        if len(value) < 10:
            raise serializers.ValidationError('Description must be at least 10 characters long.')
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.image:
            request = self.context.get('request')
            if request:
                representation['image'] = request.build_absolute_uri(f'/api/complaints/{instance.id}/image/')
            else:
                representation['image'] = f'/api/complaints/{instance.id}/image/'
        return representation
