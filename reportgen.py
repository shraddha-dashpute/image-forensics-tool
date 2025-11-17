# reportgen.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io

def generate_report(filename, original_pil, ela_pil, results):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, height - 40, "Image Forensic Report")
    c.setFont("Helvetica", 10)
    y = height - 70
    for k, v in results.items():
        c.drawString(40, y, f"{k}: {v}")
        y -= 14
        if y < 120:
            c.showPage()
            y = height - 40
    # Add images
    x = 40; y -= 20
    orig_buf = io.BytesIO()
    original_pil.save(orig_buf, format="PNG")
    orig_buf.seek(0)
    c.drawImage(ImageReader(orig_buf), x, y-200, width=250, height=200)
    ela_buf = io.BytesIO()
    ela_pil.save(ela_buf, format="PNG")
    ela_buf.seek(0)
    c.drawImage(ImageReader(ela_buf), x+270, y-200, width=250, height=200)
    c.save()
