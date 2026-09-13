import sys
import io
import os
import pandas as pd
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def build_findings_deck():
    # 1. Write Markdown Artifact
    md_content = """# 📊 Comprehensive Research Findings Presentation Deck (CPD EDS)
**Dataset & Reports Analyzed**: `EDS_Cleaned_Master_2July.xlsx`, `Empirical_CPD_EDS_Research_Report`, `PowerBI_Dashboard_Comprehensive_Report`, `TabFM_PowerBI_Integrated_Predictions`, `Observation_Field_Insights`, `discover_novel_deep_insights.py`.  
**Target Audience**: Executive Leadership, Policy Advisory Team, M&E Directors  
**PDF/PPTX File**: [`CPD_EDS_Master_Findings_Presentation.pptx`](file:///c:/My%20Files%20Work/Gravity/CPD_EDS_Master_Findings_Presentation.pptx)

---

## 🎯 Master Slide Outline

### **Slide 1: Title & Overview**
* **Title**: *Empirical Findings & Policy Insights: MP Teacher CPD Ecosystem Diagnostic (CPD EDS)*
* **Subtitle**: *Synthesizing Kobo Surveys, PowerBI Analytics, TabFM ML Predictions, and Qualitative Observations*

---

### **Slide 2: Comprehensive Findings Dashboard**
* **1. Non-Academic Workload Burden (68.3%)**:
  - BLO election duty, MDM supervision, SIR data collection, and portal entries consume 25–35% of working hours, taking vital time away from lesson planning.
* **2. High Attendance vs. Low Pedagogical Transfer**:
  - 93.3% attend In-Person Subject Training and 88.3% attend CLSS, but active classroom application drops to **only 20–30%**.
* **3. PowerBI Awareness Gap & Timing Window**:
  - Spontaneous digital awareness is low (38.3%), but **WhatsApp prompting drives 86.7% participation**. 80% prefer digital learning *after school hours*.
* **4. The Digital Paradox & Proxy Completion**:
  - 66.7% paper completion masks widespread **proxy course completion** (using spouse/family phones) and near-zero content recall.
* **5. Margdarshika Cupboard Storage Deficit**:
  - 91.8% received printed booklets, but materials remain stored in cupboards due to lack of CAC co-teaching.
* **6. TabFM Counterfactual Simulation Proof**:
  - Standalone digital training yields **0.0% classroom adoption**, whereas integrated TPD yields **12.0%**.
* **7. Core Teacher Demand**:
  - Teachers explicitly demand CACs to shift from administrative register inspection to **live model teaching demonstrations inside multigrade classrooms**.

---

### **Slide 3: Quantitative Baseline & Attendance Breakdown**
- **Sample Scope**: 60 Study Teachers across 36 MP Districts. Mean Experience = 20.9 years.
- **Period Load**: Mean = 4.7 periods/day. **43.3% of teachers (26/60) take a heavy load of 6 periods daily**.
- **Attendance Metrics**:
  - Subject In-Person Training: **93.3%**
  - CLSS (*Shaikshik Samwaad*): **88.3%**
  - Digital Training (DIKSHA/iGOT): **66.7%**
  - YouTube Live Follow-ups: **35.0%**
  - Election / BLO Duty Burden: **68.3%**

---

### **Slide 4: TabFM ML Counterfactual Scenario Predictions**
*Target Variable*: **Classroom Application of Lesson Plans & Modules**

| Scenario Name | TPD Intervention Strategy | Predicted Adoption Rate (%) |
| :--- | :--- | :---: |
| **Baseline Observed** | Current Observed System State | **16.0%** |
| **Full Integrated TPD** | Subject Training + Digital + CLSS | **12.0%** |
| **Subject Training Only** | Standalone In-Person Workshop | **2.7%** |
| **Digital Training Only** | Standalone DIKSHA / iGOT Courses | **0.0%** |
| **CLSS Only** | Standalone *Shaikshik Samwaad* | **0.0%** |

---

### **Slide 5: Field Observation Insights & Qualitative Ground Truth**
- **HM Admin Burnout**: Headmasters managing primary schools handle non-academic portal filings, leaving zero bandwidth for instructional leadership.
- **Informal CLSS Cascading**: School-level cascading is entirely informal (tea-time chats) or non-existent in single-teacher schools.
- **Demand for CAC Co-Teaching**: Teachers want CACs to spend 70% of school visit time co-teaching and demonstrating multigrade techniques.

---

### **Slide 6: Actionable Strategic Policy Roadmap**
1. **Protect Teaching Time (Short-Term: 0–6m)**: Cap non-academic administrative assignments during active terms. Re-allocate BLO duties to block data operators.
2. **Shift to Blended TPD (Medium-Term: 6–18m)**: Treat digital courses as supplementary reference; keep core learning in interactive face-to-face workshops.
3. **Embed Live Model Demonstrations (Medium-Term: 6–18m)**: Re-design in-person training around live model teaching demonstrations.
4. **Re-Orient CACs to Academic Coaches (Short-Term: 0–6m)**: Mandate CACs spend 70% of visit time co-teaching inside classrooms.
"""

    with open("C:/Users/Peepul/.gemini/antigravity/brain/d4007b68-e6ed-4169-8e19-8fc047825bef/CPD_EDS_Master_Findings_Presentation.md", "w", encoding="utf-8") as f:
        f.write(md_content)

    # 2. Build Native PPTX Slide Deck
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Palette
    c_navy = RGBColor(15, 23, 42)      # #0F172A
    c_blue = RGBColor(2, 132, 199)     # #0284C7
    c_teal = RGBColor(15, 118, 110)    # #0F766E
    c_text = RGBColor(30, 41, 59)      # #1E293B
    c_muted = RGBColor(100, 116, 139)  # #64748B
    c_bg_box = RGBColor(239, 246, 255) # #EFF6FF
    c_white = RGBColor(255, 255, 255)
    c_line = RGBColor(203, 213, 225)   # #CBD5E1

    def add_header(slide, title_text, category_text="KEY RESEARCH FINDINGS & DIAGNOSTIC"):
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p0 = tf.paragraphs[0]
        p0.text = category_text.upper()
        p0.font.name = "Arial"
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = c_blue
        
        p1 = tf.add_paragraph()
        p1.text = title_text
        p1.font.name = "Arial"
        p1.font.size = Pt(22)
        p1.font.bold = True
        p1.font.color.rgb = c_navy
        
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = c_line
        line.line.color.rgb = c_line

    def add_footer(slide, slide_num):
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.9), Inches(11.733), Inches(0.4))
        tf = footer_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p = tf.paragraphs[0]
        p.text = f"MP Teacher CPD Ecosystem Diagnostic Study (CPD EDS)  •  Slide {slide_num} of 6"
        p.font.name = "Arial"
        p.font.size = Pt(9)
        p.font.color.rgb = c_muted

    # SLIDE 1: Title
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = c_navy
    bg1.line.fill.background()

    tbox1 = slide1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(4.5))
    tf1 = tbox1.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "RESEARCH FINDINGS PRESENTATION"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = c_blue
    
    p2 = tf1.add_paragraph()
    p2.text = "Comprehensive Research Findings: MP Teacher CPD EDS"
    p2.font.size = Pt(30)
    p2.font.bold = True
    p2.font.color.rgb = c_white
    p2.space_before = Pt(10)
    
    p3 = tf1.add_paragraph()
    p3.text = "Synthesizing Kobo Surveys, PowerBI Analytics, TabFM ML Predictions, & Field Observations"
    p3.font.size = Pt(16)
    p3.font.color.rgb = RGBColor(148, 163, 184)
    p3.space_before = Pt(10)

    # SLIDE 2: ALL MASTER FINDINGS DASHBOARD (THE MAIN FINDINGS SLIDE)
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "Master Findings Dashboard: Key Empirical & Qualitative Insights")
    add_footer(slide2, 2)

    findings = [
        ("1. Non-Academic Workload Strain (68.3%)", "BLO election duty, MDM supervision, SIR data collection, APAR ID, and admissions consume 25–35% of working hours, cutting into teaching time."),
        ("2. High Attendance vs. Low Transfer", "93.3% attend In-Person Subject Training and 88.3% attend CLSS, but active classroom application drops to only 20–30%."),
        ("3. PowerBI Awareness Gap & Timing Window", "Spontaneous digital awareness is low (38.3%), but WhatsApp prompting drives 86.7% participation. 80% prefer digital learning after school hours."),
        ("4. The Digital Paradox & Proxy Completion", "66.7% paper completion masks widespread proxy course completion (using spouse phones) and near-zero content recall."),
        ("5. Margdarshika Cupboard Storage Deficit", "91.8% received printed booklets, but materials remain stored in cupboards due to lack of ongoing CAC co-teaching."),
        ("6. TabFM Counterfactual Simulation Proof", "Standalone digital training yields 0.0% classroom adoption, whereas integrated TPD yields 12.0%."),
        ("7. Core Teacher Demand for CAC Co-Teaching", "Teachers explicitly demand CACs to shift from administrative register inspection to live model teaching demonstrations in multigrade classrooms.")
    ]

    for idx, (title, desc) in enumerate(findings):
        col = idx % 2
        row = idx // 2
        left = Inches(0.8 + col * 5.9)
        top = Inches(1.7 + row * 1.25)
        
        # Adjust height for last single item
        w = Inches(11.5) if idx == 6 else Inches(5.6)
        
        cbox = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, w, Inches(1.15))
        cbox.fill.solid()
        cbox.fill.fore_color.rgb = c_bg_box
        cbox.line.color.rgb = RGBColor(191, 219, 254)
        
        tf = cbox.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.12)
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = c_navy
        
        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(8.5)
        p_desc.font.color.rgb = c_text
        p_desc.space_before = Pt(2)

    # SLIDE 3: QUANTITATIVE CENSUS
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "Quantitative Profile & TPD Attendance Census (N = 60)")
    add_footer(slide3, 3)

    tbox3 = slide3.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.733), Inches(4.8))
    tf3 = tbox3.text_frame
    tf3.word_wrap = True

    items3 = [
        ("Demographic Baseline", "60 study teachers across 36 MP districts. Mean Experience = 20.9 years (range: 2–34 yrs)."),
        ("Period Load Strain", "Mean = 4.7 periods/day. 43.3% of teachers (26/60) take a heavy load of 6 periods daily."),
        ("In-Person Subject Training Attendance", "93.3% (56/60) — Highest rated format; valued for Think-Pair-Share & activity methods."),
        ("CLSS (Shaikshik Samwaad) Attendance", "88.3% (53/60) — Valued for cross-school peer discussions; school cascading remains informal."),
        ("Digital Training Attendance (DIKSHA/iGOT)", "66.7% (40/60) — High paper completion; high proxy usage and low content recall.")
    ]

    for title, desc in items3:
        p_t = tf3.add_paragraph()
        p_t.text = f"•  {title}: {desc}"
        p_t.font.size = Pt(11)
        p_t.font.bold = False
        p_t.font.color.rgb = c_text
        p_t.space_before = Pt(8)

    # SLIDE 4: TABFM SIMULATION MATRIX
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "TabFM ML Counterfactual Intervention Predictions")
    add_footer(slide4, 4)

    t_sim_table = slide4.shapes.add_table(6, 3, Inches(0.8), Inches(1.8), Inches(11.733), Inches(4.5))
    table4 = t_sim_table.table
    table4.columns[0].width = Inches(3.2)
    table4.columns[1].width = Inches(5.5)
    table4.columns[2].width = Inches(3.033)

    headers4 = ["Intervention Scenario Name", "TPD Policy Strategy Description", "Predicted Adoption Rate (%)"]
    for i, h in enumerate(headers4):
        cell = table4.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = c_navy
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = c_white
        p.alignment = PP_ALIGN.CENTER

    rows_data4 = [
        ("Baseline Observed", "Current Observed System State", "16.0%"),
        ("Scenario A: Full Integrated TPD", "Subject Training + Digital Training + CLSS", "12.0%"),
        ("Scenario B: Subject Training Only", "Standalone In-Person Subject Workshop", "2.7%"),
        ("Scenario C: Digital Training Only", "Standalone DIKSHA / iGOT Online Modules", "0.0%"),
        ("Scenario D: CLSS Only", "Standalone Shaikshik Samwaad Discussions", "0.0%")
    ]

    for r_idx, r_data in enumerate(rows_data4):
        for c_idx, val in enumerate(r_data):
            cell = table4.cell(r_idx + 1, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = c_white if r_idx % 2 == 0 else c_bg_box
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            p.font.color.rgb = c_text
            if c_idx == 0 or c_idx == 2:
                p.font.bold = True

    # SLIDE 5: QUALITATIVE & FIELD OBSERVER INSIGHTS
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "Qualitative Field Insights & Observer Ground Truth")
    add_footer(slide5, 5)

    tbox5 = slide5.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.733), Inches(4.8))
    tf5 = tbox5.text_frame
    tf5.word_wrap = True

    items5 = [
        ("Headmaster (HM) Admin Burnout", "Headmasters managing primary schools handle non-academic portal filings (MDM, SIR, admissions), leaving near-zero bandwidth for instructional leadership."),
        ("Informal CLSS Cascading", "School-level cascading is entirely informal (tea-time chats) or non-existent in single-teacher schools due to absence of co-teachers."),
        ("Demand for CAC Co-Teaching", "Teachers explicitly request CACs to spend 70% of visit time co-teaching and demonstrating multigrade techniques inside actual classrooms.")
    ]

    for title, desc in items5:
        p_t = tf5.add_paragraph()
        p_t.text = f"•  {title}:"
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = c_teal
        p_t.space_before = Pt(10)

        p_d = tf5.add_paragraph()
        p_d.text = f"    {desc}"
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = c_text
        p_d.space_before = Pt(3)

    # SLIDE 6: STRATEGIC POLICY ROADMAP
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "Actionable Strategic Policy Roadmap & Future Measures")
    add_footer(slide6, 6)

    steps = [
        ("1. Protect Teaching Time (0–6 Months)", "Issue a strict department order capping non-academic administrative assignments. Re-allocate BLO duties to block data operators."),
        ("2. Shift to Blended TPD (6–18 Months)", "Reposition DIKSHA as a supplementary micro-library while keeping core TPD centered on interactive face-to-face workshops."),
        ("3. CAC Co-Teaching Mandate (0–6 Months)", "Re-orient Cluster Academic Coordinators (CACs) to spend 70% of visit time delivering live model demonstration lessons inside multigrade classrooms.")
    ]

    for idx, (title, desc) in enumerate(steps):
        col = idx
        left = Inches(0.8 + col * 3.9)
        top = Inches(2.0)
        
        cbox = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(3.7), Inches(4.2))
        cbox.fill.solid()
        cbox.fill.fore_color.rgb = c_bg_box
        cbox.line.color.rgb = RGBColor(191, 219, 254)
        
        tf = cbox.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.25)
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = c_navy
        
        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(10)
        p_desc.font.color.rgb = c_text
        p_desc.space_before = Pt(10)

    prs.save("CPD_EDS_Master_Findings_Presentation.pptx")
    print("SUCCESS! Built Master Findings PPTX slide deck.")

if __name__ == "__main__":
    build_findings_deck()
