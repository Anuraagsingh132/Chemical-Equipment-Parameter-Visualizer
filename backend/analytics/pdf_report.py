from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER


def generate_pdf_report(dataset, type_distribution: dict) -> BytesIO:
    """Generate a PDF report for the dataset."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        alignment=TA_CENTER,
        spaceAfter=30
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=10
    )
    
    elements = []
    
    # Title
    elements.append(Paragraph("Chemical Equipment Analysis Report", title_style))
    elements.append(Spacer(1, 12))
    
    # Dataset Info
    elements.append(Paragraph(f"<b>Dataset:</b> {dataset.name}", styles['Normal']))
    elements.append(Paragraph(f"<b>Uploaded:</b> {dataset.uploaded_at.strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 20))
    
    # Summary Statistics
    elements.append(Paragraph("Summary Statistics", heading_style))
    
    stats_data = [
        ['Metric', 'Value'],
        ['Total Equipment', str(dataset.total_count)],
        ['Average Flowrate', f'{dataset.avg_flowrate:.2f}'],
        ['Average Pressure', f'{dataset.avg_pressure:.2f}'],
        ['Average Temperature', f'{dataset.avg_temperature:.2f}'],
    ]
    
    stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F46E5')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F3F4F6')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#D1D5DB')),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
    ]))
    elements.append(stats_table)
    elements.append(Spacer(1, 30))
    
    # Equipment Type Distribution
    elements.append(Paragraph("Equipment Type Distribution", heading_style))
    
    dist_data = [['Equipment Type', 'Count']]
    for eq_type, count in type_distribution.items():
        dist_data.append([eq_type, str(count)])
    
    dist_table = Table(dist_data, colWidths=[3*inch, 2*inch])
    dist_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F3F4F6')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#D1D5DB')),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
    ]))
    elements.append(dist_table)
    
    # Equipment List
    elements.append(Spacer(1, 30))
    elements.append(Paragraph("Equipment Details", heading_style))
    
    # Status logic based on temperature (matches web frontend)
    def get_status(temp):
        if temp > 150:
            return 'Offline'
        elif temp >= 90:
            return 'Warning'
        else:
            return 'Active'
    
    eq_data = [['ID', 'Name', 'Type', 'Flowrate', 'Pressure', 'Temp', 'Status']]
    for eq in dataset.equipment.all()[:20]:  # Limit to first 20
        eq_data.append([
            f'#{eq.id}',
            eq.name, 
            eq.equipment_type,
            f'{eq.flowrate:.1f}',
            f'{eq.pressure:.1f}',
            f'{eq.temperature:.1f}',
            get_status(eq.temperature)
        ])
    
    eq_table = Table(eq_data, colWidths=[0.5*inch, 1.3*inch, 1*inch, 0.8*inch, 0.8*inch, 0.7*inch, 0.7*inch])
    eq_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#7C3AED')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # Headers centered
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # ID column centered
        ('ALIGN', (1, 1), (2, -1), 'LEFT'),    # Name, Type left-aligned
        ('ALIGN', (3, 1), (5, -1), 'RIGHT'),   # Flowrate, Pressure, Temp right-aligned
        ('ALIGN', (6, 1), (6, -1), 'CENTER'),  # Status centered
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#D1D5DB')),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
    ]))
    elements.append(eq_table)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer
