from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
from django.utils import timezone


def generate_ticket_pdf(ticket, booking=None):
    """
    Generate PDF ticket for download
    Returns: BytesIO object containing the PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a73e8'),
        spaceAfter=30,
        alignment=1  # Center
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#333333'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    normal_style = styles['Normal']
    
    elements = []
    
    # Title
    elements.append(Paragraph(f"{ticket.ticket_type} TICKET", title_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # PNR and Status
    pnr_data = [
        ['PNR Number:', ticket.pnr],
        ['Status:', ticket.status],
        ['Booking Date:', ticket.booked_at.strftime('%d %B %Y, %I:%M %p')],
    ]
    if booking and booking.razorpay_payment_id:
        pnr_data.append(['Payment ID:', booking.razorpay_payment_id])
    
    pnr_table = Table(pnr_data, colWidths=[2*inch, 3*inch])
    pnr_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f5f5f5')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    elements.append(pnr_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Journey Details
    elements.append(Paragraph("Journey Details", heading_style))
    
    journey_data = [
        ['From:', ticket.source],
        ['To:', ticket.destination],
        ['Date:', ticket.journey_date.strftime('%d %B %Y')],
        ['Time:', ticket.journey_time.strftime('%I:%M %p')],
    ]
    
    # Add type-specific details
    if hasattr(ticket, 'airline_name'):  # Flight
        journey_data.extend([
            ['Airline:', ticket.airline_name],
            ['Flight No:', ticket.flight_number],
            ['Class:', ticket.seat_class],
        ])
    elif hasattr(ticket, 'train_name'):  # Train
        journey_data.extend([
            ['Train:', ticket.train_name],
            ['Train No:', ticket.train_number],
            ['Coach:', ticket.coach],
        ])
    elif hasattr(ticket, 'bus_operator'):  # Bus
        journey_data.extend([
            ['Operator:', ticket.bus_operator],
            ['Bus Type:', ticket.bus_type],
        ])
    
    journey_table = Table(journey_data, colWidths=[2*inch, 3*inch])
    journey_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    elements.append(journey_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Passenger Details
    elements.append(Paragraph("Passenger Details", heading_style))
    
    passenger_data = [
        ['Name:', ticket.passenger_name],
        ['Age:', str(ticket.passenger_age)],
        ['Gender:', ticket.passenger_gender],
        ['Contact:', ticket.contact_number],
        ['Email:', ticket.contact_email],
    ]
    
    passenger_table = Table(passenger_data, colWidths=[2*inch, 3*inch])
    passenger_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f9f9f9')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    elements.append(passenger_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Fare Details
    elements.append(Paragraph("Fare Details", heading_style))
    
    fare_data = [
        ['Base Fare:', f'₹{ticket.base_fare}'],
        ['Taxes:', f'₹{ticket.taxes}'],
        ['Total Amount:', f'₹{ticket.total_amount}'],
    ]
    
    fare_table = Table(fare_data, colWidths=[2*inch, 3*inch])
    fare_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f0f0')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('LINEBELOW', (0, -1), (-1, -1), 2, colors.black),
    ]))
    elements.append(fare_table)
    elements.append(Spacer(1, 0.5*inch))
    
    # Footer
    footer_text = """
    <para alignment="center">
    Thank you for booking with MyTravel!<br/>
    For any queries, please contact our customer support.<br/>
    <b>This is a computer-generated ticket.</b>
    </para>
    """
    elements.append(Paragraph(footer_text, normal_style))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    
    return buffer
