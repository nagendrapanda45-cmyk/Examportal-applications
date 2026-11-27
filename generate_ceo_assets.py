import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

import pptx
from pptx.util import Inches as PptInches, Pt as PptPt
from pptx.dml.color import RGBColor as PptRGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def generate_word_document(filename):
    doc = docx.Document()
    
    # Page setup (Standard 0.75" margins)
    for s in doc.sections:
        s.top_margin = Inches(0.75)
        s.bottom_margin = Inches(0.75)
        s.left_margin = Inches(0.75)
        s.right_margin = Inches(0.75)

    # Document Header Title
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run("INTELLIGENZ IT TALENTASSESS 360™\n")
    run.font.name = "Arial"
    run.font.size = Pt(22)
    run.font.bold = True
    run.font.color.rgb = RGBColor(233, 30, 99) # Brand Pink

    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    s_run = subtitle.add_run("Transforming Human Capital Acquisition with AI & Automation\nEnd-to-End Technical Architecture, 8-Pillar Business Mind Map, DoR/DoD & CEO Executive Dossier")
    s_run.font.name = "Arial"
    s_run.font.size = Pt(12)
    s_run.font.italic = True
    s_run.font.color.rgb = RGBColor(71, 85, 105)

    doc.add_paragraph()

    # 1. Executive Summary & Vision
    h1 = doc.add_heading(level=1)
    h1.add_run("1. Executive Vision & Core Platform Mission").font.color.rgb = RGBColor(15, 23, 42)
    p = doc.add_paragraph(
        "Intelligenz IT TalentAssess 360™ is an enterprise-grade, autonomous AI assessment and digital recruitment cloud. "
        "It eliminates manual hiring bottlenecks, protects assessment integrity via Edge AI proctoring, and accelerates "
        "time-to-hire by 85%. From initial campus discovery via dynamic QR codes to automated scoring and Odoo ERP integration, "
        "the platform supports continuous evaluation of 50,000+ candidates simultaneously with zero latency."
    )
    p.paragraph_format.line_spacing = 1.15

    # 2. The 8-Pillar Business Mind Map Table
    h2 = doc.add_heading(level=1)
    h2.add_run("2. The 8-Pillar Business Mind Map (Executive Breakdown)").font.color.rgb = RGBColor(15, 23, 42)

    pillars = [
        ("1. WHY? Business Need & Value", "Reduces manual recruiting effort, speeds up hiring cycles, standardizes evaluations, lowers cost-per-hire, filters higher-quality candidates, and enables data-driven leadership decisions.", "E11D48"),
        ("2. WHO? Users & Stakeholders", "External Candidates (Students & Working Professionals), Internal Recruiters & HR Teams, Technical Hiring Managers, System Administrators, and Executive Management.", "7C3AED"),
        ("3. WHAT? Core Capabilities", "Job requisitions & approvals, candidate profiles, document upload/verification, 2-tier online assessments (General + Technical), AI proctoring & anti-cheat, candidate tracking, and analytics dashboards.", "0284C7"),
        ("4. HOW? Technology & Process", "Responsive web portal, structured evaluation workflows, real-time Edge AI vision proctoring (Face/Tab/Multi-screen), secure RBAC, indexed MySQL database, and cloud/on-premise deployment.", "EA580C"),
        ("5. KEY FEATURES What We Offer", "Online proctored exams, bilingual portal support (Arabic & English), Applicant Tracking System (ATS), advanced reporting, role-based access control, and Odoo ERP integration.", "0D9488"),
        ("6. WHERE? Deployment & Integration", "Company careers portal, LinkedIn/Naukri integration, dynamic campus QR campaigns, Odoo ERP (HR/Payroll), Cloud (AWS/Azure) or On-Premise across GCC, Middle East, and Global.", "D97706"),
        ("7. WHEN? Use Cases & Scenarios", "High-volume campus recruitment drives, bulk hiring (50,000+ candidates), lateral technical hiring, graduate recruitment, domain-specific coding tests, and periodic employee skill evaluations.", "4F46E5"),
        ("8. BENEFITS Business Outcomes", "50,000+ candidate scale, zero-latency execution, 100% test integrity, reduced coordination overhead, faster time-to-hire, superior candidate UX, measurable hiring metrics, and multi-lingual accessibility.", "16A34A")
    ]

    t_p = doc.add_table(rows=len(pillars)+1, cols=3)
    t_p.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, col_h in enumerate(["Pillar & Dimension", "Core Focus & Deliverables", "Strategic Color Code"]):
        cell = t_p.cell(0, idx)
        set_cell_background(cell, "0F172A")
        cp = cell.paragraphs[0]
        r = cp.add_run(col_h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(10)

    for idx, (p_name, p_desc, p_hex) in enumerate(pillars, start=1):
        c0 = t_p.cell(idx, 0)
        c1 = t_p.cell(idx, 1)
        c2 = t_p.cell(idx, 2)
        set_cell_background(c0, "F8FAFC" if idx % 2 == 1 else "FFFFFF")
        set_cell_background(c1, "F8FAFC" if idx % 2 == 1 else "FFFFFF")
        set_cell_background(c2, p_hex)

        r0 = c0.paragraphs[0].add_run(p_name)
        r0.font.bold = True
        r0.font.size = Pt(9.5)

        r1 = c1.paragraphs[0].add_run(p_desc)
        r1.font.size = Pt(9.5)

        r2 = c2.paragraphs[0].add_run(f"#{p_hex}")
        r2.font.bold = True
        r2.font.size = Pt(9)
        r2.font.color.rgb = RGBColor(255, 255, 255)

    doc.add_paragraph()

    # 3. End-to-End Technical Architecture
    h3 = doc.add_heading(level=1)
    h3.add_run("3. End-to-End System & Technical Architecture").font.color.rgb = RGBColor(15, 23, 42)

    arch_sections = [
        ("A. Candidate Journey (External Users - 8 Stages)", 
         "1. Find Opportunity: Inbound discovery via LinkedIn, Naukri, official careers page, and dynamic campus QR codes.\n"
         "2. Smart Registration: Form validation with 240+ global dial codes, alphanumeric PAN authentication, and dynamic qualification fields.\n"
         "3. Success & Email: Immediate confirmation screen and automated branded HR status email.\n"
         "4. Candidate Login: Secure session authentication via Registration ID and credentials.\n"
         "5. Profile Review: Candidate profile inspection and document verification before exam entry.\n"
         "6. Pre-Test Gate & Camera Test: Hardware webcam handshake, face quality check, and single-person validation.\n"
         "7. Multi-Tier Assessment: Round 1 General Cognitive (Aptitude/Logic) followed by Round 2 Technical Mastery (Coding/MCQ).\n"
         "8. Completion & Feedback: Automated exam submission, 5-star experience rating, and auto-generated result notification."),
        
        ("B. High-Level System Architecture & Infrastructure",
         "• Client Devices: Desktop/Laptop/Mobile (Chrome, Edge, Firefox) with Edge AI vision inference.\n"
         "• Web Application Layer: Django 5 / Python modular backend (Auth, Exam Dashboard, Question Bank, RBAC, Scheduler, QR Engine).\n"
         "• Security & Proctoring Services: Coco-SSD Face Detection, Tab-Switch Lockout, Dual-Monitor Defense, Geolocation Tracking.\n"
         "• Database Layer: Enterprise MySQL with indexation (db_index=True) on candidate IDs, emails, and test results.\n"
         "• External Integrations: SMTP/SendGrid Email Services, LinkedIn/Naukri Job Sources, Odoo ERP (HR & Payroll).\n"
         "• DevOps & Infrastructure: Containerized Docker deployment, Nginx reverse proxy, Linux server, and Prometheus/Grafana monitoring."),
        
        ("C. Admin / HR Workflow (14 Integrated Command Modules)",
         "1. Executive Dashboard (Live funnel & test KPIs) | 2. Manage Candidates (Profile directory & PDF dossier export)\n"
         "3. Manage Tests (Duration & cutoff controls) | 4. Question Bank (Categorized question authoring)\n"
         "5. Candidate Invites (Bulk invitation engine) | 6. Monitor & Proctor (Live exam audit & violation logs)\n"
         "7. Evaluate Results (Auto-grading & audit) | 8. Manage Instructions (Pre-test compliance rules)\n"
         "9. Manage QR (Self-service campus drive QR codes) | 10. Email Templates (Branded email builder)\n"
         "11. Role / User Access (15-module granular RBAC) | 12. Configurations (Global system cutoffs & keys)\n"
         "13. Reports & Analytics (Data-driven hiring reports) | 14. Offer & Onboard (Integration with Odoo HR & contracts).")
    ]

    for a_title, a_desc in arch_sections:
        h = doc.add_heading(level=2)
        h.add_run(a_title).font.color.rgb = RGBColor(233, 30, 99)
        p = doc.add_paragraph(a_desc)
        p.paragraph_format.line_spacing = 1.15

    doc.add_paragraph()

    # 4. Definition of Ready (DoR) and Definition of Done (DoD)
    h4 = doc.add_heading(level=1)
    h4.add_run("4. Engineering & Governance Methodology: DoR and DoD").font.color.rgb = RGBColor(15, 23, 42)

    p_d = doc.add_paragraph(
        "To guarantee 99.9% uptime and zero-defect assessment delivery during critical 50,000+ candidate campus drives, "
        "TalentAssess 360 enforces strict Definition of Ready (DoR) and Definition of Done (DoD) standards:"
    )

    dor_dod_table = doc.add_table(rows=7, cols=2)
    dor_dod_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    dor_dod_table.cell(0, 0).paragraphs[0].add_run("Definition of Ready (DoR) - Pre-Exam Gate").font.bold = True
    dor_dod_table.cell(0, 0).paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
    set_cell_background(dor_dod_table.cell(0, 0), "0F172A")

    dor_dod_table.cell(0, 1).paragraphs[0].add_run("Definition of Done (DoD) - Evaluation & Hiring Gate").font.bold = True
    dor_dod_table.cell(0, 1).paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
    set_cell_background(dor_dod_table.cell(0, 1), "0F172A")

    dor_items = [
        "Candidate identity validated via alphanumeric PAN & global mobile matching.",
        "Candidate device passes hardware webcam & bandwidth handshake.",
        "Code of Conduct and Anti-Cheat rules acknowledged via SweetAlert2 modal.",
        "Exam questions randomized from verified Question Bank with configured cutoffs.",
        "Edge AI proctoring model (Coco-SSD) loaded client-side with camera active.",
        "Server database connection pool verified with active Prometheus monitoring."
    ]

    dod_items = [
        "All candidate responses securely committed to MySQL with zero unhandled exceptions.",
        "Auto-scoring engine calculates raw marks, section percentages, and pass/fail flags.",
        "Integrity audit confirms zero unhandled multi-person or tab-switch infractions.",
        "Result table populated with candidate record visible at top of Admin Results view.",
        "One-click PDF dossier generated with candidate photo, scores, and 5-star rating.",
        "Automated confirmation email delivered to candidate and candidate status updated for HR."
    ]

    for idx, (dor, dod) in enumerate(zip(dor_items, dod_items), start=1):
        c_dor = dor_dod_table.cell(idx, 0)
        c_dod = dor_dod_table.cell(idx, 1)
        set_cell_background(c_dor, "F8FAFC" if idx % 2 == 1 else "FFFFFF")
        set_cell_background(c_dod, "F8FAFC" if idx % 2 == 1 else "FFFFFF")
        c_dor.paragraphs[0].add_run(f"✓ {dor}").font.size = Pt(9.5)
        c_dod.paragraphs[0].add_run(f"✓ {dod}").font.size = Pt(9.5)

    doc.add_paragraph()

    # 5. Real-World Enterprise Use Cases
    h5 = doc.add_heading(level=1)
    h5.add_run("5. Real-World Enterprise Use Cases").font.color.rgb = RGBColor(15, 23, 42)

    use_cases = [
        ("Campus Recruitment Drives (5,000+ Students in 3 Hours)",
         "Universities host massive on-site placement drives. TalentAssess 360 deploys dynamic QR codes projected in auditorium halls. Students scan the QR on their laptops or mobile devices, register instantly, and take Round 1 (General Aptitude) concurrently. Results are compiled within 5 minutes, allowing HR to interview the top 20% on the same afternoon."),
        
        ("Lateral Engineering Hiring (AI, Python, Cloud & DevOps)",
         "Experienced candidates undergo rigorous Round 2 technical tests featuring domain-specific algorithmic questions. The proprietary browser anti-cheat shield prevents ChatGPT abuse, tab-switching, and dual-monitor usage, ensuring only authentic, unassisted technical talent advances to executive technical panels."),
        
        ("Global & GCC Multi-Lingual Recruitment with Odoo ERP",
         "Designed for multi-regional deployment across GCC and India, the platform supports bilingual portals (Arabic & English) and integrates directly with Odoo ERP for automated employee onboarding, contract creation, and HR records synchronization.")
    ]

    for uc_title, uc_desc in use_cases:
        p_uc = doc.add_paragraph()
        r_t = p_uc.add_run(f"• {uc_title}\n")
        r_t.font.bold = True
        r_t.font.size = Pt(11)
        r_t.font.color.rgb = RGBColor(233, 30, 99)
        r_b = p_uc.add_run(uc_desc)
        r_b.font.size = Pt(10)
        p_uc.paragraph_format.line_spacing = 1.15

    doc.save(filename)
    print(f"Successfully generated Word document: {filename}")

def generate_powerpoint_presentation(filename):
    prs = pptx.Presentation()
    prs.slide_width = PptInches(13.333) # 16:9 Widescreen
    prs.slide_height = PptInches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_slide_header(slide, title_text, category_text="INTELLIGENZ IT TALENTASSESS 360™ | EXECUTIVE ARCHITECTURE & MIND MAP"):
        cat_box = slide.shapes.add_textbox(PptInches(0.8), PptInches(0.4), PptInches(10), PptInches(0.3))
        tf_cat = cat_box.text_frame
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = "Arial"
        p_cat.font.size = PptPt(9)
        p_cat.font.bold = True
        p_cat.font.color.rgb = PptRGBColor(233, 30, 99)

        title_box = slide.shapes.add_textbox(PptInches(0.8), PptInches(0.65), PptInches(11.5), PptInches(0.7))
        tf = title_box.text_frame
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Arial"
        p.font.size = PptPt(22)
        p.font.bold = True
        p.font.color.rgb = PptRGBColor(15, 23, 42)

    # ------------------ SLIDE 1: Title Slide ------------------
    slide1 = prs.slides.add_slide(blank_layout)
    bg = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = PptRGBColor(15, 23, 42)
    bg.line.fill.background()

    tbox = slide1.shapes.add_textbox(PptInches(1.0), PptInches(1.6), PptInches(11.3), PptInches(3.2))
    tf1 = tbox.text_frame
    p0 = tf1.paragraphs[0]
    p0.text = "INTELLIGENZ IT TALENTASSESS 360™"
    p0.font.name = "Arial"
    p0.font.size = PptPt(38)
    p0.font.bold = True
    p0.font.color.rgb = PptRGBColor(233, 30, 99)

    p1 = tf1.add_paragraph()
    p1.text = "AI-Powered Assessment & Digital Recruitment Platform"
    p1.font.name = "Arial"
    p1.font.size = PptPt(20)
    p1.font.color.rgb = PptRGBColor(255, 255, 255)

    p2 = tf1.add_paragraph()
    p2.text = "End-to-End Workflow, Technical Architecture, 8-Pillar Mind Map & Real-World Use Cases"
    p2.font.name = "Arial"
    p2.font.size = PptPt(14)
    p2.font.italic = True
    p2.font.color.rgb = PptRGBColor(148, 163, 184)

    fbox = slide1.shapes.add_textbox(PptInches(1.0), PptInches(6.2), PptInches(11.3), PptInches(0.6))
    p_f = fbox.text_frame.paragraphs[0]
    p_f.text = "VISION: TRANSFORMING HUMAN CAPITAL ACQUISITION WITH AI & AUTOMATION"
    p_f.font.size = PptPt(11)
    p_f.font.bold = True
    p_f.font.color.rgb = PptRGBColor(100, 116, 139)

    # ------------------ SLIDE 2: 8-Pillar Business Mind Map ------------------
    slide2 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide2, "1. The 8-Pillar Business Mind Map")

    eight_pillars = [
        ("1. WHY? Business Need", "Reduce manual effort, faster & consistent hiring, standardized tests, lower cost, data-driven decisions.", PptRGBColor(225, 29, 72)),
        ("2. WHO? Stakeholders", "Candidates (Students/Pros), Recruiters & HR, Hiring Managers, Admins, Executive Leadership.", PptRGBColor(124, 58, 237)),
        ("3. WHAT? Capabilities", "Job requisitions, registration profiles, document upload, 2-tier online tests, AI proctoring, tracking, analytics.", PptRGBColor(2, 132, 199)),
        ("4. HOW? Technology", "Responsive web portal, structured workflows, real-time AI proctoring (Camera/Tab/Screen), secure MySQL, cloud/on-prem.", PptRGBColor(234, 88, 12)),
        ("5. KEY FEATURES", "Online proctored tests, bilingual portal (Arabic/English), ATS, Odoo ERP integration, role-based access.", PptRGBColor(13, 148, 136)),
        ("6. WHERE? Sourcing", "Careers portal, LinkedIn/Naukri, dynamic campus QR campaigns, Odoo ERP, Cloud AWS/Azure or On-Premise.", PptRGBColor(217, 119, 6)),
        ("7. WHEN? Use Cases", "Campus drives, bulk hiring (50K+), lateral hiring, graduate recruitment, domain-specific coding tests.", PptRGBColor(79, 70, 229)),
        ("8. BENEFITS & ROI", "50,000+ candidates at scale, zero latency, 100% test integrity, faster hiring cycle, measurable recruitment ROI.", PptRGBColor(22, 163, 74))
    ]

    for idx, (title, desc, color) in enumerate(eight_pillars):
        col = idx % 4
        row = idx // 4
        x = 0.8 + col * 2.95
        y = 1.5 + row * 2.7
        box = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, PptInches(x), PptInches(y), PptInches(2.8), PptInches(2.45))
        box.fill.solid()
        box.fill.fore_color.rgb = PptRGBColor(255, 255, 255)
        box.line.color.rgb = color
        box.line.width = PptPt(2.5)

        tf = box.text_frame
        tf.margin_left = PptInches(0.15)
        tf.margin_top = PptInches(0.15)
        p = tf.paragraphs[0]
        p.text = title
        p.font.bold = True
        p.font.size = PptPt(12)
        p.font.color.rgb = color

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = PptPt(10)
        p_d.font.color.rgb = PptRGBColor(51, 65, 85)

    # ------------------ SLIDE 3: Candidate Journey (8 Stages) ------------------
    slide3 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide3, "2. Section A: Candidate Journey (External Users - 8 Stages)")

    journey_steps = [
        ("1. Find Opportunity", "Inbound discovery via LinkedIn, Naukri, company careers page, or campus QR scan."),
        ("2. Smart Registration", "Personal details, document uploads, 240+ global country dial codes, alphanumeric PAN validation."),
        ("3. Success & Email", "Instant confirmation screen and automated branded HTML status email from Intelligenz IT."),
        ("4. Candidate Login", "Secure authentication via Registration ID and credentials."),
        ("5. Profile Review", "Review profile details, qualification toggles (UG % vs PG CGPA), and test eligibility."),
        ("6. Instructions & Camera Test", "Read compliance rules, webcam hardware handshake, live face detection test."),
        ("7. Multi-Round Exam", "Progression from Round 1 General Cognitive (Aptitude) to Round 2 Technical Mastery (Coding/MCQs)."),
        ("8. Test Completion", "Exam auto-submitted, response audit saved, 5-star candidate experience rating submitted.")
    ]

    for idx, (title, desc) in enumerate(journey_steps):
        row = idx // 2
        col = idx % 2
        x = 0.8 + col * 5.9
        y = 1.5 + row * 1.35
        card = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, PptInches(x), PptInches(y), PptInches(5.7), PptInches(1.2))
        card.fill.solid()
        card.fill.fore_color.rgb = PptRGBColor(248, 250, 252)
        card.line.color.rgb = PptRGBColor(233, 30, 99) if col == 0 else PptRGBColor(14, 165, 233)
        card.line.width = PptPt(2)

        tf = card.text_frame
        tf.margin_left = PptInches(0.2)
        tf.margin_top = PptInches(0.12)
        p = tf.paragraphs[0]
        p.text = title
        p.font.bold = True
        p.font.size = PptPt(12)
        p.font.color.rgb = PptRGBColor(15, 23, 42)

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = PptPt(10)
        p_d.font.color.rgb = PptRGBColor(71, 85, 105)

    # ------------------ SLIDE 4: System Architecture High-Level ------------------
    slide4 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide4, "3. Section B: System Architecture (High-Level)")

    arch_boxes = [
        ("Candidate Devices (Browser)", "• Desktop / Laptop (Chrome, Edge)\n• Mobile / Tablet Responsive UI\n• Webcam Live Proctoring\n• GPS / IP Location Tracking\n• Hardware/Display Monitoring", 0.8, 1.5, 3.7, 2.5, PptRGBColor(14, 165, 233)),
        ("Web Application (Django / Python)", "• Authentication & User Mgmt\n• Exam Dashboard & Test Mgmt\n• Question Bank & Randomizer\n• Role-Based Access (15 Modules)\n• Email Scheduler & Notifications\n• QR Generator & Campus Engine", 4.8, 1.5, 4.3, 2.5, PptRGBColor(233, 30, 99)),
        ("Security & Proctoring AI", "• Coco-SSD Face Detection AI\n• Multi-Person Detection & Filter\n• Tab-Switching Lockout\n• Dual-Monitor Defense\n• Geolocation & Session Tracking\n• Screenshot & Violation Logs", 9.4, 1.5, 3.1, 2.5, PptRGBColor(249, 115, 22)),
        ("Database & Storage", "• Enterprise MySQL (50,000+ indexed records)\n• Local/Cloud Media Storage (Resume, ID Proof, Photo)\n• Zero N+1 query optimization (select_related)", 0.8, 4.3, 4.3, 2.4, PptRGBColor(16, 185, 129)),
        ("Infrastructure & DevOps", "• Cloud (AWS/Azure) or On-Premise\n• Docker Containerization\n• Nginx High-Concurrency Reverse Proxy\n• Prometheus & Grafana System Monitoring", 5.4, 4.3, 3.8, 2.4, PptRGBColor(124, 58, 237)),
        ("External Integrations", "• SMTP / SendGrid Email\n• LinkedIn / Naukri Sourcing\n• Odoo ERP (HR, Payroll)\n• Corporate Careers Portal", 9.5, 4.3, 3.0, 2.4, PptRGBColor(2, 132, 199))
    ]

    for title, desc, x, y, w, h, color in arch_boxes:
        box = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, PptInches(x), PptInches(y), PptInches(w), PptInches(h))
        box.fill.solid()
        box.fill.fore_color.rgb = PptRGBColor(255, 255, 255)
        box.line.color.rgb = color
        box.line.width = PptPt(2.5)

        tf = box.text_frame
        tf.margin_left = PptInches(0.18)
        tf.margin_top = PptInches(0.15)
        p = tf.paragraphs[0]
        p.text = title
        p.font.bold = True
        p.font.size = PptPt(12)
        p.font.color.rgb = color

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = PptPt(9.5)
        p_d.font.color.rgb = PptRGBColor(51, 65, 85)

    # ------------------ SLIDE 5: Admin / HR 14 Modules ------------------
    slide5 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide5, "4. Section C: Admin / HR Workflow (14 Core Modules)")

    admin_14 = [
        ("01. Dashboard", "Real-time stats, registrations, tests in progress, recent activity"),
        ("02. Manage Candidates", "View, search, filter, verify documents, shortlist/reject, check profiles"),
        ("03. Manage Tests", "Create tests, set time & rules, assign sections: General/Technical"),
        ("04. Question Bank", "Add/Edit/Delete MCQ/Coding, categorize by skill, import/export"),
        ("05. Send Invitations", "Select candidates, set exam date & time, send email/SMS, track status"),
        ("06. Monitor & Proctor", "Live monitoring, view violations, camera snapshots, session logs"),
        ("07. Evaluate Results", "Auto evaluation, manual review, final result matrix, export reports"),
        ("08. Manage Instructions", "Create guidelines, set rules per role / domain"),
        ("09. Manage QR", "Generate QR codes, campus/walk-in drives, track scans"),
        ("10. Email Templates", "Branded emails, custom templates, status notifications"),
        ("11. User / Role Access", "Add/edit users, role permissions, Admin/HR/Invigilator RBAC"),
        ("12. Configuration", "System settings, exam parameters, integration keys"),
        ("13. Reports & Analytics", "Hiring insights, performance reports, download PDF/Excel"),
        ("14. Offer & Onboard", "Generate offers, digital contracts, integrate with Odoo ERP HR")
    ]

    for idx, (m_title, m_desc) in enumerate(admin_14):
        col = idx // 7
        row = idx % 7
        x = 0.8 + col * 5.9
        y = 1.45 + row * 0.78
        box = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, PptInches(x), PptInches(y), PptInches(5.7), PptInches(0.7))
        box.fill.solid()
        box.fill.fore_color.rgb = PptRGBColor(248, 250, 252)
        box.line.color.rgb = PptRGBColor(203, 213, 225)
        box.line.width = PptPt(1)

        tf = box.text_frame
        tf.margin_left = PptInches(0.15)
        tf.margin_top = PptInches(0.08)
        p = tf.paragraphs[0]
        p.text = m_title
        p.font.bold = True
        p.font.size = PptPt(11)
        p.font.color.rgb = PptRGBColor(233, 30, 99) if col == 0 else PptRGBColor(14, 165, 233)

        p_d = tf.add_paragraph()
        p_d.text = m_desc
        p_d.font.size = PptPt(9)
        p_d.font.color.rgb = PptRGBColor(71, 85, 105)

    # ------------------ SLIDE 6: DoR & DoD Engineering Governance ------------------
    slide6 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide6, "5. Engineering & Governance: Definition of Ready (DoR) & Done (DoD)")

    dor_card = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, PptInches(0.8), PptInches(1.5), PptInches(5.7), PptInches(5.2))
    dor_card.fill.solid()
    dor_card.fill.fore_color.rgb = PptRGBColor(255, 255, 255)
    dor_card.line.color.rgb = PptRGBColor(233, 30, 99)
    dor_card.line.width = PptPt(2.5)

    tf_dor = dor_card.text_frame
    tf_dor.margin_left = PptInches(0.25)
    tf_dor.margin_top = PptInches(0.2)
    p = tf_dor.paragraphs[0]
    p.text = "🎯 Definition of Ready (DoR) - Pre-Exam Gate"
    p.font.bold = True
    p.font.size = PptPt(14)
    p.font.color.rgb = PptRGBColor(233, 30, 99)

    dor_pts = [
        "Identity Verified: Alphanumeric PAN + global mobile country code match.",
        "Hardware Handshake: Webcam resolution and network bandwidth confirmed.",
        "Code of Conduct: SweetAlert2 strict compliance modal accepted.",
        "Test Generated: Questions pulled from Question Bank with configured rules.",
        "Edge AI Model Active: Coco-SSD initialized inside browser (Face verified).",
        "System Healthy: Database indexed and Prometheus metrics streaming."
    ]
    for pt in dor_pts:
        p_pt = tf_dor.add_paragraph()
        p_pt.text = f"✓ {pt}"
        p_pt.font.size = PptPt(10.5)
        p_pt.font.color.rgb = PptRGBColor(30, 41, 59)

    dod_card = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, PptInches(6.8), PptInches(1.5), PptInches(5.7), PptInches(5.2))
    dod_card.fill.solid()
    dod_card.fill.fore_color.rgb = PptRGBColor(255, 255, 255)
    dod_card.line.color.rgb = PptRGBColor(16, 185, 129)
    dod_card.line.width = PptPt(2.5)

    tf_dod = dod_card.text_frame
    tf_dod.margin_left = PptInches(0.25)
    tf_dod.margin_top = PptInches(0.2)
    p = tf_dod.paragraphs[0]
    p.text = "🏁 Definition of Done (DoD) - Evaluation & Hiring Gate"
    p.font.bold = True
    p.font.size = PptPt(14)
    p.font.color.rgb = PptRGBColor(16, 185, 129)

    dod_pts = [
        "Responses Committed: Zero unhandled test submissions; answers stored in DB.",
        "Auto-Evaluation Complete: Raw marks, percentages, and pass/fail generated.",
        "Proctoring Audited: Zero unhandled multi-person or tab-switching violations.",
        "Result Registered: Candidate visible in Admin Results hub (/results/).",
        "PDF Dossier Ready: One-click candidate portfolio with 5-star rating & feedback.",
        "Automated Communication: Branded confirmation email sent and HR notified."
    ]
    for pt in dod_pts:
        p_pt = tf_dod.add_paragraph()
        p_pt.text = f"✓ {pt}"
        p_pt.font.size = PptPt(10.5)
        p_pt.font.color.rgb = PptRGBColor(30, 41, 59)

    # ------------------ SLIDE 7: Real-World Use Cases ------------------
    slide7 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide7, "6. Real-World Enterprise Deployment Scenarios")

    use_case_cards = [
        ("Campus Recruitment Drives (5,000+ Concurrent Students)",
         "Universities project dynamic QR codes in audit halls. Students scan on laptops/phones, complete instant onboarding with 240+ global country codes, and take Round 1 Aptitude simultaneously. Results are ready in 5 minutes for same-day hiring.", PptRGBColor(233, 30, 99)),
        ("Lateral Engineering Hiring (AI, Python, Cloud & QA)",
         "High-stakes technical assessments for experienced developers. The browser anti-cheat shield completely prevents ChatGPT in background tabs, dual-monitors, and proxy test-takers, ensuring 100% genuine engineering talent.", PptRGBColor(14, 165, 233)),
        ("Global Multi-Lingual & Odoo ERP Integration (GCC & Global)",
         "Bilingual candidate experience (Arabic & English) with direct Odoo ERP integration. Candidate scores automatically sync into Odoo HR for seamless contract generation, onboarding, and payroll provisioning.", PptRGBColor(16, 185, 129))
    ]

    for idx, (title, desc, color) in enumerate(use_case_cards):
        box = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, PptInches(0.8), PptInches(1.5 + idx * 1.8), PptInches(11.7), PptInches(1.6))
        box.fill.solid()
        box.fill.fore_color.rgb = PptRGBColor(248, 250, 252)
        box.line.color.rgb = color
        box.line.width = PptPt(2.5)

        tf = box.text_frame
        tf.margin_left = PptInches(0.25)
        tf.margin_top = PptInches(0.2)
        p = tf.paragraphs[0]
        p.text = f"📌 {title}"
        p.font.bold = True
        p.font.size = PptPt(13)
        p.font.color.rgb = color

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = PptPt(10.5)
        p_d.font.color.rgb = PptRGBColor(51, 65, 85)

    # ------------------ SLIDE 8: Business Outcomes & Strategic ROI ------------------
    slide8 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide8, "7. Measurable Business Outcomes & CEO Value Proposition")

    roi_metrics = [
        ("85% Less Engineering Time", "Automating preliminary screening recovers 300+ billable senior developer hours every month.", PptRGBColor(16, 185, 129)),
        ("70% Drop in Cost-Per-Hire", "Insourcing assessment IP saves $15,000–$25,000 annually in HackerRank / Mettl subscriptions.", PptRGBColor(14, 165, 233)),
        ("Zero Cloud GPU Bills", "In-browser Edge AI vision runs on candidate devices, eliminating expensive cloud GPU streaming costs.", PptRGBColor(233, 30, 99)),
        ("100% Hiring Authenticity", "Proprietary multi-person detection and tab lockout eliminates proxy hiring and remote test fraud.", PptRGBColor(249, 115, 22))
    ]

    for idx, (m_title, m_desc, m_color) in enumerate(roi_metrics):
        col = idx % 2
        row = idx // 2
        x = 0.8 + col * 6.0
        y = 1.6 + row * 2.5
        box = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, PptInches(x), PptInches(y), PptInches(5.7), PptInches(2.2))
        box.fill.solid()
        box.fill.fore_color.rgb = PptRGBColor(255, 255, 255)
        box.line.color.rgb = m_color
        box.line.width = PptPt(3)

        tf = box.text_frame
        tf.margin_left = PptInches(0.3)
        tf.margin_top = PptInches(0.2)
        p = tf.paragraphs[0]
        p.text = m_title
        p.font.bold = True
        p.font.size = PptPt(18)
        p.font.color.rgb = m_color

        p_d = tf.add_paragraph()
        p_d.text = m_desc
        p_d.font.size = PptPt(11.5)
        p_d.font.color.rgb = PptRGBColor(71, 85, 105)

    prs.save(filename)
    print(f"Successfully generated PowerPoint presentation: {filename}")

if __name__ == "__main__":
    generate_word_document("Intelligenz_TalentAssess_360_Executive_Dossier.docx")
    generate_powerpoint_presentation("Intelligenz_TalentAssess_360_CEO.pptx")
