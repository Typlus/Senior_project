import database
from reportlab.pdfgen import canvas
from functions import get_result_by_id
from pathlib import Path

REPORT_DIR = Path(__file__).parent / "reports"
REPORT_DIR.mkdir(exist_ok=True)

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

    pdf_path = REPORT_DIR / f"report_{detection_id}.pdf"

    pdf = canvas.Canvas(str(pdf_path))
    pdf.setFont("Times-Roman", 18)
    pdf.drawString(100, 750, "ImmersaVLM Detection Report")

    y = 700
    pdf.setFont("Helvetica", 12)

    for label, key in fields:
        pdf.drawString(100, y, f"{label}: {detection[key]}")
        y -= 20

    image_path = (
        Path(__file__).parent
        / "spectrograms"
        / detection["filename"].replace(".wav", ".jpg")
    )

    print("IMAGE PATH:", image_path)
    print("IMAGE EXISTS:", image_path.exists())

    pdf.drawImage(
        str(image_path),
        100,
        300,
        width=400,
        height=250,
        preserveAspectRatio=True
    )

    pdf.save()

    print("PDF CREATED:", pdf_path)
