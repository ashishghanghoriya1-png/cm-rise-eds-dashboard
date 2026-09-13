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

# Register a font that supports Hindi/Devanagari characters
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
        self.drawString(50, 10.75*inch, "Qualitative Field Insights | Education Development Study (EDS)")
        self.line(50, 42, 8.5*inch-50, 42)
        self.drawString(50, 28, "Observation Sheet Analysis - Raw Field Notes")
        self.drawRightString(8.5*inch-50, 28, f"Page {self._pageNumber} of {total}")
        self.restoreState()

def build_pdf(filename="Observation_Field_Insights.pdf"):
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
    
    BHindi = ParagraphStyle("BHindi", parent=sty["Normal"], fontName=default_font, fontSize=9.5, leading=14, textColor=DARK, spaceAfter=6)
    IT = ParagraphStyle("IT", parent=sty["Normal"], fontName="Helvetica-Oblique", fontSize=9.5, leading=14, textColor=DARK, spaceAfter=6, leftIndent=10, rightIndent=10)
    ITHindi = ParagraphStyle("ITHindi", parent=sty["Normal"], fontName=default_font, fontSize=9.5, leading=14, textColor=DARK, spaceAfter=6, leftIndent=10, rightIndent=10)

    def P(text, style):
        return Paragraph(text, style)

    s = []

    # TITLE
    s.append(P("Qualitative Field Insights", T))
    s.append(P("Observation Sheet Analysis", T))
    s.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=15))
    s.append(P("Synthesized from field researchers' raw notes across 60 teacher observations.", ST))

    # Executive Summary Box
    exec_summary = (
        "<b>Overview:</b> Based on an analysis of the field researchers' raw free-text notes from the 'Obs_Observations' sheet, "
        "three distinct qualitative themes emerge regarding teacher behavior and program adoption. These field notes heavily "
        "corroborate the findings from the TabFM regression analysis, specifically highlighting operational barriers to lesson "
        "plan execution and digital training compliance."
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

    # THEME 1
    s.append(P("1. The 'Compliance vs. Engagement' Reality in Digital Learning", H2))
    s.append(P("<b>Observation:</b> Teachers are often clicking through digital courses strictly for compliance without absorbing the material.", B))
    s.append(P("<b>Direct Evidence from Field Observers:</b>", B))
    s.append(P("\"He just did the course without listening the content, he just share politically right answer.\"", IT))
    s.append(P("\"He generally starts the course and do some other work... His feedback was to give pdf of question answers.\"", IT))
    s.append(P("\"The teacher mentioned he does online courses only when he thinks it is important. On probing further... he mentioned that when multiple messages and reminders come and it gets mandated, then he will consider it important.\"", IT))
    s.append(P("<b>Insight:</b> Digital course completion metrics are likely inflated by 'click-through' compliance. Teachers view these courses as administrative hurdles mandated by persistent WhatsApp reminders rather than genuine professional development opportunities. Long course durations are the primary driver of this disengagement.", B))
    s.append(Spacer(1, 0.1*inch))

    # THEME 2
    s.append(P("2. Systemic Barriers to Classroom Translation", H2))
    s.append(P("<b>Observation:</b> Even when in-person training is well-received, translating it to the classroom is blocked by structural realities (student attendance, single-teacher schools, administrative load).", B))
    s.append(P("<b>Direct Evidence from Field Observers:</b>", B))
    s.append(P("\"उनके अनुसार ट्रेनिंग का 20% ही वो इंप्लीमेंट कर पाते है क्योंकि समय की कमी और administrative कार्य ज्यादा। साथ ही बच्चों की अनियमित उपस्थिति के कारण भी शिक्षक चीजों को नहीं कर पाते।\"", ITHindi))
    s.append(P("\"एकल शिक्षक होने के कारण सीख लागू नहीं होती।\"", ITHindi))
    s.append(P("\"She tried sometimes but due to strength of students and management of student, she was not doing it on a regular basis.\"", IT))
    s.append(P("<b>Insight:</b> The failure to execute lesson plans is not necessarily a pedagogical failure, but an operational one. Training modules are designed for an idealized classroom. When faced with massive class sizes, multi-grade teaching, or high absenteeism, the prescribed activities become impossible to manage.", B))
    s.append(Spacer(1, 0.1*inch))

    # THEME 3
    s.append(P("3. The Informal Cascade of CLSS Learnings", H2))
    s.append(P("<b>Observation:</b> CLSS knowledge transfer within schools is entirely informal, relying on casual conversations rather than structured meetings.", B))
    s.append(P("<b>Direct Evidence from Field Observers:</b>", B))
    s.append(P("\"शिक्षिका CLSS में प्राप्त सीख को विद्यालय स्तर पर सहकर्मी शिक्षकों के साथ अनौपचारिक चर्चा के माध्यम से साझा करती हैं... विद्यालय स्तर पर सीख के प्रसार (cascade) की कोई औपचारिक या संरचित व्यवस्था नहीं है।\"", ITHindi))
    s.append(P("\"CLSS learning was shared with both regular teachers and guest teachers... Through discussions, teachers exchanged ideas and solutions.\"", IT))
    s.append(P("<b>Insight:</b> While peer-to-peer learning is happening, it is highly dependent on individual teacher initiative. Without a formalized 10-minute slot in a staff meeting, the cascade of CLSS learnings is inconsistent and evaporates quickly after the training ends.", B))
    s.append(Spacer(1, 0.2*inch))

    # RECOMMENDATIONS
    s.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=15))
    s.append(P("Strategic Recommendations for Field Operations", H2))
    
    recs = [
        "<b>1. Redesign for the 'Realistic' Classroom:</b> Future training materials must include explicit modules on how to execute activities in challenging environments (e.g., 'How to run this activity with 60 students' or 'How to adapt this for a single-teacher school').",
        "<b>2. Audit Digital Course Formats:</b> Stop relying on course completion certificates as a metric for learning. If teachers are asking for 'just the PDF of answers' to get through the long videos, the videos are too long. Pivot to 3-minute micro-videos.",
        "<b>3. Formalize the Cascade:</b> Field teams and Jan Shikshaks (JSKs) must mandate that Headmasters schedule a formal 10-minute 'CLSS Debrief' at the weekly school assembly, transitioning the knowledge transfer from casual hallway chats to a structural requirement."
    ]
    
    for r in recs:
        s.append(P(r, B))
        s.append(Spacer(1, 4))

    doc.build(s, canvasmaker=NumberedCanvas)
    print(f"Generated '{filename}' successfully!")

build_pdf()
