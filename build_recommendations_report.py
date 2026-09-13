import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak, ListFlowable, ListItem
)
from reportlab.pdfgen import canvas

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
        self.drawString(50, 10.75*inch, "Strategic Policy Recommendations | Education Development Study (EDS)")
        self.line(50, 42, 8.5*inch-50, 42)
        self.drawString(50, 28, "Data-Driven Recommendations Based on TabFM 60-Teacher Cohort Analysis")
        self.drawRightString(8.5*inch-50, 28, f"Page {self._pageNumber} of {total}")
        self.restoreState()

def build_pdf(filename="EDS_Policy_Recommendations.pdf"):
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
    RED    = colors.HexColor("#DC2626")

    T  = ParagraphStyle("T",  parent=sty["Heading1"], fontName="Helvetica-Bold", fontSize=22, leading=26, textColor=NAVY, spaceAfter=2)
    ST = ParagraphStyle("ST", parent=sty["Normal"], fontName="Helvetica", fontSize=11, leading=14, textColor=MUTED, spaceAfter=15)
    H2 = ParagraphStyle("H2", parent=sty["Heading2"], fontName="Helvetica-Bold", fontSize=14, leading=18, textColor=TEAL, spaceBefore=12, spaceAfter=6)
    H3 = ParagraphStyle("H3", parent=sty["Heading3"], fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=NAVY, spaceBefore=8, spaceAfter=4)
    B  = ParagraphStyle("B",  parent=sty["Normal"], fontName="Helvetica", fontSize=9.5, leading=14, textColor=DARK, spaceAfter=6)
    BL = ParagraphStyle("BL", parent=sty["Normal"], fontName="Helvetica", fontSize=9.5, leading=14, textColor=DARK, leftIndent=15, spaceAfter=4)
    TH = ParagraphStyle("TH", parent=sty["Normal"], fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=colors.white)
    TC = ParagraphStyle("TC", parent=sty["Normal"], fontName="Helvetica", fontSize=8.5, leading=11, textColor=DARK)
    TCB= ParagraphStyle("TCB",parent=sty["Normal"], fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=DARK)
    TCA= ParagraphStyle("TCA",parent=sty["Normal"], fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=RED)

    def make_tbl(data, widths, hdr_color=NAVY):
        t = Table(data, colWidths=widths)
        t.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),hdr_color),
            ('ALIGN',(0,0),(-1,-1),'LEFT'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('GRID',(0,0),(-1,-1),0.4,colors.HexColor("#CBD5E1")),
            ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,LIGHT]),
            ('TOPPADDING',(0,0),(-1,-1),6),
            ('BOTTOMPADDING',(0,0),(-1,-1),6),
        ]))
        return t

    def P(text, style=B): return Paragraph(text, style)
    def PH(text): return Paragraph(text, TH)
    def PC(text): return Paragraph(text, TC)
    def PCB(text): return Paragraph(text, TCB)
    def PCA(text): return Paragraph(text, TCA)

    s = []  # story

    # ═══════════════════════════════════════
    # TITLE
    # ═══════════════════════════════════════
    s.append(P("Data-Driven Policy & Intervention", T))
    s.append(P("Recommendations Report", T))
    s.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=15))
    s.append(P("Derived from the TabFM Zero-Shot Regression Analysis of 60 Teachers \u00d7 103 Features (July 2026)", ST))

    # Executive Summary Box
    exec_summary = (
        "<b>Executive Summary:</b> The recent comprehensive data imputation using TabFM regression revealed "
        "several critical gaps between teacher training and classroom execution. While theoretical buy-in "
        "and digital engagement are remarkably high, on-the-ground application of pedagogies (like lesson plans) "
        "and structural retention of CLSS workshops are lagging. The following recommendations are tailored "
        "to address these specific execution bottlenecks."
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

    # ═══════════════════════════════════════
    # ISSUE 1: THE EXECUTION GAP
    # ═══════════════════════════════════════
    s.append(P("1. Bridging the 'Training-to-Classroom' Execution Gap", H2))
    s.append(P("<b>The Data Reality:</b> 93.3% of teachers find in-person training useful, yet only 28.3% confidently apply the provided lesson plans/modules in the classroom. A staggering 50% are 'Not sure' if they are applying them correctly."))
    
    tbl1 = [
        [PH("Proposed Intervention"), PH("Target Audience"), PH("Expected Impact")],
        [PCB("In-Class Demonstration (Handholding)"), PC("The 50% 'Not Sure' cohort"), PC("Convert uncertainty to confidence through peer shadowing.")],
        [PCB("Simplified 'One-Pager' Lesson Plans"), PC("All teachers"), PC("Reduce cognitive load. Current modules are perceived as too complex.")],
        [PCB("JSK Application Audits"), PC("Low-application schools"), PC("Shift JSK focus from 'attendance' to 'classroom observation'.")]
    ]
    s.append(make_tbl(tbl1, [2.5*inch, 1.5*inch, 3*inch], TEAL))
    s.append(Spacer(1, 0.1*inch))
    
    s.append(P("<b>Actionable Next Step:</b> Launch a 'Micro-Teaching' pilot where Jan Shikshaks (JSKs) conduct 15-minute live demonstrations of the Margdarshika lesson plan during their school visits, rather than just delivering the manual.", BL))

    # ═══════════════════════════════════════
    # ISSUE 2: CLSS RECALL & CASCADE
    # ═══════════════════════════════════════
    s.append(P("2. Overhauling CLSS (Cluster Level Sharing Sessions) Retention", H2))
    s.append(P("<b>The Data Reality:</b> Despite 86.7% attendance, 43.3% of teachers could not recall a single topic from the CLSS. Furthermore, cascading knowledge back to the school relies heavily on unstructured 'verbal discussions' (23 teachers) or no process at all (18 teachers)."))
    
    tbl2 = [
        [PH("Proposed Intervention"), PH("Implementation Mechanism"), PH("Urgency")],
        [PCB("Standardized Visual Agenda Cards"), PC("Distribute printed 1-page visual summaries at the start of every CLSS."), PCA("High")],
        [PCB("Mandatory 5-Min School Assembly Brief"), PC("Require returning teachers to share 3 bullet points in morning assembly."), PCB("Medium")],
        [PCB("Gamified Recall via WhatsApp"), PC("JSK to send a 1-question quiz via WhatsApp 2 days post-CLSS."), PCB("Low / Experimental")]
    ]
    s.append(make_tbl(tbl2, [2.5*inch, 3.5*inch, 1*inch], NAVY))
    s.append(Spacer(1, 0.1*inch))

    s.append(P("<b>Actionable Next Step:</b> Require Headmasters (HMs) to allocate a dedicated 10-minute slot in the weekly staff meeting exclusively for the CLSS attendee to formally cascade learnings, replacing informal verbal chats.", BL))

    # ═══════════════════════════════════════
    # ISSUE 3: DIKSHA PLATFORM OPTIMIZATION
    # ═══════════════════════════════════════
    s.append(P("3. Optimizing DIKSHA Digital Course Delivery", H2))
    s.append(P("<b>The Data Reality:</b> 100% awareness and 85% completion rate. However, 'Not Aware' (35 mentions) of specific new courses and 'Technical Issues' (27 mentions) remain massive barriers. The most preferred duration is 2 hours, primarily done 'After School'. Interactive features (Quizzes: 30, Videos: 27) drive engagement."))
    
    tbl3 = [
        [PH("Insight"), PH("Current Strategy"), PH("Recommended Pivot")],
        [PC("Top Info Source: JSK WhatsApp (50 mentions)"), PC("Relying on dashboard / state portals"), PCB("Formalize JSK WhatsApp groups as the primary official broadcast channel.")],
        [PC("Preferred Timing: After School (47 mentions)"), PC("Assuming in-school completion"), PCB("Design courses to be downloaded offline during school Wi-Fi, completed at home.")],
        [PC("Best Features: Quizzes (30), Videos (27)"), PC("Text-heavy PDF resources (15)"), PCB("Pivot budget from text resources to interactive quizzes and short animations.")]
    ]
    s.append(make_tbl(tbl3, [2.2*inch, 2.2*inch, 2.6*inch], TEAL))
    s.append(Spacer(1, 0.1*inch))
    
    s.append(P("<b>Actionable Next Step:</b> Establish a centralized 'Tech Support Hotline' or WhatsApp chatbot to address the 'Technical Issues' barrier, which is currently preventing high-intent teachers from completing courses.", BL))
    
    s.append(PageBreak())

    # ═══════════════════════════════════════
    # ISSUE 4: RSK MP PORTAL ATTRITION
    # ═══════════════════════════════════════
    s.append(P("4. Fixing RSK MP Feedback / Attendance Drop-off", H2))
    s.append(P("<b>The Data Reality:</b> The biggest barrier to filling out the post-CLSS attendance/feedback form on RSK MP is the 'Session end rush for teachers to leave the venue' (14 mentions) and generalized 'other' frustrations (39 mentions)."))
    
    s.append(P("<b>Recommendations:</b>"))
    s.append(P("<b>\u2022 Dedicated Administrative Window:</b> Mandate that the final 15 minutes of every CLSS is a 'pencils down, phones out' silent period strictly for RSK MP form submission before anyone is allowed to leave.", BL))
    s.append(P("<b>\u2022 Offline Sync Capability:</b> Ensure the RSK MP form can be filled out offline and synced later, as network connectivity at rural cluster venues is often poor, contributing to the 'rush' and frustration.", BL))
    
    # ═══════════════════════════════════════
    # ISSUE 5: CM RISE BRANDING
    # ═══════════════════════════════════════
    s.append(Spacer(1, 0.2*inch))
    s.append(P("5. Establishing the CM RISE Brand Identity", H2))
    s.append(P("<b>The Data Reality:</b> There is a 65% 'Unbranded Activity Recall Gap'. Teachers are participating in activities, but unaided recall of the 'CM RISE' programme name is critically low (5%)."))
    
    s.append(P("<b>Recommendations:</b>"))
    s.append(P("<b>\u2022 Visual Unification:</b> Every piece of collateral (Margdarshika, DIKSHA course splash screens, CLSS banners, JSK WhatsApp posters) must carry a standardized, prominent CM RISE Teacher Professional Development logo.", BL))
    s.append(P("<b>\u2022 Nomenclature Shift:</b> Stop referring to activities generically (e.g., 'Digital Training'). Rebrand them internally and externally (e.g., 'CM RISE Digital Educator Module').", BL))

    # ═══════════════════════════════════════
    # CONCLUSION
    # ═══════════════════════════════════════
    s.append(Spacer(1, 0.4*inch))
    s.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=15))
    s.append(P("Conclusion & Strategic Priority", H2))
    s.append(P("The TabFM regression analysis proves that the Madhya Pradesh EDS cohort is not lacking in **willingness** or **attendance**. The primary friction points are **retention** (CLSS topics), **translation** (training to classroom application), and **technical friction** (DIKSHA/RSK MP)."))
    s.append(P("By shifting the focus from 'increasing attendance' to 'improving in-classroom execution and technical support', the CM RISE TPD programme can significantly amplify its impact on student learning outcomes."))

    doc.build(s, canvasmaker=NumberedCanvas)
    print(f"Generated '{filename}' successfully!")

build_pdf()
