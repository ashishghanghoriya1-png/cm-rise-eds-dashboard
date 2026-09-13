import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

sys.stdout.reconfigure(encoding='utf-8')

pdf_filename = "EDS_Data_Audit_And_Mismatch_Report.pdf"
artifact_pdf_path = os.path.join(r"C:\Users\Peepul\.gemini\antigravity\brain\7bcfe871-9ab0-496a-9859-4a48c33122a1", pdf_filename)
local_pdf_path = os.path.join(r"c:\My Files Work\Gravity", pdf_filename)

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to add total page counts and header/footer"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#4A5568"))
        
        # Header (on pages after cover/page 1)
        if self._pageNumber > 1:
            self.drawString(54, 11 * inch - 36, "EDS Data Consolidation vs July Master Audit Report")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)
            
        # Footer (all pages)
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 36, page_text)
        self.drawString(54, 36, "Confidential — Educational Data Systems (EDS) Audit")
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(54, 48, 8.5 * inch - 54, 48)
        self.restoreState()

def create_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#1A365D"),
        spaceAfter=12
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#4A5568"),
        spaceAfter=20
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#2B6CB0"),
        spaceBefore=16,
        spaceAfter=10,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#2D3748"),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#2D3748"),
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.white,
        alignment=0
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#1A202C")
    )
    
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#1A202C")
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=body_style,
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#742A2A")
    )

    elements = []

    # Title Banner
    elements.append(Paragraph("EDS Data Discrepancy & Audit Report", title_style))
    elements.append(Paragraph("Reconciliation of <b>EDS_Full Data Table Consolidation_30 Aug.xlsx</b> vs <b>EDS_Cleaned_Master_2July.xlsx</b>", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#3182CE"), spaceAfter=15))

    # Executive Summary Box
    summary_html = """
    <b>EXECUTIVE SUMMARY</b><br/>
    An exhaustive cell-by-cell and column-by-column audit was conducted comparing the 30 August Consolidation workbook with the 2 July Cleaned Master dataset. 
    While key headline statistics (digital completion: 86.7%, IPT attendance: 93.3%, CLSS attendance: 88.3%) are consistent, critical structural flaws, missingness gaps, and logical row contradictions were identified in the master dataset.
    """
    summary_table = Table(
        [[Paragraph(summary_html, ParagraphStyle('SumText', parent=body_style, textColor=colors.HexColor("#1A365D"), fontSize=9.5, leading=14))]],
        colWidths=[504]
    )
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EBF8FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#3182CE")),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 15))

    # Section 1: Sample Size & Export Artifacts
    elements.append(Paragraph("1. Sample Size & Export Artifacts", h1_style))
    elements.append(Paragraph("The raw <b>Quant_Structured</b> sheet contains <b>75 rows</b> in Excel, creating a potential calculation baseline error if computed naively:", body_style))
    
    sample_data = [
        [Paragraph("Sheet Name", table_header_style), Paragraph("Raw Rows", table_header_style), Paragraph("Header Rows", table_header_style), Paragraph("Trailing Blank Rows", table_header_style), Paragraph("Valid Sample (N)", table_header_style)],
        [Paragraph("<b>Quant_Structured</b>", table_cell_style), Paragraph("75", table_cell_style), Paragraph("1 (Row 0)", table_cell_style), Paragraph("14 (Rows 61–74)", table_cell_style), Paragraph("<b>60 Teachers</b>", table_cell_bold)],
        [Paragraph("<b>Qual_FreeText</b>", table_cell_style), Paragraph("61", table_cell_style), Paragraph("1 (Row 0)", table_cell_style), Paragraph("0", table_cell_style), Paragraph("<b>60 Teachers</b>", table_cell_bold)],
        [Paragraph("<b>Obs_Observations</b>", table_cell_style), Paragraph("61", table_cell_style), Paragraph("1 (Row 0)", table_cell_style), Paragraph("0", table_cell_style), Paragraph("<b>60 Teachers</b>", table_cell_bold)],
    ]
    t_sample = Table(sample_data, colWidths=[130, 70, 90, 114, 100])
    t_sample.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2B6CB0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(t_sample)
    elements.append(Spacer(1, 15))

    # Section 2: Key Inaccuracies & Logical Contradictions
    elements.append(Paragraph("2. Internal Logical Contradictions in July Master File", h1_style))
    
    contradictions = [
        "<b>Teacher 38 CLSS Participation Contradiction</b>: Col 18 (<i>CLSS Flag</i>) is marked <b>1</b> (Participated), but Col 68 (<i>No. of CLSS Attended</i>) explicitly records <b>'Not Participated'</b>. This causes an attendee sum mismatch (53 vs 52).",
        "<b>Online Course Derivative Flag Contradiction</b>: Teachers 18, 26, 27, 28, 34, 44, 47, and 49 answered <i>No</i> for completing online courses (Col 37), but Col 96 records string <b>'0'</b> instead of remaining null.",
        "<b>Duplicate Header Rows</b>: Row 0 across <code>Quant_Structured</code>, <code>Qual_FreeText</code>, and <code>Obs_Observations</code> repeats string column headers as data values (<i>Teacher_ID = 'Teacher_ID'</i>).",
        "<b>Uncleaned Scratch Sheets</b>: <code>Sheet1</code> contains misspelled headers (<i>'Annual Enagement '</i>) and <code>Sheet2</code> contains raw unformatted pivot outputs."
    ]
    for c in contradictions:
        elements.append(Paragraph(f"• {c}", bullet_style))

    elements.append(Spacer(1, 15))

    # Section 3: High Missingness & Data Entry Gaps
    elements.append(Paragraph("3. High Field Missingness (Implicit vs Explicit Nulls)", h1_style))
    elements.append(Paragraph("High missingness in binary indicator columns indicates that enumerators skipped checkboxes when respondents replied 'No' or 'Unaware', rather than explicitly entering 0 or No:", body_style))

    gap_data = [
        [Paragraph("Column Name & Question", table_header_style), Paragraph("Total N", table_header_style), Paragraph("Non-Null Count", table_header_style), Paragraph("Missing (NaN)", table_header_style), Paragraph("Missing %", table_header_style)],
        [Paragraph("<b>Quant Col 62</b>: Knowledge of DIKSHA", table_cell_style), Paragraph("60", table_cell_style), Paragraph("23 Yes", table_cell_style), Paragraph("37 missing", table_cell_style), Paragraph("<b>61.7%</b>", table_cell_bold)],
        [Paragraph("<b>Quant Col 87</b>: Knowledge of CLSS Format", table_cell_style), Paragraph("60", table_cell_style), Paragraph("10 Yes, 3 No", table_cell_style), Paragraph("47 missing", table_cell_style), Paragraph("<b>78.3%</b>", table_cell_bold)],
        [Paragraph("<b>Quant Col 33</b>: Classroom Resource Application", table_cell_style), Paragraph("60", table_cell_style), Paragraph("38 answered", table_cell_style), Paragraph("22 missing", table_cell_style), Paragraph("<b>36.7%</b>", table_cell_bold)],
        [Paragraph("<b>Obs</b>: Material Access & Adoption Notes", table_cell_style), Paragraph("60", table_cell_style), Paragraph("32 answered", table_cell_style), Paragraph("28 missing", table_cell_style), Paragraph("<b>46.7%</b>", table_cell_bold)],
    ]
    t_gap = Table(gap_data, colWidths=[174, 50, 95, 95, 90])
    t_gap.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#C53030")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#FEB2B2")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#FFF5F5")]),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(t_gap)
    elements.append(Spacer(1, 15))

    # Page Break for Reconciliation Matrix
    elements.append(PageBreak())

    # Section 4: Cell-by-Cell Reconciliation Matrix
    elements.append(Paragraph("4. Cell-by-Cell Metric Reconciliation Matrix", h1_style))
    elements.append(Paragraph("Reconciliation of all key metrics in 30 Aug Consolidation against July Master dataset:", body_style))

    recon_data = [
        [Paragraph("Domain / Metric", table_header_style), Paragraph("30 Aug Claim", table_header_style), Paragraph("July Master Re-Calculated", table_header_style), Paragraph("Denominator", table_header_style), Paragraph("Status", table_header_style)],
        [Paragraph("Digital Course Completion", table_cell_style), Paragraph("52 / 60 (87%)", table_cell_style), Paragraph("52 / 60 (86.7%)", table_cell_style), Paragraph("N = 60", table_cell_style), Paragraph("<b>Match</b>", table_cell_bold)],
        [Paragraph("Timing: After School", table_cell_style), Paragraph("48 / 60 (80%)", table_cell_style), Paragraph("48 / 60 (80.0%)", table_cell_style), Paragraph("N = 60", table_cell_style), Paragraph("<b>Match</b>", table_cell_bold)],
        [Paragraph("Timing: During School", table_cell_style), Paragraph("22 / 60 (37%)", table_cell_style), Paragraph("22 / 60 (36.7%)", table_cell_style), Paragraph("N = 60", table_cell_style), Paragraph("<b>Match</b>", table_cell_bold)],
        [Paragraph("Subject Training Attendance", table_cell_style), Paragraph("56 / 60 (93%)", table_cell_style), Paragraph("56 / 60 (93.3%)", table_cell_style), Paragraph("N = 60", table_cell_style), Paragraph("<b>Match</b>", table_cell_bold)],
        [Paragraph("Training Modules Received", table_cell_style), Paragraph("36 teachers", table_cell_style), Paragraph("36 / 60 (60.0%)", table_cell_style), Paragraph("N = 60", table_cell_style), Paragraph("<b>Match</b>", table_cell_bold)],
        [Paragraph("IPT Materials: None Received", table_cell_style), Paragraph("19 teachers", table_cell_style), Paragraph("19 / 56 attendees (33.9%)", table_cell_style), Paragraph("N = 56", table_cell_style), Paragraph("<b>Match</b>", table_cell_bold)],
        [Paragraph("CLSS Attendance (1+ Session)", table_cell_style), Paragraph("53 / 60 (88%)", table_cell_style), Paragraph("53 / 60 (88.3%)", table_cell_style), Paragraph("N = 60", table_cell_style), Paragraph("<b>Match</b>", table_cell_bold)],
        [Paragraph("Attended All 5 CLSS Sessions", table_cell_style), Paragraph("20 / 53 (38%)", table_cell_style), Paragraph("20 / 53 (37.7%)", table_cell_style), Paragraph("N = 53", table_cell_style), Paragraph("<b>Match</b>", table_cell_bold)],
        [Paragraph("CLSS Solved Challenge", table_cell_style), Paragraph("32 / 60 (53%)", table_cell_style), Paragraph("32 / 60 (53.3%)", table_cell_style), Paragraph("N = 60", table_cell_style), Paragraph("<b>Match</b>", table_cell_bold)],
        [Paragraph("CLSS Topic Non-Recall", table_cell_style), Paragraph("18 reported", table_cell_style), Paragraph("<b>35 / 53 (66.0%)</b>", table_cell_bold), Paragraph("N = 53", table_cell_style), Paragraph("<font color='#DD6B20'><b>Recalibrated</b></font>", table_cell_style)],
    ]
    t_recon = Table(recon_data, colWidths=[140, 90, 134, 70, 70])
    t_recon.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2B6CB0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(t_recon)
    elements.append(Spacer(1, 15))

    # Section 5: Column Total & Denominator Analysis
    elements.append(Paragraph("5. Multi-Selection Column Totals & Denominators", h1_style))
    
    col_totals = [
        "<b>DIKSHA Engaging Features (Cols 43–49)</b>: 86 selections across 40 responding teachers (20 left section blank). Calculating % over N=40 (quizzes: 50.0%) vs N=60 (quizzes: 33.3%) creates a <b>16.7 percentage point mismatch</b>.",
        "<b>CLSS Attendance Form Friction (Cols 82–86)</b>: 66 selections across 53 CLSS attendees. Calculating % over N=53 vs N=60 creates a <b>7.5 percentage point shift</b>.",
        "<b>CLSS Topic Non-Recall Deficit (Cols 69–74)</b>: 18 teachers explicitly marked 'No recall', while 17 attendees left all topic checkboxes blank. Combined non-recall is <b>35 of 53 attendees (66.0%)</b>."
    ]
    for ct in col_totals:
        elements.append(Paragraph(f"• {ct}", bullet_style))

    elements.append(Spacer(1, 15))

    # Action Recommendations Box
    rec_html = """
    <b>RECOMMENDED CLEANING ACTIONS FOR JULY MASTER DATASET</b><br/>
    1. <b>Strip Trailing Rows</b>: Delete blank export rows 61–74 in <code>Quant_Structured</code> and drop string header row 0.<br/>
    2. <b>Resolve Teacher 38 Contradiction</b>: Reconcile CLSS flag (Col 18) and attendance count (Col 68).<br/>
    3. <b>Standardize Null Values</b>: Convert missing <code>NaN</code> values in binary awareness columns (Cols 62, 87) to explicit <code>0</code> (No).<br/>
    4. <b>Purge Scratch Sheets</b>: Remove uncleaned <code>Sheet1</code> and <code>Sheet2</code>.
    """
    rec_table = Table(
        [[Paragraph(rec_html, ParagraphStyle('RecText', parent=body_style, textColor=colors.HexColor("#22543D"), fontSize=9.5, leading=14))]],
        colWidths=[504]
    )
    rec_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0FFF4")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#38A169")),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    elements.append(rec_table)

    # Build PDF
    doc.build(elements, canvasmaker=NumberedCanvas)
    print(f"PDF successfully created at: {filename}")

if __name__ == '__main__':
    create_pdf(artifact_pdf_path)
    create_pdf(local_pdf_path)
