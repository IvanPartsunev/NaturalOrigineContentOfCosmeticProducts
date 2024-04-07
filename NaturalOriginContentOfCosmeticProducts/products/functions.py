import os

from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Table, PageTemplate

from NaturalOriginContentOfCosmeticProducts.settings import STATICFILES_DIRS


def export_pdf(product_formula_data):
    # Create a buffer object to write PDF data
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="product_formula_details.pdf"'
    buffer = response

    page_size = landscape(letter)

    font_path = os.path.join(STATICFILES_DIRS[0], 'fonts', 'EncodeSansExpanded-Regular.ttf')
    pdfmetrics.registerFont(TTFont('Encode', font_path))

    # Create a PDF document object
    doc = SimpleDocTemplate(buffer, pagesize=page_size)

    # Define a custom style with centered alignment
    centered_style_prod_name = ParagraphStyle(
        name='CenteredStyle',
        fontSize=16,
        spaceAfter=20,
        alignment=1  # 0=left, 1=center, 2=right
    )

    centered_style_desc = ParagraphStyle(
        name='CenteredStyle',
        fontSize=12,
        spaceAfter=20,
        alignment=1  # 0=left, 1=center, 2=right
    )

    style_noc = ParagraphStyle(
        name='NocStyle',
        fontSize=11,
        spaceBefore=20,
        alignment=0  # 0=left, 1=center, 2=right
    )

    style_date = ParagraphStyle(
        name='NocStyle',
        fontSize=9,
        spaceBefore=15,
        alignment=0  # 0=left, 1=center, 2=right
    )

    # Add content to the PDF
    content = []
    styles = getSampleStyleSheet()
    content.append(
        Paragraph("Product Name: {}".format(product_formula_data.product.product_name), centered_style_prod_name))
    content.append(Paragraph("Description: {}".format(product_formula_data.description or ""), centered_style_desc))
    content.append(Paragraph("", styles['Normal']))

    data = [['#', 'Trade Name', 'INCI Name', 'Raw Material Content', 'Material Type', 'Natural Origin Content']]
    for index, product in enumerate(product_formula_data.formula.all(), start=1):
        raw_material = product.raw_material
        # Convert decimal objects to strings before adding to the table
        row_num = str(index)
        raw_material_content = str(product.raw_material_content)
        natural_origin_content = str(raw_material.natural_origin_content)
        data.append([row_num, raw_material.trade_name, raw_material.inci_name, raw_material_content,
                     raw_material.material_type, natural_origin_content])

    table_style = TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),

    ])

    table = Table(data)
    table.setStyle(table_style)
    content.append(table)

    product_noc = product_formula_data.product.natural_content
    product_date = product_formula_data.product.edited_on
    content.append(Paragraph(f"Natural origin content of the product: {product_noc} %", style_noc))
    content.append(Paragraph(f"Date calculated: {product_date}", style_date))

    # Build the PDF document
    doc.build(content)

    return response
