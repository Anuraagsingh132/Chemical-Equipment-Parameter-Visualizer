from rest_framework import serializers
from .models import Dataset, Equipment


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'name', 'equipment_type', 'flowrate', 'pressure', 'temperature']


class DatasetSerializer(serializers.ModelSerializer):
    equipment_count = serializers.SerializerMethodField()

    class Meta:
        model = Dataset
        fields = [
            'id', 'name', 'uploaded_at', 'total_count',
            'avg_flowrate', 'avg_pressure', 'avg_temperature',
            'equipment_count'
        ]

    def get_equipment_count(self, obj):
        return obj.equipment.count()


class DatasetDetailSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer(many=True, read_only=True)
    type_distribution = serializers.SerializerMethodField()

    class Meta:
        model = Dataset
        fields = [
            'id', 'name', 'uploaded_at', 'total_count',
            'avg_flowrate', 'avg_pressure', 'avg_temperature',
            'equipment', 'type_distribution'
        ]

    def get_type_distribution(self, obj):
        """Returns count of equipment grouped by type."""
        from django.db.models import Count
        return list(
            obj.equipment.values('equipment_type')
            .annotate(count=Count('id'))
            .order_by('equipment_type')
        )


class UploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        # Check file extension (case-insensitive)
        filename = value.name.lower() if value.name else ''
        valid_extensions = ['.csv']
        
        # Also accept common CSV MIME types
        valid_content_types = [
            'text/csv',
            'application/csv',
            'application/vnd.ms-excel',
            'text/plain',
            'application/octet-stream',  # Sometimes browsers send this
        ]
        
        has_valid_extension = any(filename.endswith(ext) for ext in valid_extensions)
        has_valid_content_type = value.content_type in valid_content_types
        
        if not has_valid_extension and not has_valid_content_type:
            raise serializers.ValidationError(
                f"Only CSV files are allowed. Got: {value.name} ({value.content_type})"
            )
        return value

