import pandas as pd
from io import StringIO
from .models import Dataset, Equipment


def parse_csv_and_save(dataset: Dataset, file_content: bytes) -> dict:
    """
    Parse CSV file content and save equipment data to database.
    Returns summary statistics.
    """
    # Read CSV content
    content = file_content.decode('utf-8')
    df = pd.read_csv(StringIO(content))
    
    # Validate required columns
    required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
    missing = set(required_columns) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    # Clean and process data
    df = df.dropna()
    
    # Create Equipment objects
    equipment_objects = []
    for _, row in df.iterrows():
        equipment_objects.append(Equipment(
            dataset=dataset,
            name=row['Equipment Name'],
            equipment_type=row['Type'],
            flowrate=float(row['Flowrate']),
            pressure=float(row['Pressure']),
            temperature=float(row['Temperature'])
        ))
    
    # Bulk create
    Equipment.objects.bulk_create(equipment_objects)
    
    # Calculate and save statistics
    stats = {
        'total_count': len(df),
        'avg_flowrate': df['Flowrate'].mean(),
        'avg_pressure': df['Pressure'].mean(),
        'avg_temperature': df['Temperature'].mean(),
    }
    
    # Update dataset with stats
    dataset.total_count = stats['total_count']
    dataset.avg_flowrate = round(stats['avg_flowrate'], 2)
    dataset.avg_pressure = round(stats['avg_pressure'], 2)
    dataset.avg_temperature = round(stats['avg_temperature'], 2)
    dataset.save()
    
    return stats


def get_type_distribution(dataset: Dataset) -> dict:
    """Get equipment count by type for a dataset."""
    from django.db.models import Count
    
    distribution = (
        dataset.equipment
        .values('equipment_type')
        .annotate(count=Count('id'))
        .order_by('equipment_type')
    )
    return {item['equipment_type']: item['count'] for item in distribution}
