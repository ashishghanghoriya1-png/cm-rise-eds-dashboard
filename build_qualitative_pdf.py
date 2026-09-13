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
        self.drawString(50, 10.75*inch, "Deep Qualitative Free-Text Analysis | Education Development Study (EDS)")
        self.line(50, 42, 8.5*inch-50, 42)
        self.drawString(50, 28, "The Voice of the Teacher: Analysis of Open-Ended Responses")
        self.drawRightString(8.5*inch-50, 28, f"Page {self._pageNumber} of {total}")
        self.restoreState()

def build_pdf(filename="Deep_Qualitative_Research_Report.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=50, rightMargin=50, topMargin=50, bottomMargin=50)
    sty = getSampleStyleSheet()

    NAVY   = colors.HexColor("#1E3A8A")
    TEAL   = colors.HexColor("#0D9488")
    DARK   = colors.HexColor("#1E293B")
    MUTED  = colors.HexColor("#475569")
    LIGHT  = colors.HexColor("#F8FAFC")
    BOX_BG = colors.HexColor("#F0FDFA")
    BOX_BD = colors.HexColor("#99F6E4")

    T  = ParagraphStyle("T",  parent=sty["Heading1"], fontName="Helvetica-Bold", fontSize=22, leading=26, textColor=NAVY, spaceAfter=2)
    ST = ParagraphStyle("ST", parent=sty["Normal"], fontName="Helvetica", fontSize=11, leading=14, textColor=MUTED, spaceAfter=15)
    H2 = ParagraphStyle("H2", parent=sty["Heading2"], fontName="Helvetica-Bold", fontSize=14, leading=18, textColor=TEAL, spaceBefore=12, spaceAfter=6)
    B  = ParagraphStyle("B",  parent=sty["Normal"], fontName="Helvetica", fontSize=9.5, leading=14, textColor=DARK, spaceAfter=6)
    
    ITHindi = ParagraphStyle("ITHindi", parent=sty["Normal"], fontName=default_font, fontSize=9.5, leading=14, textColor=DARK, spaceAfter=6, leftIndent=10, rightIndent=10)
    IT = ParagraphStyle("IT", parent=sty["Normal"], fontName="Helvetica-Oblique", fontSize=9.5, leading=14, textColor=DARK, spaceAfter=6, leftIndent=10, rightIndent=10)

    def P(text, style): return Paragraph(text, style)

    s = []

    # TITLE
    s.append(P("The Voice of the Teacher", T))
    s.append(P("Deep Qualitative Free-Text Analysis", T))
    s.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=15))
    s.append(P("Synthesized from the 'Qual_FreeText' sheet comprising 58 open-ended response variables across 60 teachers.", ST))

    # Executive Summary Box
    exec_summary = (
        "<b>Overview:</b> While quantitative data tells us *what* is happening, the free-text responses tell us *why*. "
        "An analysis of the unprompted, open-ended responses from teachers reveals a workforce that possesses high intrinsic "
        "motivation but feels stifled by generalized, top-down mandates. Teachers are asking for hyper-localized training, "
        "peer-led problem-solving spaces, and realistic expectations regarding their classroom demographics."
    )
    box = Table([[P(exec_summary, B)]], colWidths=[7*inch])
    box.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),BOX_BG),
        ('BOX',(0,0),(-1,-1),1,BOX_BD),
        ('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10),
        ('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),
    ]))
    s.append(box)
    s.append(Spacer(1, 0.2*inch))

    # INSIGHT 1
    s.append(P("1. The Demand for Contextualization in Training", H2))
    s.append(P("<b>Insight:</b> Teachers feel that statewide, one-size-fits-all training modules fail to address the realities of rural or tribal classrooms. They are explicitly asking for Master Trainers (MTs) from their own geographies.", B))
    s.append(P("<b>Direct Quotes from Teachers:</b>", B))
    s.append(P("\"Select MTs from the more interior like tribal areas... there should be four groups based on the geographies and context. So, training should cater differently for all these groups based on their experiences.\"", IT))
    s.append(P("\"Real classroom demo video help to connect more during training.\"", IT))
    s.append(P("<b>Recommendation:</b> Restructure training cohorts not just by subject, but by geography or school typology (e.g., 'Multi-grade Tribal School Cohort' vs. 'Urban High-Enrollment Cohort').", B))
    s.append(Spacer(1, 0.1*inch))

    # INSIGHT 2
    s.append(P("2. CLSS as a 'Venting' and Problem-Solving Space", H2))
    s.append(P("<b>Insight:</b> Teachers are frustrated by top-down agendas during Cluster Level Sharing Sessions (CLSS). They want agency to discuss their localized, daily academic challenges with peers.", B))
    s.append(P("<b>Direct Quotes from Teachers:</b>", B))
    s.append(P("\"Half time should be pre-decided agenda on any subject but half time should be there for discussion teacher local academic challenges.\"", IT))
    s.append(P("\"दो चीज़ होनी चाहिए अच्छी बातचीत और सभी शिक्षकों को बोलने का मौका\" (There should be two things: good conversation and an opportunity for all teachers to speak).", ITHindi))
    s.append(P("\"At the block level official look at this activity as timepass, so People dont take training seriously.\"", IT))
    s.append(P("<b>Recommendation:</b> Mandate an 'Open Floor' structure for the second half of every CLSS where the pre-decided agenda is abandoned, allowing teachers to crowd-source solutions to local issues.", B))
    s.append(Spacer(1, 0.1*inch))

    # INSIGHT 3
    s.append(P("3. The Burden of Execution & Digital Pushback", H2))
    s.append(P("<b>Insight:</b> There is a polarizing view on digital training. While some want more, a vocal segment feels digital courses add no value and distract from core issues like staffing and syllabus overload.", B))
    s.append(P("<b>Direct Quotes from Teachers:</b>", B))
    s.append(P("\"Digital program needed more, except that teacher mainly highlighted his challenges as administrative challenges like staff need to be increase, remove workload, Syllabus need to in the more easy format.\"", IT))
    s.append(P("\"शिक्षकों के लिय स्टेट लेवल ट्रेंनिंग होना चाहिए, Digital कोर्स को बंद करना चाहिए ये शिक्षकों को कम फायदा पहुचता हैं.\" (State level training should be for teachers, Digital courses should be stopped as they benefit teachers less).", ITHindi))
    s.append(P("\"Low engagement of students (they not able to connect the topic), Low attendance, Lack of resources.\"", IT))
    s.append(P("<b>Recommendation:</b> Acknowledge administrative burdens before pushing digital adoption. Frame digital courses as time-saving tools rather than additional homework for teachers.", B))
    s.append(Spacer(1, 0.1*inch))

    # INSIGHT 4
    s.append(P("4. High Intrinsic Motivation (The Silver Lining)", H2))
    s.append(P("<b>Insight:</b> Despite structural challenges, the core motivation of teachers remains deeply intrinsic. They care about student outcomes, not just departmental compliance.", B))
    s.append(P("<b>Direct Quotes from Observers & Teachers:</b>", B))
    s.append(P("\"मैडम की बातों से यह स्पष्ट होता है कि उनकी प्रेरणा मुख्य रूप से आंतरिक है... उनका ध्यान प्रमाणपत्र या औपचारिक आवश्यकताओं से अधिक बच्चों के सीखने के परिणामों पर है।\" (It is clear that her motivation is intrinsic... her focus is on children's learning outcomes rather than certificates or formal requirements).", ITHindi))
    s.append(P("\"Teacher was intrinsically shown keen to learn, he is also working in the very interior of the balaghat. He engage students in multiple ways.\"", IT))
    s.append(P("<b>Recommendation:</b> Pivot the messaging of the CM RISE TPD programme. Stop using compliance threats (attendance, certificates) and start using outcome-based messaging ('This module will help your students grasp fractions faster').", B))

    doc.build(s, canvasmaker=NumberedCanvas)
    print(f"Generated '{filename}' successfully!")

build_pdf()
