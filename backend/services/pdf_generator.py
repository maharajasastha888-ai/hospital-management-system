import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime


def generate_invoice_pdf(bill):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5 * inch, bottomMargin=0.5 * inch)
    styles = getSampleStyleSheet()
    elements = []

    title_style = ParagraphStyle(
        'CustomTitle', parent=styles['Heading1'],
        fontSize=20, spaceAfter=12, alignment=1
    )
    elements.append(Paragraph('HOSPITAL MANAGEMENT SYSTEM', title_style))
    elements.append(Paragraph('123 Health Street, Medical City', styles['Normal']))
    elements.append(Paragraph('Phone: +1-234-567-8900 | Email: info@hospital.com', styles['Normal']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f'<b>INVOICE #{bill.invoice_number}</b>', styles['Heading2']))
    elements.append(Spacer(1, 6))

    patient_name = f'{bill.patient.first_name} {bill.patient.last_name}' if bill.patient else 'N/A'
    info_data = [
        ['Patient:', patient_name],
        ['Date:', bill.created_at.strftime('%Y-%m-%d %H:%M') if bill.created_at else 'N/A'],
        ['Status:', bill.status.upper()],
    ]
    info_table = Table(info_data, colWidths=[1.5 * inch, 4 * inch])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 12))

    charges_data = [
        ['Description', 'Amount ($)'],
        ['Consultation Fee', f'{bill.consultation_fee:.2f}'],
        ['Lab Fee', f'{bill.lab_fee:.2f}'],
        ['Medicine Fee', f'{bill.medicine_fee:.2f}'],
        ['Other Fee', f'{bill.other_fee:.2f}'],
        ['Total Amount', f'{bill.total_amount:.2f}'],
        ['Paid Amount', f'{bill.paid_amount:.2f}'],
        ['Due Amount', f'{bill.due_amount:.2f}'],
    ]

    charges_table = Table(charges_data, colWidths=[4 * inch, 1.5 * inch])
    charges_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, -3), (-1, -3), colors.HexColor('#f0f0f0')),
        ('BACKGROUND', (0, -2), (-1, -2), colors.HexColor('#e8f5e9')),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#ffebee')),
        ('FONTNAME', (0, -3), (-1, -1), 'Helvetica-Bold'),
    ]))
    elements.append(charges_table)
    elements.append(Spacer(1, 20))

    elements.append(Paragraph('<i>Thank you for choosing our hospital. We wish you good health!</i>', styles['Normal']))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
