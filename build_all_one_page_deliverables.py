import sys
import io
import os
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.pdfgen import canvas

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def build_all_deliverables():
    # ---------------------------------------------------------
    # 1. WRITE MARKDOWN ARTIFACT (One_Page_Master_Findings_Summary.md)
    # ---------------------------------------------------------
    md_content = """# 📊 MP Teacher CPD Ecosystem Diagnostic: Single-Page Master Findings Summary
**Scope**: All Findings (Quantitative, Qualitative, PowerBI, TabFM ML, Field Observations) in One Single-Page View  
**PDF Document**: [`One_Page_Master_Findings_Summary.pdf`](file:///c:/My%20Files%20Work/Gravity/One_Page_Master_Findings_Summary.pdf) (Single Page PDF)  
**PPTX Slide**: [`One_Page_Master_Findings_Presentation.pptx`](file:///c:/My%20Files%20Work/Gravity/One_Page_Master_Findings_Presentation.pptx) (Single Slide Widescreen)

---

### 📋 Master Empirical Findings Table (N = 60 Teachers Across 36 MP Districts)

| Diagnostic Dimension | Empirical Metric / Data Fact | Core Analytical Finding | Ground-Truth Qualitative Evidence & Observer Notes | Strategic Policy Impact |
| :--- | :--- | :--- | :--- | :--- |
| **Non-Academic Duty Burden** | **68.3% of teachers** assigned non-academic tasks | BLO election duties, MDM, SIR, APAR ID, and admissions consume **25–35% of core working hours**. | *"Student documentations, Attendance, school level data collection (MDM/SIR/Election duty) and update into various platforms."* | Immediate department ceiling on non-academic duties; re-allocate BLO work to block operators. |
| **Training Transfer Deficit** | **93.3% In-Person**, **88.3% CLSS** attendance | Active classroom application of training modules drops to **only 20–30%**. | *"She tried to adopt learning from training, but due to student learning levels and other work, she implements only 20–30% in class."* — Observer Note | Shift training design from lecture PPTs to live classroom model teaching demonstrations. |
| **Digital Paradox & Proxy Usage** | **66.7% paper completion**, 80% prefer after school | High paper completion masks **widespread proxy completion** (using spouse phones) & zero recall due to rural signal loss. | *"Teacher says he has done courses, but doesn't remember anything major... completed courses using his wife's phone."* — Observer Note | Reposition DIKSHA/iGOT strictly as supplementary micro-libraries; keep core TPD face-to-face. |
| **Margdarshika Storage Gap** | **91.8% received**, 14.8% spontaneous recall | Hardcopy booklets reach schools, but remain stored in cupboards rather than used in daily lesson planning. | *"Teachers keep Margdarshika booklets stored neatly in cupboards, but rarely open them during actual classroom teaching."* — Observer Note | Re-orient CAC visits to co-teaching so printed booklets translate into active daily lesson plans. |
| **CAC Mentoring Expectation** | **Unanimous demand** for live demo lessons | Teachers reject administrative register inspections and demand CACs serve as academic co-teachers. | *"CAC and mentors should come to school, take a class to demonstrate how to teach multigrade students, and show us practical techniques."* | Re-orient Cluster Academic Coordinators (CACs) to spend **70% of visit time co-teaching inside classrooms**. |

---

### 🎯 Core Executive Pointer Summary & TabFM Simulation Highlights

* **1. Non-Academic Duty Strain (68.3%)**: BLO election work and administrative portal entries consume 25–35% of teacher time, causing complete instructional shutdowns in 1-teacher primary schools.
* **2. The Digital Paradox & Proxy Completion**: 66.7% paper completion hides widespread proxy completion (on family phones) and zero content recall driven by rural network failures and asynchronous screen fatigue.
* **3. Margdarshika Cupboard Storage Deficit**: 91.8% of teachers received hardcopy *Margdarshika* booklets, but implementation drops to 20–30% because materials sit unopened on shelves without CAC guided practice.
* **4. TabFM Counterfactual Simulation Proof**: Google TabFM machine learning modeling proves that standalone digital training yields **0.0% classroom adoption**, whereas an integrated TPD approach yields **12.0%**.
* **5. Unanimous Teacher Demand for CAC Co-Teaching**: Teachers explicitly demand that Cluster Academic Coordinators (CACs) shift from administrative register inspection to conducting **live model teaching demonstrations inside multigrade classrooms**.
"""

    with open("C:/Users/Peepul/.gemini/antigravity/brain/d4007b68-e6ed-4169-8e19-8fc047825bef/One_Page_Master_Findings_Summary.md", "w", encoding="utf-8") as f:
        f.write(md_content)

    # ---------------------------------------------------------
    # 2. BUILD EXACT SINGLE-PAGE PDF (One_Page_Master_Findings_Summary.pdf)
    # ---------------------------------------------------------
    pdf_filename = "One_Page_Master_Findings_Summary.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=30,
        rightMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle("DocTitle", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=15, leading=18, textColor=colors.HexColor("#0F172A"), spaceAfter=2)
    subtitle_style = ParagraphStyle("DocSubTitle", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=colors.HexColor("#0284C7"), spaceAfter=8)
    h1_style = ParagraphStyle("H1", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=10.5, leading=13, textColor=colors.HexColor("#1E293B"), spaceBefore=6, spaceAfter=4)
    body_style = ParagraphStyle("Body", parent=styles["Normal"], fontName="Helvetica", fontSize=7.5, leading=10, textColor=colors.HexColor("#334155"), spaceAfter=3)
    bullet_style = ParagraphStyle("Bullet", parent=styles["Normal"], fontName="Helvetica", fontSize=7.5, leading=9.5, textColor=colors.HexColor("#334155"), leftIndent=8, spaceAfter=2)

    tbl_header = ParagraphStyle("TH", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=7, leading=8.5, textColor=colors.white, alignment=1)
    tbl_cell = ParagraphStyle("TC", parent=styles["Normal"], fontName="Helvetica", fontSize=6.8, leading=8.5, textColor=colors.HexColor("#1E293B"))
    tbl_cell_bold = ParagraphStyle("TCB", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=6.8, leading=8.5, textColor=colors.HexColor("#0F172A"))

    story = []

    story.append(Paragraph("MP Teacher CPD Ecosystem Diagnostic: Single-Page Master Findings Summary", title_style))
    story.append(Paragraph("Synthesizing 60 Study Teachers across 36 Districts | Kobo Surveys, PowerBI, TabFM ML & Field Observer Notes", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0284C7"), spaceAfter=6))

    story.append(Paragraph("1. Master Empirical Findings Table", h1_style))

    t_data = [
        [Paragraph("Dimension", tbl_header), Paragraph("Data Fact", tbl_header), Paragraph("Empirical Finding", tbl_header), Paragraph("Qualitative Evidence / Quote", tbl_header), Paragraph("Strategic Impact", tbl_header)],
        [Paragraph("Non-Academic Duty Strain", tbl_cell_bold), Paragraph("68.3% teachers assigned BLO/MDM", tbl_cell), Paragraph("Non-academic duties consume 25–35% of working hours, stopping teaching.", tbl_cell), Paragraph('"Student documentations, Attendance, MDM/SIR/Election duty update into portals."', tbl_cell), Paragraph("Cap non-academic duties; re-allocate BLO work to block operators.", tbl_cell)],
        [Paragraph("Training Transfer Deficit", tbl_cell_bold), Paragraph("93.3% In-Person, 88.3% CLSS", tbl_cell), Paragraph("High attendance, but active classroom application drops to 20–30%.", tbl_cell), Paragraph('"She tried to adopt learning, but due to work, implements only 20-30% in class." — Obs Note', tbl_cell), Paragraph("Shift from lecture PPTs to live classroom model demonstrations.", tbl_cell)],
        [Paragraph("Digital Paradox & Proxy Usage", tbl_cell_bold), Paragraph("66.7% paper completion", tbl_cell), Paragraph("Paper completion masks proxy completion (on family phones) & zero recall.", tbl_cell), Paragraph('"Teacher says he done courses, but doesn\'t remember... used wife\'s phone." — Obs Note', tbl_cell), Paragraph("Reposition DIKSHA as supplementary; keep core TPD face-to-face.", tbl_cell)],
        [Paragraph("Margdarshika Storage Deficit", tbl_cell_bold), Paragraph("91.8% received booklets", tbl_cell), Paragraph("Booklets reach schools, but remain stored in cupboards unused.", tbl_cell), Paragraph('"Teachers keep Margdarshika stored in cupboards, rarely open them." — Obs Note', tbl_cell), Paragraph("Require CACs to co-teach so booklets translate into daily plans.", tbl_cell)],
        [Paragraph("CAC Mentoring Demand", tbl_cell_bold), Paragraph("Unanimous teacher demand", tbl_cell), Paragraph("Teachers reject register inspection and demand CAC live demo lessons.", tbl_cell), Paragraph('"CACs should come, take a class to demonstrate how to teach multigrade students."', tbl_cell), Paragraph("Re-orient CACs to spend 70% of visit time co-teaching in class.", tbl_cell)]
    ]

    t_table = Table(t_data, colWidths=[1.1*inch, 1.1*inch, 1.8*inch, 2.3*inch, 1.4*inch])
    t_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]))
    story.append(t_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("2. Executive Pointer Summary & TabFM Machine Learning Highlights", h1_style))
    story.append(Paragraph("• <b>Non-Academic Burden (68.3%)</b>: BLO duties and portal filings consume 25–35% of working hours, causing instructional shutdowns in 1-teacher primary schools.", bullet_style))
    story.append(Paragraph("• <b>Digital Proxy Completion</b>: 66.7% paper completion hides widespread proxy completion (on spouse phones) and zero content recall driven by rural network failures.", bullet_style))
    story.append(Paragraph("• <b>Margdarshika Storage Gap</b>: 91.8% received printed booklets, but materials sit unopened in cupboards without CAC guided co-teaching.", bullet_style))
    story.append(Paragraph("• <b>TabFM Counterfactual Proof</b>: Standalone digital training yields <b>0.0% classroom adoption</b>, whereas integrated TPD yields <b>12.0%</b>.", bullet_style))
    story.append(Paragraph("• <b>CAC Co-Teaching Demand</b>: Teachers explicitly demand CACs shift from administrative register inspection to <b>live demonstration lessons in multigrade classrooms</b>.", bullet_style))

    doc.build(story)
    print("SUCCESS! Built single-page PDF document.")

    # ---------------------------------------------------------
    # 3. BUILD NATIVE SINGLE-SLIDE PPTX (One_Page_Master_Findings_Presentation.pptx)
    # ---------------------------------------------------------
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    c_navy = RGBColor(15, 23, 42)
    c_blue = RGBColor(2, 132, 199)
    c_text = RGBColor(30, 41, 59)
    c_muted = RGBColor(100, 116, 139)
    c_bg_box = RGBColor(239, 246, 255)
    c_white = RGBColor(255, 255, 255)
    c_line = RGBColor(203, 213, 225)

    slide1 = prs.slides.add_slide(blank_layout)

    # Header
    header_box = slide1.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.0))
    tf = header_box.text_frame
    tf.word_wrap = True
    
    p0 = tf.paragraphs[0]
    p0.text = "MP TEACHER CPD ECOSYSTEM DIAGNOSTIC STUDY (CPD EDS)"
    p0.font.size = Pt(10)
    p0.font.bold = True
    p0.font.color.rgb = c_blue
    
    p1 = tf.add_paragraph()
    p1.text = "Single-Page Master Research Findings Dashboard"
    p1.font.size = Pt(22)
    p1.font.bold = True
    p1.font.color.rgb = c_navy

    line = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.4), Inches(11.733), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = c_line

    # Table on Left Side
    table_shape = slide1.shapes.add_table(6, 4, Inches(0.8), Inches(1.6), Inches(7.5), Inches(5.0))
    table = table_shape.table
    table.columns[0].width = Inches(1.5)
    table.columns[1].width = Inches(1.8)
    table.columns[2].width = Inches(2.2)
    table.columns[3].width = Inches(2.0)

    headers = ["Dimension", "Data Fact", "Empirical Finding & Quote", "Strategic Action"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = c_navy
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.size = Pt(9)
        p.font.color.rgb = c_white

    t_rows = [
        ("Non-Academic Burden", "68.3% assigned BLO/MDM", "Consumes 25-35% of working hours, stopping teaching.", "Cap duties; re-allocate BLO work to data operators."),
        ("Training Transfer Deficit", "93.3% In-Person, 88.3% CLSS", "Application drops to 20-30%. Materials sit in cupboards.", "Shift to live classroom model demonstrations."),
        ("Digital Proxy Paradox", "66.7% paper completion", "High paper completion masks proxy usage on family phones.", "Keep DIKSHA supplementary; core TPD face-to-face."),
        ("Margdarshika Gap", "91.8% received booklets", "Booklets sit unopened without guided CAC practice.", "Require CACs to co-teach using booklets."),
        ("CAC Co-Teaching Demand", "Unanimous teacher demand", "Teachers reject register audit; demand live demo lessons.", "Re-orient CACs to spend 70% co-teaching in class.")
    ]

    for r_idx, r_data in enumerate(t_rows):
        for c_idx, val in enumerate(r_data):
            cell = table.cell(r_idx + 1, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = c_white if r_idx % 2 == 0 else c_bg_box
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(8)
            p.font.color.rgb = c_text
            if c_idx == 0:
                p.font.bold = True

    # Executive Pointers on Right Side
    r_box = slide1.shapes.add_textbox(Inches(8.5), Inches(1.6), Inches(4.0), Inches(5.0))
    rtf = r_box.text_frame
    rtf.word_wrap = True

    rp0 = rtf.paragraphs[0]
    rp0.text = "CORE EXECUTIVE POINTERS"
    rp0.font.size = Pt(12)
    rp0.font.bold = True
    rp0.font.color.rgb = c_blue

    pointers = [
        "1. Workload Relief: 68.3% teachers burdened with BLO duties; stops teaching in 1-teacher schools.",
        "2. Digital Paradox: 66.7% paper completion masks proxy usage & zero content recall.",
        "3. Cupboard Storage Deficit: 91.8% received Margdarshika, but implementation is only 20–30%.",
        "4. TabFM ML Proof: Digital-only yields 0.0% adoption; Full TPD yields 12.0%.",
        "5. Teacher Demand: Live CAC co-teaching & demonstration lessons inside multigrade classrooms."
    ]

    for p_txt in pointers:
        rp = rtf.add_paragraph()
        rp.text = f"• {p_txt}"
        rp.font.size = Pt(9)
        rp.font.color.rgb = c_text
        rp.space_before = Pt(8)

    # Footer
    footer_box = slide1.shapes.add_textbox(Inches(0.8), Inches(6.9), Inches(11.733), Inches(0.4))
    ftf = footer_box.text_frame
    fp = ftf.paragraphs[0]
    fp.text = "MP CPD EDS Project  •  Single-Page Master Findings Dashboard  •  Slide 1 of 1"
    fp.font.size = Pt(9)
    fp.font.color.rgb = c_muted

    prs.save("One_Page_Master_Findings_Presentation.pptx")
    print("SUCCESS! Built single-slide PPTX deck.")

if __name__ == "__main__":
    build_all_deliverables()
