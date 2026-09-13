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
        self.drawString(50, 10.75*inch, "Core Qualitative Field Transcripts Analysis | CM RISE TPD Study")
        self.line(50, 42, 8.5*inch-50, 42)
        self.drawString(50, 28, "Exhaustive Inspection of 4 Detailed Field Interview Transcripts")
        self.drawRightString(8.5*inch-50, 28, f"Page {self._pageNumber} of {total}")
        self.restoreState()

def build_pdf(filename="Core_Field_Transcripts_Exhaustive_Analysis.pdf"):
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
    s.append(P("CORE QUALITATIVE FIELD TRANSCRIPTS ANALYSIS", T))
    s.append(P("Exhaustive Synthesis of 4 Primary Handwritten Field Interview Logs", T))
    s.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=12))
    s.append(P("Field In-Depth Interview Analysis | CM RISE TPD Evaluation", ST))

    # Executive Summary Box
    exec_summary = (
        "<b>Executive Summary:</b> This report presents a complete, line-by-line qualitative analysis of the 4 core handwritten "
        "field interview transcripts conducted across Madhya Pradesh (Balaghat, Paraswada, Betul, and Satna/Jawa). "
        "It details the lived realities of teachers regarding daily period load, non-academic duties, digital network friction, "
        "CLSS peer-learning dynamics, and officer mentoring expectations."
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

    # TRANSCRIPT 1: KRISHNA KUMAR KUSHWAHA
    s.append(P("1. Transcript 1: Krishna Kumar Kushwaha (Balaghat, 25+ Yrs Exp, Science)", H2))
    s.append(P("<b>Context & Workload:</b> Teaches Science; takes 6 periods/day. Travels from Balaghat (10:00–10:40 AM). Manages MDM supervision, e-Attendance, BLO/Election duty, and National-level Yoga activities."))
    s.append(P("<b>Training & Materials Feedback:</b> Margdarshika Science charts are effective, but textbooks lack intermediate questions. Training manuals must be provided <i>during</i> session to retain visual concepts."))
    s.append(P("<b>Digital & Network Friction:</b> Rural network loading timeouts cause disengagement. At home, household chores intervene. Recommends offline download features and 1-click WhatsApp course links."))
    s.append(P("<b>Direct Field Quote:</b>", B))
    s.append(P("\"ग्रामीण क्षेत्र में नेटवर्क नहीं रहता, प्रशिक्षण लोड (loading) होता रहता है... ऐसा करें कि बिना Internet चले, Download का feature आये।\"", ITHindi))
    s.append(P("\"अधिकारियों का रवैया सकारात्मक होना चाहिए, डर या अनुशासन की दृष्टि से न आए, सलाहकार के रूप में आएं।\"", ITHindi))
    s.append(Spacer(1, 0.12*inch))

    # TRANSCRIPT 2: C.K. BHATIA
    s.append(P("2. Transcript 2: C.K. Bhatia / Chhatra Kumar (Paraswada, 37 Yrs Exp, Social Science)", H2))
    s.append(P("<b>Context & Health Strain:</b> Senior teacher (37 yrs exp, sugar/diabetes). Teaches Social Science; takes 4 periods/day."))
    s.append(P("<b>Critique of Block Training:</b> Calls block training a 'formality/timepass'. Criticizes urban Master Trainers (MTs) who do not understand interior tribal realities. Recommends MTs be selected from interior tribal blocks."))
    s.append(P("<b>Network & CLSS Friction:</b> Zero mobile network in school. Session feedback forms are filled at home due to network failure. Requests topics be announced 4 days in advance."))
    s.append(P("<b>Direct Field Quote:</b>", B))
    s.append(P("\"ब्लॉक स्तर पर टाइमपास नहीं होना चाहिए... MTs मास्टर स्तर वाले उठाए जाएं जो इंटीरियर ट्राइबल क्षेत्र के हों।\"", ITHindi))
    s.append(P("\"स्कूल में completely नेटवर्क नहीं रहता है... RSK MP पोर्टल फॉर्म जल्दबाजी में नहीं कर पाते, घर जाकर भरते हैं।\"", ITHindi))
    s.append(PageBreak())

    # TRANSCRIPT 3: RAJESH SOLANKI
    s.append(P("3. Transcript 3: Rajesh Solanki (Betul / Ambada, 25 Yrs Exp, Hindi)", H2))
    s.append(P("<b>Context & Classroom Reality:</b> Teaches Hindi; takes 6 periods/day. Manages APAAR ID mapping, registers, and student hygiene during lunch."))
    s.append(P("<b>Pedagogical Challenge:</b> High disparity between textbook grade levels and student actual learning levels (students in Grade 6/7 reading at Grade 2 level)."))
    s.append(P("<b>Digital & CLSS Feedback:</b> Watches videos at home after 4:00 PM (2-3 hrs/week). Finds CLSS discussion on student behavior useful. Notes that feedback forms are skipped due to forgetting or perceived irrelevance."))
    s.append(P("<b>Direct Field Quote:</b>", B))
    s.append(P("\"पाठ्यक्रम textbook और grade में अंतर मिलता है... छात्रों का स्तर अलग-अलग होता है, वह भी एक चुनौती है।\"", ITHindi))
    s.append(P("\"फॉर्म भरने में रिस्पांस नहीं... भूल गए या महत्वपूर्ण नहीं समझा।\"", ITHindi))
    s.append(Spacer(1, 0.12*inch))

    # TRANSCRIPT 4: BHAGAMLAL SINGH
    s.append(P("4. Transcript 4: Bhagamlal Singh / Jawa (Satna, 19 Yrs Exp, Maths & Science)", H2))
    s.append(P("<b>Context & Administrative Burden:</b> Teaches Maths & Science; takes 7 periods/day (40 min each). Non-academic duties (MDM, BLO, Census) consume 30-40% of time, leaving zero time for lesson prep."))
    s.append(P("<b>Training & Digital Needs:</b> Needs working projectors and TLM materials. Prefers short 30-minute videos split into 4 parts. Requests offline video downloads."))
    s.append(P("<b>Staff Cascade Recommendation:</b> Recommends a <b>One-Pager Summary</b> for staff rooms so non-attending teachers can quickly catch up on CLSS learnings."))
    s.append(P("<b>Direct Field Quote:</b>", B))
    s.append(P("\"30-40% समय प्रशासनिक कार्य में जाता है... केवल क्लासरूम में engage कर सकते हैं, properly subject पढ़ा नहीं पाते।\"", ITHindi))
    s.append(P("\"CLSS के लिए One-Pager Summary मिले ताकि staff room में दूसरे शिक्षक उपयोग कर सकें।\"", ITHindi))
    s.append(Spacer(1, 0.15*inch))

    # COMPARATIVE SUMMARY TABLE
    s.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=10))
    s.append(P("5. Cross-Transcript Comparative Findings Table", H2))

    comp_tbl = [
        [PH("Teacher Name / Location"), PH("Exp & Subject"), PH("Primary Non-Academic Load"), PH("Digital & CLSS Barrier"), PH("Key Policy Recommendation")],
        [PCB("Krishna Kumar (Balaghat)"), PC("25+ Yrs, Science"), PC("MDM, e-Attendance, Yoga"), PC("School network loading timeout"), PC("Offline downloadable videos & WhatsApp links")],
        [PCB("C.K. Bhatia (Paraswada)"), PC("37 Yrs, Social Sci"), PC("Health issues, Admin duties"), PC("Zero network in school, urban MTs"), PC("Appoint interior tribal MTs & small batches")],
        [PCB("Rajesh Solanki (Betul)"), PC("25 Yrs, Hindi"), PC("APAAR ID, Lunch registers"), PC("Grade level disparity in kids"), PC("Differentiated learning modules for kids")],
        [PCB("Bhagamlal Singh (Satna)"), PC("19 Yrs, Maths/Sci"), PC("30-40% MDM/BLO/Census"), PC("Portal feedback form rush"), PC("Staff room One-Pager Summary cards")],
    ]
    s.append(make_tbl(comp_tbl, [1.4*inch, 1.1*inch, 1.3*inch, 1.5*inch, 1.7*inch], TEAL))

    doc.build(s, canvasmaker=NumberedCanvas)
    print(f"Generated '{filename}' successfully!", flush=True)

build_pdf()
