import sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
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
        self.drawString(50, 10.75*inch, "Strategic TPD Improvement Roadmap & Action Plan | CM RISE Madhya Pradesh")
        self.line(50, 42, 8.5*inch-50, 42)
        self.drawString(50, 28, "Integrated Analysis: Power BI, TabFM AI Predictions & Field Observations")
        self.drawRightString(8.5*inch-50, 28, f"Page {self._pageNumber} of {total}")
        self.restoreState()

def build_pdf(filename="Strategic_TPD_Improvement_Roadmap.pdf"):
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
    s.append(P("STRATEGIC TPD IMPROVEMENT ROADMAP", T))
    s.append(P("Evidence-Based Action Plan for CM RISE Professional Development", T))
    s.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=12))
    s.append(P("Synthesized from Power BI Analytics, TabFM AI Simulations & Field Research", ST))

    # Summary Box
    exec_summary = (
        "<b>Executive Synthesis:</b> By integrating findings from the 4-page Power BI dashboard, TabFM Classifier predictions, "
        "and qualitative observer logs across 60 study teachers (<b>56 Subject Training, 53 CLSS, 52 Digital Training</b>), "
        "this report provides a 5-pillar strategic roadmap to eliminate operational bottlenecks, boost digital completion to 100%, "
        "and double classroom lesson plan execution."
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

    # PILLAR 1
    s.append(P("1. Pillar 1: Closing the Awareness-to-Adoption Funnel Gap", H2))
    s.append(P("<b>Diagnostic Finding:</b> Official awareness is low at 38.3% (23/60), yet digital participation reaches 86.7% (52/60) when links are pushed via WhatsApp."))
    s.append(P("<b>Current Bottleneck:</b> Teachers rely on informal WhatsApp postings (26.9%) or direct instructions (47.8%) rather than searching web portals.", B))
    s.append(P("<b>Strategic Solution:</b> Transition from passive web portal announcements to 1-click WhatsApp Broadcast Cards with embedded course links. Make WhatsApp the official broadcast channel for RSK/TPD updates.", B))
    s.append(Spacer(1, 0.12*inch))

    # PILLAR 2
    s.append(P("2. Pillar 2: Micro-Learning Architecture for Digital Courses", H2))
    s.append(P("<b>Diagnostic Finding:</b> 80% (48 teachers) prefer learning at home after school, and 30% request a 2-hour max window. Long 3-hour videos cause severe time fatigue (27.8%) and passive background playback."))
    s.append(P("<b>Direct Field Evidence:</b> <i>\"He generally starts the course and do some other work... His feedback was to give pdf of question answers.\"</i>", IT))
    s.append(P("<b>Strategic Solution:</b> Re-architect DIKSHA courses into 15-minute animated micro-learning modules. Follow every video immediately with a 2-question checkpoint quiz to validate active engagement.", B))
    s.append(Spacer(1, 0.12*inch))

    # PILLAR 3
    s.append(P("3. Pillar 3: Re-engineering CLSS for High Retention & Cascading", H2))
    s.append(P("<b>Diagnostic Finding:</b> 34.0% of CLSS participants recall NO topic, and 28.3% share ZERO learnings upon returning to school."))
    s.append(P("<b>Strategic Solution:</b> Mandate a formal 10-minute 'CLSS Debrief' during Monday morning staff assemblies. Supply returning teachers with a 1-page visual summary card to brief non-attending peers.", B))
    s.append(PageBreak())

    # PILLAR 4
    s.append(P("4. Pillar 4: Margdarshika Redesign for Multi-Grade Classrooms", H2))
    s.append(P("<b>Diagnostic Finding:</b> Subject Training has the highest utility (92.9%), but 31.7% of teachers never received Margdarshika books. Those who did only execute 20-30% of activities due to multi-grade classroom strain."))
    s.append(P("<b>Direct Field Evidence:</b> <i>\"एकल शिक्षक होने के कारण सीख लागू नहीं होती... class strength makes regular implementation difficult.\"</i>", ITHindi))
    s.append(P("<b>Strategic Solution:</b> Add explicit 'Multi-Grade Classroom Adaptations' in Margdarshika manuals (e.g., instructions on managing Grades 3-5 in one room). Audit logistics to ensure 100% physical delivery.", B))
    s.append(Spacer(1, 0.12*inch))

    # PILLAR 5
    s.append(P("5. Pillar 5: Multi-Channel Training Bundles (TabFM AI Proof)", H2))
    s.append(P("<b>Diagnostic Finding:</b> Google TabFM Classifier proves that standalone digital training has lower impact. Combining <b>Subject Training + Digital Micro-Learning + CLSS</b> pushes digital completion to <b>100% (60/60)</b> and eliminates memory decay."))
    s.append(P("<b>Strategic Solution:</b> Require Jan Shikshaks (JSKs) to bundle interventions: every teacher completing a digital module is automatically assigned a CLSS peer discussion slot.", B))
    s.append(Spacer(1, 0.15*inch))

    # ACTION MATRIX TABLE
    s.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=10))
    s.append(P("6. Complete Implementation Action Matrix", H2))

    act_tbl = [
        [PH("Pillar / Area"), PH("Current Bottleneck"), PH("Immediate Tactical Action"), PH("Owner"), PH("Target KPI")],
        [PCB("1. Awareness"), PC("38.3% awareness rate"), PC("Deploy 1-click WhatsApp Broadcast Cards"), PC("TPD Comms"), PC("90% Awareness")],
        [PCB("2. Digital Courses"), PC("Passive playback / 27.8% fatigue"), PC("Pivot to 15-min animated micro-videos"), PC("Digital Content"), PC("100% Completion")],
        [PCB("3. CLSS Cascade"), PC("34% topic forgetfulness"), PC("Mandate 10-min Monday assembly debrief"), PC("Headmasters / JSK"), PC("80% Cascade")],
        [PCB("4. Margdarshika"), PC("31.7% non-receipt / multi-grade"), PC("Multi-grade activity redesign & audit"), PC("Academic Team"), PC("100% Receipt")],
        [PCB("5. AI Bundling"), PC("Isolated intervention silos"), PC("Bundle Subject + Digital + CLSS via JSK"), PC("District DIET"), PC("81.7% Adoption")],
    ]
    s.append(make_tbl(act_tbl, [1.1*inch, 1.6*inch, 2.1*inch, 1.0*inch, 1.2*inch], TEAL))

    doc.build(s, canvasmaker=NumberedCanvas)
    print(f"Generated '{filename}' successfully!", flush=True)

build_pdf()
