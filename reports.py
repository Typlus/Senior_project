
from reportlab.pdfgen import canvas
from io import BytesIO
from pathlib import Path
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
        return None

    # Create PDF in memory
    buffer = BytesIO()

    pdf = canvas.Canvas(buffer)

    pdf.setFont("Times-Roman", 18)
    pdf.drawString(100, 750, "ImmersaVLM Detection Report")

    y = 700
    pdf.setFont("Helvetica", 12)

    for label, key in fields:
        pdf.drawString(100, y, f"{label}: {detection[key]}")
        y -= 20

    # Find spectrogram
    image_path = (
        Path(__file__).parent
        / "spectrograms"
        / detection["filename"].replace(".wav", ".jpg")
    )

    if image_path.exists():
        pdf.drawImage(
            str(image_path),
            100,
            300,
            width=400,
            height=250,
            preserveAspectRatio=True
        )

    pdf.save()

    # Move to beginning of file
    buffer.seek(0)

    return buffer.getvalue()
