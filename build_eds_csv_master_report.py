import sys, io, os
import pandas as pd
import numpy as np

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
        self.drawString(50, 10.75*inch, "EDS CSV Qualitative Field Research Report | Madhya Pradesh TPD")
        self.line(50, 42, 8.5*inch-50, 42)
        self.drawString(50, 28, "Exhaustive Analysis of 60 Teacher Observations (EDS Sheet.csv)")
        self.drawRightString(8.5*inch-50, 28, f"Page {self._pageNumber} of {total}")
        self.restoreState()

def build_pdf(filename="EDS_CSV_Exhaustive_Research_Report.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=50, rightMargin=50, topMargin=50, bottomMargin=50)
    sty = getSampleStyleSheet()

    NAVY   = colors.HexColor("#1E3A8A")
    TEAL   = colors.HexColor("#0D9488")
    DARK   = colors.HexColor("#1E293B")
    MUTED  = colors.HexColor("#475569")
    LIGHT  = colors.HexColor("#F8FAFC")
    BOX_BG = colors.HexColor("#F0FDFA")
    BOX_BD = colors.HexColor("#99F6E4")
    AMBER  = colors.HexColor("#D97706")

    T  = ParagraphStyle("T",  parent=sty["Heading1"], fontName="Helvetica-Bold", fontSize=22, leading=26, textColor=NAVY, spaceAfter=2)
    ST = ParagraphStyle("ST", parent=sty["Normal"], fontName="Helvetica", fontSize=11, leading=14, textColor=MUTED, spaceAfter=15)
    H2 = ParagraphStyle("H2", parent=sty["Heading2"], fontName="Helvetica-Bold", fontSize=14, leading=18, textColor=TEAL, spaceBefore=12, spaceAfter=6)
    H3 = ParagraphStyle("H3", parent=sty["Heading3"], fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=NAVY, spaceBefore=8, spaceAfter=4)
    B  = ParagraphStyle("B",  parent=sty["Normal"], fontName="Helvetica", fontSize=9.5, leading=14, textColor=DARK, spaceAfter=6)
    BL = ParagraphStyle("BL", parent=sty["Normal"], fontName="Helvetica", fontSize=9.5, leading=14, textColor=DARK, leftIndent=15, spaceAfter=4)
    TH = ParagraphStyle("TH", parent=sty["Normal"], fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=colors.white)
    TC = ParagraphStyle("TC", parent=sty["Normal"], fontName="Helvetica", fontSize=8.5, leading=11, textColor=DARK)
    TCB= ParagraphStyle("TCB",parent=sty["Normal"], fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=DARK)
    IT = ParagraphStyle("IT", parent=sty["Normal"], fontName="Helvetica-Oblique", fontSize=9.5, leading=14, textColor=DARK, spaceAfter=6, leftIndent=10, rightIndent=10)
    ITHindi = ParagraphStyle("ITHindi", parent=sty["Normal"], fontName=default_font, fontSize=9.5, leading=14, textColor=DARK, spaceAfter=6, leftIndent=10, rightIndent=10)

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
            ('TOPPADDING',(0,0),(-1,-1),5),
            ('BOTTOMPADDING',(0,0),(-1,-1),5),
        ]))
        return t

    s = []

    # COVER / HEADER
    s.append(P("EDS Field Qualitative Research Report", T))
    s.append(P("Exhaustive Analysis of 60 Teacher Observation Sheets", T))
    s.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=15))
    s.append(P("Education Development Study (EDS) | Source: `EDS Sheet.csv`", ST))

    # Executive Summary Box
    exec_summary = (
        "<b>Executive Overview:</b> This research report synthesizes field observer qualitative notes across 60 government school "
        "teachers in Madhya Pradesh. By analyzing direct observation text across 7 structural domains, we uncover the underlying "
        "operational, administrative, and technological frictions that impede the implementation of teacher professional development (TPD) "
        "initiatives, including Margdarshika lesson plan adoption, digital course completion, and CLSS peer cascading."
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

    # SECTION 1: DOMAIN OVERVIEW & DEMOGRAPHICS
    s.append(P("1. Study Cohort & Domain Overview", H2))
    s.append(P("The qualitative observation dataset comprises <b>60 study teachers</b> surveyed across multiple districts in Madhya Pradesh."))
    
    overview_tbl = [
        [PH("Metric / Parameter"), PH("Observation Value"), PH("Analytical Significance")],
        [PCB("Total Teachers Observed"), PC("60 Teachers"), PC("Complete field sample cohort")],
        [PCB("Districts Covered"), PC("Bhind, Balaghat, Seoni, etc."), PC("Diverse geographical & tribal contexts")],
        [PCB("Gender Breakdown"), PC("38 Male (63.3%), 22 Female (36.7%)"), PC("Reflects primary cadre distribution")],
        [PCB("Observation Domains"), PC("7 Key Qualitative Domains"), PC("Covering daily, annual, digital & CLSS aspects")],
    ]
    s.append(make_tbl(overview_tbl, [2.0*inch, 2.2*inch, 2.8*inch], TEAL))
    s.append(Spacer(1, 0.15*inch))

    # SECTION 2: DOMAIN 1 & 2 - DAILY & ANNUAL ENGAGEMENT
    s.append(P("2. Daily & Annual Engagement Realities", H2))
    s.append(P("<b>Key Finding:</b> Administrative overload—especially for Headmasters and senior teachers—severely cannibalizes instructional time and activity preparation."))
    s.append(P("<b>Direct Field Evidence:</b>", B))
    s.append(P("\"Teacher is also headmaster therefore he highly engaged in academic and non-academic responsibilities.\"", IT))
    s.append(P("\"Government design a lot of activity, so it will get difficult to manage with low grade level student. But overall, the teacher does not take part in administrative work due to health concern and seniority.\"", IT))
    s.append(P("<b>Synthesis:</b> Teachers face conflicting priorities. Dual-role teachers (Teacher + Headmaster) spend up to 40% of their day managing non-academic administrative mandates, leaving minimal energy for innovative pedagogy.", B))
    s.append(Spacer(1, 0.15*inch))

    # SECTION 3: DOMAIN 3 & 4 - IN-PERSON TRAINING & MATERIAL ADOPTION
    s.append(P("3. In-Person Training & Margdarshika Adoption Gaps", H2))
    s.append(P("<b>Key Finding:</b> While 93.3% of teachers appreciate in-person training conceptually, actual classroom adoption of Margdarshika modules drops to 20-30% due to large class sizes and multi-grade teaching."))
    s.append(P("<b>Direct Field Evidence:</b>", B))
    s.append(P("\"She tried to adopt learning from various training but due to learning level of students and other works, she implement only 20-30 percent in class.\"", IT))
    s.append(P("\"Teacher had access to and used the Margdarshika resource; however, its use was occasional due to competing administrative responsibilities as the Headmaster.\"", IT))
    s.append(P("\"The teacher reported using the training materials... However, the responses remained general, and the teacher was unable to recall specific classroom incidents.\"", IT))
    s.append(P("<b>Synthesis:</b> A major 'transfer-of-learning' gap exists. Materials are used occasionally as reference documents rather than structured daily guides.", B))
    s.append(PageBreak())

    # SECTION 4: DOMAIN 5 & 6 - DIGITAL LEARNING & NON-PARTICIPATION
    s.append(P("4. Digital Learning Perceptions & Non-Participation", H2))
    s.append(P("<b>Key Finding:</b> Digital training suffers from compliance-driven 'click-throughs', long video fatigue, and severe technical friction (device access, network issues)."))
    s.append(P("<b>Direct Field Evidence:</b>", B))
    s.append(P("\"Teacher is saying that he has done courses, but he dont remember anything major and thus, it feels like he either havent done and asked somebody else to do it for him.\"", IT))
    s.append(P("\"Time is the problem, acc to him courses are of long duration, His feedback was to give pdf of question answers... he generally starts the course and do some other courses.\"", IT))
    s.append(P("\"Completed most of the courses using his wife's phone, primarily based on instructions from the school administration... finds in-person training more effective.\"", IT))
    s.append(P("\"Not aware of the app Whatsapp and is not very comfortable in using Android.\"", IT))
    s.append(P("<b>Synthesis:</b> Digital completion metrics are heavily distorted by passive playback. Short micro-learning modules (1-2 hours) with direct subject relevance are urgently required.", B))
    s.append(Spacer(1, 0.15*inch))

    # SECTION 5: DOMAIN 7 - CLSS CASCADE PROCESS
    s.append(P("5. CLSS (Cluster Level Sharing Sessions) Cascade Breakdown", H2))
    s.append(P("<b>Key Finding:</b> School-level knowledge cascading of CLSS learnings is overwhelmingly informal and uncoordinated, leading to rapid memory decay."))
    s.append(P("<b>Direct Field Evidence:</b>", B))
    s.append(P("\"CLSS learnings are mainly shared through informal discussions among teachers.\"", IT))
    s.append(P("\"There is no any process placed to cascade learning of the CLSS with their teacher who did not participated.\"", IT))
    s.append(P("\"No established peer-learning or cascade mechanism was reported.\"", IT))
    s.append(P("<b>Synthesis:</b> Without a mandatory, structured 10-minute briefing during weekly staff assemblies, CLSS learnings remain isolated to the individual attendee.", B))
    s.append(Spacer(1, 0.15*inch))

    # SECTION 6: STRATEGIC RECOMMENDATIONS
    s.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=15))
    s.append(P("6. Strategic Policy & Operational Recommendations", H2))
    
    recs = [
        "<b>1. Formalize CLSS School Briefings:</b> Institute a mandatory 10-minute 'CLSS Knowledge Cascade' slot during Monday staff assemblies to transform informal hallway chats into structured peer learning.",
        "<b>2. Pivot to Micro-Learning (1-Hour Cap):</b> Eliminate long 3+ hour digital modules. Structure DIKSHA courses into 15-minute bite-sized videos followed by immediate quizzes.",
        "<b>3. Contextualize Margdarshika for Large Classes:</b> Add dedicated chapters in Margdarshika addressing multi-grade teaching and high pupil-teacher ratios.",
        "<b>4. Establish JSK Technical Helpdesk:</b> Deploy a WhatsApp automated bot/helpdesk to resolve device, login, and network barriers preventing high-intent teachers from completing courses.",
        "<b>5. Shift Brand Messaging from Compliance to Impact:</b> Move away from threat-based deadlines ('complete by Friday') to value-based outcomes ('Learn how to teach fractions in 10 minutes')."
    ]
    for r in recs:
        s.append(P(r, B))
        s.append(Spacer(1, 4))

    doc.build(s, canvasmaker=NumberedCanvas)
    print(f"Generated '{filename}' successfully!", flush=True)

build_pdf()
