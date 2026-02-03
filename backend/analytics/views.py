from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import HttpResponse
from django.db.models import Count
from io import BytesIO

from .models import Dataset, Equipment
from .serializers import (
    DatasetSerializer, DatasetDetailSerializer, 
    EquipmentSerializer, UploadSerializer
)
from .services import parse_csv_and_save, get_type_distribution
from .pdf_report import generate_pdf_report


class DatasetViewSet(viewsets.ModelViewSet):
    """ViewSet for Dataset CRUD operations."""
    serializer_class = DatasetSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        """Return only datasets for the current user."""
        # Don't slice here - it breaks detail lookups
        # We limit to 5 in the list action instead
        return Dataset.objects.filter(user=self.request.user).order_by('-uploaded_at')

    def list(self, request, *args, **kwargs):
        """List datasets, limited to last 5."""
        queryset = self.get_queryset()[:5]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DatasetDetailSerializer
        return DatasetSerializer

    def create(self, request, *args, **kwargs):
        """Handle CSV file upload."""
        serializer = UploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        uploaded_file = serializer.validated_data['file']
        
        # Read file content BEFORE saving (Django will exhaust the stream when saving)
        file_content = uploaded_file.read()
        uploaded_file.seek(0)  # Reset file pointer for saving
        
        # Create dataset
        dataset = Dataset.objects.create(
            user=request.user,
            name=uploaded_file.name,
            file=uploaded_file
        )
        
        try:
            # Parse and save equipment data using the content we already read
            parse_csv_and_save(dataset, file_content)
            
            # Enforce last 5 datasets limit
            self._enforce_dataset_limit(request.user)
            
            return Response(
                DatasetSerializer(dataset).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            dataset.delete()
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def _enforce_dataset_limit(self, user, limit=5):
        """Delete older datasets beyond the limit."""
        datasets = Dataset.objects.filter(user=user).order_by('-uploaded_at')
        if datasets.count() > limit:
            for old_dataset in datasets[limit:]:
                old_dataset.delete()

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get detailed statistics for a dataset."""
        dataset = self.get_object()
        type_distribution = get_type_distribution(dataset)
        
        return Response({
            'total_count': dataset.total_count,
            'avg_flowrate': dataset.avg_flowrate,
            'avg_pressure': dataset.avg_pressure,
            'avg_temperature': dataset.avg_temperature,
            'type_distribution': type_distribution
        })

    @action(detail=True, methods=['get'])
    def equipment(self, request, pk=None):
        """Get all equipment data for a dataset."""
        dataset = self.get_object()
        equipment = dataset.equipment.all()
        serializer = EquipmentSerializer(equipment, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def report(self, request, pk=None):
        """Generate and download PDF report."""
        dataset = self.get_object()
        type_distribution = get_type_distribution(dataset)
        
        # Generate PDF
        pdf_buffer = generate_pdf_report(dataset, type_distribution)
        
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{dataset.name}_report.pdf"'
        return response
