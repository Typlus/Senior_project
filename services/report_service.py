import database
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from functions import get_result_by_id

fields = [
        ("Detection ID", "id"),
        ("Species", "species"),
        ("Filename", "filename"),
        ("Confidence", "confidence")
    ]


def generate_report(detection_id):
    detection = get_result_by_id(detection_id)

    if detection is None:
        return
    pdf = canvas.Canvas(f"report_{detection_id}.pdf")
    pdf.setFont("Times-Roman",18)
    pdf.drawString(100,750, "ImmersaVLM Detection Report")

    
    y = 700
    pdf.setFont("Helvetica", 12)

    for label, key in fields:
        pdf.drawString(100, y, f"{label}: {detection[key]}")
        y -= 20

    image_path = f"spectrograms/{detection['filename'].replace('.wav', '.png')}"

    pdf.drawImage(
        ImageReader(image_path),
        100,
        300,
        width=400,
        height=250,
        preserveAspectRatio=True
    )

    pdf.save()

import os

print(os.path.exists("spectrograms/dolphin001.png"))
