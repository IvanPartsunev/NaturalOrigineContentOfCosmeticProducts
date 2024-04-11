import os

from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Table, PageTemplate, Image, Frame

from NaturalOriginContentOfCosmeticProducts.settings import STATICFILES_DIRS


def export_pdf(product_formula_data):
    # Create a buffer object to write PDF data
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="product_formula_details.pdf"'
    buffer = response

    page_size = landscape(A4)
    left_margin = 0.5 * cm
    right_margin = 0.5 * cm
    top_margin = 0.5 * cm
    bottom_margin = 0.5 * cm

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(buffer, pagesize=page_size, leftMargin=left_margin, rightMargin=right_margin,
                            topMargin=top_margin, bottomMargin=bottom_margin)

    font_path = os.path.join(STATICFILES_DIRS[0], 'fonts', 'Roboto-Regular.ttf')
    pdfmetrics.registerFont(TTFont('Roboto', font_path))

    image_width = 4.8 * cm
    image_height = 1 * cm

    image_path = os.path.join(STATICFILES_DIRS[0], 'img', 'web-site-logo.png')
    header_image = Image(image_path, width=image_width, height=image_height, hAlign="LEFT")

    # Define a custom styles
    # 0=left, 1=center, 2=right

    centered_style_prod_name = ParagraphStyle(
        name='CenteredStyle',
        fontSize=16,
        fontName="Roboto",
        spaceAfter=20,
        alignment=1
    )

    centered_style_desc = ParagraphStyle(
        name='CenteredStyle',
        fontSize=12,
        spaceAfter=20,
        alignment=1
    )

    style_noc = ParagraphStyle(
        name='NocStyle',
        fontSize=11,
        fontName="Roboto",
        spaceBefore=20,
        alignment=0
    )

    style_date = ParagraphStyle(
        name='NocStyle',
        fontSize=9,
        fontName="Roboto",
        spaceBefore=10,
        spaceAfter=10,
        alignment=0
    )

    # Add content to the PDF
    content = [
        Paragraph("", styles['Normal']),
        Paragraph("", styles['Normal']),
        Paragraph("Product Name: {}".format(product_formula_data.product.product_name), centered_style_prod_name),
        Paragraph("Description: {}".format(product_formula_data.description or ""), centered_style_desc),
        Paragraph("", styles['Normal']),
    ]

    data = [['#', 'Trade Name', 'INCI Name', 'Content %', 'Material Type %']]

    for index, product in enumerate(product_formula_data.formula.all(), start=1):
        raw_material = product.raw_material
        row_num = str(index)
        raw_material_content = str(product.raw_material_content)
        natural_origin_content = str(raw_material.natural_origin_content)
        data.append([row_num, raw_material.trade_name, raw_material.inci_name, raw_material_content,
                     raw_material.material_type, natural_origin_content])

    table_style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
                              ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                              ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                              ('FONTNAME', (0, 0), (-1, 0), 'Roboto'),
                              ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                              ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                              ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
                              ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                              ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                              ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                              ('FONTNAME', (0, 0), (-1, 0), 'Roboto'),
                              ('FONTSIZE', (0, 0), (-1, 0), 12),
                              ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                              ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                              ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                              ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                              ('FONTNAME', (0, 0), (-1, -1), 'Roboto'),
                              ('GRID', (0, 0), (-1, -1), 0, colors.gray),
                              ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                              ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                              ('SPAN', (1, 0), (1, 0)),
                              ('SPAN', (4, 0), (5, 0)),
                              ('WORDWRAP', (0, 0), (-1, -1))])  # Enable word wrap for all cells

    table = Table(data, splitByRow=True)  # Explicitly set splitByRow to True
    table.setStyle(table_style)

    content.append(table)

    product_noc = product_formula_data.product.natural_content
    product_date = product_formula_data.product.edited_on
    content.append(Paragraph(f"Natural origin content of the product: {product_noc} %", style_noc))
    content.append(Paragraph(f"Date calculated: {product_date}", style_date))
    content.append(header_image)

    doc.build(content)

    return response
