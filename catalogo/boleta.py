# catalogo/boleta.py

from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import json

def generar_boleta(request, nombre, total, productos, metodo_pago, alias):
    # Lógica para generar el PDF de la boleta
    total = float(total)
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, 750, f"Boleta de Venta")
    p.setFont("Helvetica", 12)
    p.drawString(100, 730, f"Cliente: {nombre}")
    p.drawString(100, 710, f"Método de pago: {metodo_pago} ({alias})")
    p.drawString(100, 690, f"Total: ${total:.2f}")

    y_position = 650
    p.setFont("Helvetica", 10)
    p.drawString(100, y_position, "Producto")
    p.drawString(300, y_position, "Cantidad")
    p.drawString(500, y_position, "Total")
    y_position -= 20

    for producto in productos:
        p.drawString(100, y_position, f"{producto['nombre']}")
        p.drawString(300, y_position, f"{producto['cantidad']}")
        p.drawString(500, y_position, f"${producto['total']:.2f}")
        y_position -= 20

    p.line(100, y_position, 500, y_position)
    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=boleta.pdf'
    response.write(buffer.getvalue())
    return response
