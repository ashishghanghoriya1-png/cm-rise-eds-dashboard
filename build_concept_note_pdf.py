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
        self.drawString(50, 10.75*inch, "Concept Note: Qualitative Research Study | CM RISE TPD Program")
        self.line(50, 42, 8.5*inch-50, 42)
        self.drawString(50, 28, "Education Development Study (EDS) | Madhya Pradesh")
        self.drawRightString(8.5*inch-50, 28, f"Page {self._pageNumber} of {total}")
        self.restoreState()

def build_pdf(filename="Qualitative_Research_Concept_Note.pdf"):
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
    s.append(P("CONCEPT NOTE: QUALITATIVE RESEARCH STUDY", T))
    s.append(P("Unpacking Operational Friction & Pedagogical Translation in CM RISE TPD", T))
    s.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=12))
    s.append(P("State Education Department & RSK Madhya Pradesh | Technical Partner: Peepul / TPD Unit", ST))

    # Executive Summary Box
    exec_summary = (
        "<b>Executive Summary & Study Rationale:</b> While quantitative evaluations and AI foundation models (Google TabFM) "
        "have mapped baseline participation across 60 study teachers (<b>56 Subject Training, 53 CLSS, 52 Digital Training</b>), "
        "there remains a critical knowledge gap regarding <i>why</i> classroom lesson plan application lags behind attendance. "
        "This concept note outlines a rigorous qualitative research design to investigate the lived experiences, operational bottlenecks, "
        "and agency of government school teachers in translating professional development into daily classroom practice."
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

    # SECTION 1: RESEARCH OBJECTIVES & KEY RESEARCH QUESTIONS
    s.append(P("1. Research Objectives & Key Research Questions (RQs)", H2))
    s.append(P("The qualitative study is structured around three primary inquiry pillars:"))
    
    rq_tbl = [
        [PH("Inquiry Pillar"), PH("Primary Qualitative Research Question (RQ)"), PH("Target Focus Area")],
        [PCB("1. Pedagogical Translation"), PC("RQ1: Why do teachers report executing only 20-30% of Margdarshika lesson plan modules in their classrooms despite high training satisfaction?"), PC("Classroom realities: multi-grade teaching, large class sizes & pupil-teacher ratios")],
        [PCB("2. Digital Engagement"), PC("RQ2: What drives the gap between digital course completion (52/60) and actual content retention / active learning?"), PC("Compliance-driven playback, video duration fatigue & mobile device sharing")],
        [PCB("3. Peer Cascading"), PC("RQ3: How can informal hallway conversations following CLSS sessions be institutionalized into structured school briefings?"), PC("CLSS mechanics, Headmaster leadership & Jan Shikshak (JSK) facilitation")],
    ]
    s.append(make_tbl(rq_tbl, [1.5*inch, 3.7*inch, 1.8*inch], TEAL))
    s.append(Spacer(1, 0.15*inch))

    # SECTION 2: METHODOLOGY & SAMPLING DESIGN
    s.append(P("2. Qualitative Methodology & Sampling Framework", H2))
    s.append(P("A <b>mixed-methods qualitative approach</b> combining grounded theory with contextual inquiry across 60 study teachers in Madhya Pradesh."))
    
    s.append(P("<b>Sampling Strategy:</b> Stratified Purposive Sampling across 4 geographic clusters:"))
    s.append(P("• <b>Cluster A (Tribal / Remote):</b> Interior schools in Balaghat & Seoni with single-teacher or multi-grade setups.", BL))
    s.append(P("• <b>Cluster B (High-Enrollment Urban):</b> Schools with >50 pupils per classroom in Bhind & district headquarters.", BL))
    s.append(P("• <b>Cluster C (High Digital Adopters):</b> Teachers completing >3 DIKSHA modules per term.", BL))
    s.append(P("• <b>Cluster D (CLSS Champions):</b> Teachers actively facilitating peer discussions during CLSS sessions.", BL))
    s.append(Spacer(1, 0.1*inch))

    s.append(P("<b>Data Collection Instruments:</b>", H3))
    inst_tbl = [
        [PH("Instrument"), PH("Sample Size"), PH("Methodological Objective")],
        [PCB("In-Depth Interviews (IDIs)"), PC("30 Teachers"), PC("Unpack individual motivation, time allocation & administrative friction")],
        [PCB("Focus Group Discussions (FGDs)"), PC("6 Groups (36 Teachers)"), PC("Analyze peer-learning dynamics and CLSS cascade opportunities")],
        [PCB("Classroom Observation Protocols (CRO)"), PC("20 Classroom Visits"), PC("Validate direct application of Margdarshika activities")],
        [PCB("Key Informant Interviews (KIIs)"), PC("10 JSKs & Block Officials"), PC("Assess administrative support & monitoring mechanics")],
    ]
    s.append(make_tbl(inst_tbl, [2.2*inch, 1.6*inch, 3.2*inch]))
    s.append(PageBreak())

    # SECTION 3: THEORETICAL & ANALYTICAL FRAMEWORK
    s.append(P("3. Theoretical Grounding & Analytical Pipeline", H2))
    s.append(P("<b>Conceptual Framework:</b> The study applies the <i>Teacher Agency & Systemic Friction Model</i>. It evaluates how teacher intrinsic motivation interacts with external operational constraints (administrative duties, device access, syllabus timelines)."))
    
    s.append(P("<b>AI-Assisted CAQDAS Pipeline:</b>", H3))
    s.append(P("1. <b>Transcription & Anonymization:</b> Audio recordings transcribed and scrubbed for PII.", BL))
    s.append(P("2. <b>Thematic Coding Rubric:</b> Dual-tier inductive (emergent notes) and deductive (RQ-aligned) coding using Dovetail / MAXQDA.", BL))
    s.append(P("3. <b>Local LLM Synthesis:</b> Querying local <b>Qwen2.5:14B</b> via Ollama to synthesize multi-transcript themes while maintaining strict data privacy.", BL))
    s.append(Spacer(1, 0.15*inch))

    # SECTION 4: EXPECTED DELIVERABLES & POLICY TIMELINE
    s.append(P("4. Deliverables & Policy Implementation Roadmap", H2))
    
    deliv_tbl = [
        [PH("Phase / Milestone"), PH("Key Output / Deliverable"), PH("Target Date"), PH("Policy Impact")],
        [PCB("Phase 1: Tool Finalization"), PC("Validated IDI, FGD & CRO Field Guides"), PC("Month 1"), PC("Standardized field observation")],
        [PCB("Phase 2: Field Data Collection"), PC("30 IDIs, 6 FGDs, 20 CRO Field Logs"), PC("Month 2"), PC("Empirical qualitative evidence")],
        [PCB("Phase 3: Coding & Analysis"), PC("Qualitative Evidence Matrix & Qwen 14B Synthesis"), PC("Month 3"), PC("Thematic identification")],
        [PCB("Phase 4: Policy Brief & Report"), PC("State Policy Report & Executive Deck for RSK"), PC("Month 4"), PC("TPD Program Refinement")],
    ]
    s.append(make_tbl(deliv_tbl, [1.6*inch, 2.6*inch, 1.1*inch, 1.7*inch], TEAL))
    s.append(Spacer(1, 0.2*inch))

    # SECTION 5: RECOMMENDATIONS FOR RESEARCH GOVERNANCE
    s.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=12))
    s.append(P("5. Strategic Recommendations for Research Governance", H2))
    
    recs = [
        "<b>1. Embed Qualitative Feedback Loops in JSK Reviews:</b> Transition JSK monitoring visits from compliance checklists to qualitative mentoring debriefs.",
        "<b>2. Co-Design Modules with Remote Teachers:</b> Involve teachers from single-teacher schools in Balaghat/Seoni to co-design realistic classroom activity adaptations.",
        "<b>3. Establish a State Qualitative Research Repository:</b> Archive qualitative transcripts in a local Dovetail / Ollama repository to enable continuous longitudinal inquiry."
    ]
    for r in recs:
        s.append(P(r, B))
        s.append(Spacer(1, 3))

    doc.build(s, canvasmaker=NumberedCanvas)
    print(f"Generated '{filename}' successfully!", flush=True)

build_pdf()
