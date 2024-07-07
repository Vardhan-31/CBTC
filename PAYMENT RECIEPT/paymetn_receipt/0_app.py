from flask import Flask, request, send_file, render_template
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
import io

app = Flask(__name__, template_folder='1_templates', static_folder='2_static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/receipt', methods=['POST'])
def generate_receipt():
    customer_name = request.form['customer_name']
    transaction_id = request.form['transaction_id']
    date = request.form['date']

    # Extract item details
    item_descriptions = request.form.getlist('item_description')
    quantities = request.form.getlist('quantity')
    unit_prices = request.form.getlist('unit_price')

    items = []
    total_amount = 0
    for description, quantity, unit_price in zip(item_descriptions, quantities, unit_prices):
        quantity = int(quantity)
        unit_price = float(unit_price)
        total = quantity * unit_price
        total_amount += total
        items.append([description, str(quantity), f"${unit_price:.2f}", f"${total:.2f}"])

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    title_style = styles['Title']
    subtitle_style = ParagraphStyle(name='Subtitle', fontSize=12, leading=14)
    normal_style = styles['Normal']

    elements.append(Paragraph("Transaction Receipt", title_style))
    elements.append(Paragraph(f"Date: {date}", subtitle_style))
    elements.append(Paragraph(f"Transaction ID: {transaction_id}", subtitle_style))
    elements.append(Paragraph(f"Customer Name: {customer_name}", subtitle_style))
    elements.append(Paragraph(f"Total Amount: ${total_amount:.2f}", subtitle_style))
    elements.append(Paragraph(" ", subtitle_style))

    data = [["Description", "Quantity", "Unit Price", "Total"]] + items
    data.append(["Total", "", "", f"${total_amount:.2f}"])

    table = Table(data, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)

    doc.build(elements)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name='receipt.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
