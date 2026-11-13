
"""
MachFlow - PDF Report Generator
Generates a PDF report from simulation results.
"""

from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


def generate_pdf_report(result, checks, flow_type, inputs):

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm
    )

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="ReportTitle",
        parent=styles["Title"],
        fontSize=22,
        textColor=colors.HexColor("#12304A"),
        spaceAfter=12
    ))

    story = []

    # TITLE
    story.append(Paragraph(
        "MACHFLOW - DIFFUSER SIMULATOR",
        styles["ReportTitle"]
    ))

    story.append(Paragraph(
        "Engineering Simulation Report",
        styles["Heading2"]
    ))

    story.append(Spacer(1, 10))

    story.append(Paragraph(
        f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
        styles["Normal"]
    ))

    story.append(Spacer(1, 15))

    # PROJECT INFORMATION
    story.append(Paragraph(
        "1. PROJECT INFORMATION",
        styles["Heading2"]
    ))

    project_data = [
        ["Parameter", "Details"],
        ["Project", "MachFlow - Diffuser Simulator"],
        ["Author", "Not Specified"],
        ["Programme", "B.E. Aeronautical Engineering"],
        ["Diffuser Type", flow_type]
    ]

    table = Table(project_data, colWidths=[65*mm, 95*mm])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0),
         colors.HexColor("#12304A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
    ]))

    story.append(table)
    story.append(Spacer(1, 15))

    # INPUT PARAMETERS
    story.append(Paragraph(
        "2. SIMULATION INPUT PARAMETERS",
        styles["Heading2"]
    ))

    input_data = [
        ["Input", "Value"],
        ["Inlet Mach Number", str(inputs["inlet_mach"])],
        ["Area Ratio", str(inputs["area_ratio"])],
        ["Specific Heat Ratio", str(inputs["gamma"])]
    ]

    table = Table(input_data, colWidths=[65*mm, 95*mm])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0),
         colors.HexColor("#1F6E9A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8)
    ]))

    story.append(table)
    story.append(Spacer(1, 15))

    # CALCULATED RESULTS
    story.append(Paragraph(
        "3. CALCULATED ENGINEERING RESULTS",
        styles["Heading2"]
    ))

    result_data = [["Parameter", "Calculated Value"]]

    for key, value in result.items():

        if isinstance(value, float):
            value = f"{value:.6f}"

        result_data.append([str(key), str(value)])

    table = Table(result_data, colWidths=[90*mm, 70*mm])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0),
         colors.HexColor("#12304A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#EAF3F8")]),
        ("PADDING", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "TOP")
    ]))

    story.append(table)
    story.append(Spacer(1, 15))

    # VALIDATION
    story.append(Paragraph(
        "4. ENGINEERING VALIDATION",
        styles["Heading2"]
    ))

    validation_data = [["Validation Check", "Status"]]

    for description, passed in checks.items():
        validation_data.append([
            description,
            "PASS" if passed else "FAIL"
        ])

    table = Table(validation_data, colWidths=[120*mm, 40*mm])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0),
         colors.HexColor("#12304A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "TOP")
    ]))

    story.append(table)
    story.append(Spacer(1, 15))

    passed = sum(checks.values())
    total = len(checks)

    story.append(Paragraph(
        f"Validation Score: {passed}/{total}",
        styles["Heading3"]
    ))

    # LIMITATIONS
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "5. MODEL LIMITATIONS",
        styles["Heading2"]
    ))

    story.append(Paragraph(
        "This software uses idealized one-dimensional compressible-flow "
        "models. The supersonic diffuser model assumes a normal shock "
        "at the inlet followed by ideal subsonic diffusion. Friction, "
        "boundary-layer development, flow separation and shock "
        "interactions are not fully modelled. Results are intended "
        "for educational engineering analysis and are not certified "
        "design predictions.",
        styles["BodyText"]
    ))

    story.append(Spacer(1, 20))

    story.append(Paragraph(
        "Generated by MachFlow - Diffuser Simulator",
        styles["Italic"]
    ))

    document.build(story)

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes
