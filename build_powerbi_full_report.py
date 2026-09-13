import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak, Image
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Hindi font
try:
    pdfmetrics.registerFont(TTFont('Nirmala', 'Nirmala.ttf'))
    default_font = 'Nirmala'
except:
    try:
        pdfmetrics.registerFont(TTFont('Mangal', 'mangal.ttf'))
        default_font = 'Mangal'
    except:
        default_font = 'Helvetica'

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved = []
    def showPage(self):
        self._saved.append(dict(self.__dict__))
        self._startPage()
    def save(self):
        total = len(self._saved)
        for s in self._saved:
            self.__dict__.update(s)
            self._draw(total)
            super().showPage()
        super().save()
    def _draw(self, total):
        self.saveState()
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.4)
        self.line(50, 10.7*inch, 8.5*inch-50, 10.7*inch)
        self.drawString(50, 10.75*inch, "Microsoft Power BI Dashboard Analysis Report | CM RISE TPD")
        self.line(50, 42, 8.5*inch-50, 42)
        self.drawString(50, 28, "Exhaustive Inspection of 4 Dashboard Pages (N=60 Teachers)")
        self.drawRightString(8.5*inch-50, 28, f"Page {self._pageNumber} of {total}")
        self.restoreState()

def build_pdf(filename="PowerBI_Dashboard_Comprehensive_Report.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=50, rightMargin=50, topMargin=50, bottomMargin=50)
    sty = getSampleStyleSheet()

    NAVY   = colors.HexColor("#1E3A8A")
    TEAL   = colors.HexColor("#0D9488")
    DARK   = colors.HexColor("#1E293B")
    MUTED  = colors.HexColor("#475569")
    LIGHT  = colors.HexColor("#F8FAFC")
    BOX_BG = colors.HexColor("#F0FDFA")
    BOX_BD = colors.HexColor("#99F6E4")

    T  = ParagraphStyle("T",  parent=sty["Heading1"], fontName="Helvetica-Bold", fontSize=20, leading=24, textColor=NAVY, spaceAfter=2)
    ST = ParagraphStyle("ST", parent=sty["Normal"], fontName="Helvetica", fontSize=10.5, leading=14, textColor=MUTED, spaceAfter=12)
    H2 = ParagraphStyle("H2", parent=sty["Heading2"], fontName="Helvetica-Bold", fontSize=13, leading=17, textColor=TEAL, spaceBefore=10, spaceAfter=4)
    H3 = ParagraphStyle("H3", parent=sty["Heading3"], fontName="Helvetica-Bold", fontSize=10.5, leading=13, textColor=NAVY, spaceBefore=6, spaceAfter=3)
    B  = ParagraphStyle("B",  parent=sty["Normal"], fontName="Helvetica", fontSize=9, leading=13, textColor=DARK, spaceAfter=5)
    BL = ParagraphStyle("BL", parent=sty["Normal"], fontName="Helvetica", fontSize=9, leading=13, textColor=DARK, leftIndent=12, spaceAfter=3)
    TH = ParagraphStyle("TH", parent=sty["Normal"], fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=colors.white)
    TC = ParagraphStyle("TC", parent=sty["Normal"], fontName="Helvetica", fontSize=8.5, leading=11, textColor=DARK)
    TCB= ParagraphStyle("TCB",parent=sty["Normal"], fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=DARK)
    IT = ParagraphStyle("IT", parent=sty["Normal"], fontName="Helvetica-Oblique", fontSize=9, leading=13, textColor=DARK, spaceAfter=5, leftIndent=10, rightIndent=10)
    ITHindi = ParagraphStyle("ITHindi", parent=sty["Normal"], fontName=default_font, fontSize=9, leading=13, textColor=DARK, spaceAfter=5, leftIndent=10, rightIndent=10)

    def P(text, style=B): return Paragraph(text, style)
    def PH(text): return Paragraph(text, TH)
    def PC(text): return Paragraph(text, TC)
    def PCB(text): return Paragraph(text, TCB)

    def make_tbl(data, widths, hdr_color=NAVY):
        t = Table(data, colWidths=widths)
        t.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),hdr_color),
            ('ALIGN',(0,0),(-1,-1),'LEFT'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('GRID',(0,0),(-1,-1),0.4,colors.HexColor("#CBD5E1")),
            ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,LIGHT]),
            ('TOPPADDING',(0,0),(-1,-1),4),
            ('BOTTOMPADDING',(0,0),(-1,-1),4),
        ]))
        return t

    s = []

    # TITLE & HEADER
    s.append(P("POWER BI DASHBOARD ANALYSIS REPORT", T))
    s.append(P("Comprehensive Inspection Across All 4 Pages (N=60 Study Teachers)", T))
    s.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=12))
    s.append(P("Published Power BI Report URL Analysis | CM RISE TPD Evaluation", ST))

    # Executive Summary Box
    exec_summary = (
        "<b>Executive Overview:</b> This report presents an exhaustive inspection of the 4-page Power BI dashboard "
        "(<i>Overview, Digital Course, CLSS, and Filler</i>) rendered via Playwright automation. "
        "It synthesizes ground-truth participation metrics, perceived utility rates, awareness funnel breakdowns, "
        "and critical execution barriers across 60 government school teachers in Madhya Pradesh."
    )
    box = Table([[P(exec_summary, B)]], colWidths=[7*inch])
    box.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),BOX_BG),
        ('BOX',(0,0),(-1,-1),1,BOX_BD),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
    ]))
    s.append(box)
    s.append(Spacer(1, 0.15*inch))

    # PAGE 1: OVERVIEW
    s.append(P("1. Page 1: Overview & Baseline Demographics", H2))
    s.append(P("The Overview page captures cohort demographics, intervention participation rates, and resource distribution."))
    
    img1 = r"C:\Users\Peepul\.gemini\antigravity\brain\f3d36a05-31c4-4ca8-978f-d6e3730b02aa\powerbi_tab1_overview.png"
    if os.path.exists(img1):
        s.append(Image(img1, width=6.8*inch, height=3.2*inch))
        s.append(Spacer(1, 0.1*inch))

    ov_tbl = [
        [PH("Intervention Channel"), PH("Participated Count"), PH("Perceived Useful Count"), PH("Utility Efficiency Rate (%)")],
        [PCB("Subject Training"), PC("56 / 60 (93.3%)"), PC("52 Teachers"), PCB("92.9% (Highest Utility)")],
        [PCB("CLSS Workshops"), PC("53 / 60 (88.3%)"), PC("32 Teachers"), PC("60.4%")],
        [PCB("Digital Training"), PC("52 / 60 (86.7%)"), PC("38 Teachers"), PC("73.1%")],
        [PCB("YouTube Training (YTL)"), PC("21 / 60 (35.0%)"), PC("16 Teachers"), PC("76.2%")],
        [PCB("SKG (Sheekh ki Yatra)"), PC("6 / 60 (10.0%)"), PC("6 Teachers"), PC("100.0%")],
        [PCB("WEBEX Meetings"), PC("1 / 60 (1.7%)"), PC("1 Teacher"), PC("100.0%")],
    ]
    s.append(make_tbl(ov_tbl, [2.2*inch, 1.6*inch, 1.6*inch, 1.6*inch], TEAL))
    s.append(Spacer(1, 0.15*inch))

    # PAGE 2: DIGITAL COURSE
    s.append(P("2. Page 2: Digital Course Adoption & Friction Points", H2))
    s.append(P("<b>Awareness Gap:</b> Only <b>23 out of 60 teachers (38.3%)</b> are actively aware of digital training initiatives, yet <b>52 teachers (86.7%)</b> participate when prompted via WhatsApp."))

    img2 = r"C:\Users\Peepul\.gemini\antigravity\brain\f3d36a05-31c4-4ca8-978f-d6e3730b02aa\powerbi_tab2_digital_course.png"
    if os.path.exists(img2):
        s.append(Image(img2, width=6.8*inch, height=3.2*inch))
        s.append(Spacer(1, 0.1*inch))

    digi_tbl = [
        [PH("Digital Metric"), PH("Power BI Value"), PH("Key Operational Insight")],
        [PCB("Preferred Timing"), PC("48 Teachers (80.0%) After School"), PC("Teachers do not learn during school hours due to classroom load.")],
        [PCB("Available Time Window"), PC("18 Teachers (30.0%) prefer 2 Hours"), PC("2 hours is the optimal maximum completion threshold.")],
        [PCB("Platform Usage"), PC("DIKSHA (40), iGOT (30), Both (24)"), PC("Platform fragmentation exists; DIKSHA is the dominant channel.")],
        [PCB("Most Engaging Content"), PC("Quizzes/Assessments (35.9%), Animated Videos (23.3%)"), PC("Teachers prefer short visual/interactive content over long PDFs.")],
        [PCB("Primary Barriers"), PC("Time Constraints (27.8%), Tech Issues (22.2%)"), PC("Network, device sharing & video length cause disengagement.")],
    ]
    s.append(make_tbl(digi_tbl, [1.8*inch, 2.4*inch, 2.8*inch]))
    s.append(PageBreak())

    # PAGE 3: CLSS
    s.append(P("3. Page 3: CLSS (Cluster Level Sharing Sessions) Breakdown", H2))
    s.append(P("<b>Participation vs Utility:</b> 53 teachers participated, but only 32 found it useful (60.4% utility rate). <b>34.0% failed to recall any specific topic</b>."))

    img3 = r"C:\Users\Peepul\.gemini\antigravity\brain\f3d36a05-31c4-4ca8-978f-d6e3730b02aa\powerbi_tab3_clss.png"
    if os.path.exists(img3):
        s.append(Image(img3, width=6.8*inch, height=3.2*inch))
        s.append(Spacer(1, 0.1*inch))

    clss_tbl = [
        [PH("CLSS Dimension"), PH("Power BI Finding"), PH("Strategic Action Required")],
        [PCB("Topic Recall Deficit"), PC("18 Teachers (34.0%) recalled NO topic"), PC("Reinforce sessions with post-meeting 1-page WhatsApp summary cards.")],
        [PCB("Top Recalled Topics"), PC("Classroom Management (14), Homework (11)"), PC("Focus future CLSS sessions on practical classroom management.")],
        [PCB("School Cascade Process"), PC("20 Verbally Share, 15 Share NO Process"), PC("Mandate 10-min Monday assembly briefing slot for attendees.")],
        [PCB("Attendance Form Barriers"), PC("Session End Rush (18.2%), Unwilling (12.1%)"), PC("Provide 1-click WhatsApp attendance forms instead of long URLs.")],
    ]
    s.append(make_tbl(clss_tbl, [1.8*inch, 2.4*inch, 2.8*inch], TEAL))
    s.append(Spacer(1, 0.15*inch))

    # PAGE 4: FILLER
    s.append(P("4. Page 4: Filler / Awareness Funnel Deep Dive", H2))
    s.append(P("<b>Unaided vs Aided Program Recall:</b> 13 teachers recall interventions without knowing the official programme name, while only 1 teacher has unaided recall of full programme details."))

    img4 = r"C:\Users\Peepul\.gemini\antigravity\brain\f3d36a05-31c4-4ca8-978f-d6e3730b02aa\powerbi_tab4_filler.png"
    if os.path.exists(img4):
        s.append(Image(img4, width=6.8*inch, height=2.2*inch))
        s.append(Spacer(1, 0.1*inch))

    # STRATEGIC RECOMMENDATIONS
    s.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=10))
    s.append(P("5. Strategic Recommendations Based on Power BI Inspection", H2))

    recs = [
        "<b>1. Capitalize on WhatsApp Broadcasts:</b> 47.8% of teachers get course info from direct links and 26.9% from WhatsApp. Stop relying on passive web portals; push 1-click links directly to WhatsApp groups.",
        "<b>2. Micro-Video Architecture:</b> Since 80% learn at home after school and prefer 2-hour windows, break courses into 15-minute animated modules.",
        "<b>3. Formalize the CLSS Cascade:</b> 28.3% of teachers share zero CLSS learnings upon return. Institute a 10-minute mandatory Monday assembly debrief slot."
    ]
    for r in recs:
        s.append(P(r, B))
        s.append(Spacer(1, 3))

    doc.build(s, canvasmaker=NumberedCanvas)
    print(f"Generated '{filename}' successfully!", flush=True)

build_pdf()
