from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import render_to_string

def generate_pdf_receipt(service):
    html = render_to_string('pdf/receipt_template.html', {'service': service})
    result = BytesIO()
    pisa.CreatePDF(html, dest=result)
    return result
