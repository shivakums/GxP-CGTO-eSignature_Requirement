from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUTPUT = r"C:\Users\I308878\GxP-CGTO-eSignature_Requirement\GxP_Training_Implementation_Highlights.pdf"

# ── Colours ───────────────────────────────────────────────────────────────────
SAP_DARK      = colors.HexColor("#003366")
SAP_BLUE      = colors.HexColor("#0070F2")
SAP_LIGHT     = colors.HexColor("#E8F4FD")
BTP_GREEN     = colors.HexColor("#1A6632")
BTP_LIGHT     = colors.HexColor("#E6F4EA")
ORANGE        = colors.HexColor("#E87722")
ORANGE_LIGHT  = colors.HexColor("#FFF3E8")
PURPLE        = colors.HexColor("#6B3FA0")
PURPLE_LIGHT  = colors.HexColor("#F0EAF8")
TEAL          = colors.HexColor("#007B8A")
TEAL_LIGHT    = colors.HexColor("#E0F5F7")
GOLD          = colors.HexColor("#F0AB00")
GOLD_LIGHT    = colors.HexColor("#FFFBE6")
RED           = colors.HexColor("#BB0000")
RED_LIGHT     = colors.HexColor("#FFF0F0")
GREEN_OK      = colors.HexColor("#188918")
GREEN_LIGHT   = colors.HexColor("#E6F4EA")
GREY_BG       = colors.HexColor("#F5F5F5")
GREY_BORDER   = colors.HexColor("#CCCCCC")
WHITE         = colors.white
BLACK         = colors.black
DARK_GREY     = colors.HexColor("#444444")

W, H = A4

# ── Styles ────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def ms(name, **kw):
    return ParagraphStyle(name=name, parent=styles["Normal"], **kw)

TITLE      = ms("T",   fontSize=22, textColor=WHITE,    fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=4)
SUBTITLE   = ms("ST",  fontSize=11, textColor=colors.HexColor("#AACCFF"), fontName="Helvetica", alignment=TA_CENTER, spaceAfter=2)
META       = ms("M",   fontSize=8,  textColor=colors.HexColor("#AACCFF"), fontName="Helvetica", alignment=TA_CENTER)
SEC_TITLE  = ms("STi", fontSize=13, textColor=WHITE,    fontName="Helvetica-Bold", spaceAfter=3)
H2         = ms("H2",  fontSize=11, textColor=SAP_DARK, fontName="Helvetica-Bold", spaceAfter=4, spaceBefore=8)
BODY       = ms("B",   fontSize=8.5,textColor=BLACK,    leading=13, spaceAfter=3, alignment=TA_JUSTIFY)
BODY_SML   = ms("BS",  fontSize=8,  textColor=BLACK,    leading=12, spaceAfter=2)
QUOTE_S    = ms("QS",  fontSize=8.5,textColor=DARK_GREY,fontName="Helvetica-Oblique", leading=13, leftIndent=10, spaceAfter=3)
BULLET_HDR = ms("BH",  fontSize=9,  textColor=WHITE,    fontName="Helvetica-Bold", alignment=TA_CENTER)
BULLET_TXT = ms("BT",  fontSize=8,  textColor=BLACK,    leading=12, spaceAfter=1)
WARN_TXT   = ms("WT",  fontSize=8,  textColor=RED,      fontName="Helvetica-Bold", leading=12, spaceAfter=1)
OK_TXT     = ms("OT",  fontSize=8,  textColor=GREEN_OK, fontName="Helvetica-Bold", leading=12, spaceAfter=1)
TH         = ms("TH",  fontSize=8,  textColor=WHITE,    fontName="Helvetica-Bold", alignment=TA_CENTER)
TC         = ms("TC",  fontSize=8,  textColor=BLACK,    leading=11)
LABEL      = ms("LB",  fontSize=7.5,textColor=SAP_DARK, fontName="Helvetica-Bold")
NUM_BIG    = ms("NB",  fontSize=28, textColor=WHITE,    fontName="Helvetica-Bold", alignment=TA_CENTER)

def sp(n=6): return Spacer(1, n)

# ── Helpers ───────────────────────────────────────────────────────────────────
def sec_hdr(number, title, subtitle, hdr_color=SAP_DARK, sub_color=None):
    if not sub_color:
        sub_color = hdr_color
    num_cell   = Table([[Paragraph(str(number), NUM_BIG)]], colWidths=[1.6*cm], rowHeights=[1.4*cm])
    num_cell.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), sub_color),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0),(-1,-1), 0),
        ("BOTTOMPADDING", (0,0),(-1,-1), 0),
    ]))
    title_cell = Table([
        [Paragraph(title, SEC_TITLE)],
        [Paragraph(subtitle, ms(f"sub{number}", fontSize=8, textColor=colors.HexColor("#AACCFF"),
                                fontName="Helvetica-Oblique"))],
    ], colWidths=[15.9*cm])
    title_cell.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), hdr_color),
        ("TOPPADDING",    (0,0),(-1,-1), 6),
        ("BOTTOMPADDING", (0,0),(-1,-1), 6),
        ("LEFTPADDING",   (0,0),(-1,-1), 12),
    ]))
    t = Table([[num_cell, title_cell]], colWidths=[1.6*cm, 15.9*cm])
    t.setStyle(TableStyle([
        ("LEFTPADDING",  (0,0),(-1,-1), 0),
        ("RIGHTPADDING", (0,0),(-1,-1), 0),
        ("TOPPADDING",   (0,0),(-1,-1), 0),
        ("BOTTOMPADDING",(0,0),(-1,-1), 0),
        ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
    ]))
    return t

def highlight_cards(items, bg=SAP_LIGHT, border=SAP_BLUE, icon="⚑"):
    """items = list of (heading, body_text)"""
    rows = []
    for heading, body in items:
        card = Table([[
            Paragraph(f"<b>{icon}  {heading}</b>", ms(f"ch{heading[:5]}", fontSize=8.5,
                      textColor=border, fontName="Helvetica-Bold")),
            Paragraph(body, BODY_SML)
        ]], colWidths=[4.5*cm, 13*cm])
        card.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(0,0),  bg),
            ("BACKGROUND",    (1,0),(1,0),  WHITE),
            ("LINEABOVE",     (0,0),(-1,0), 0.5, border),
            ("LINEBELOW",     (0,0),(-1,0), 0.5, GREY_BORDER),
            ("LINEBEFORE",    (0,0),(0,0),  3,   border),
            ("TOPPADDING",    (0,0),(-1,-1), 5),
            ("BOTTOMPADDING", (0,0),(-1,-1), 5),
            ("LEFTPADDING",   (0,0),(-1,-1), 8),
            ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ]))
        rows.append(card)
        rows.append(sp(4))
    return rows

def warn_card(text, label="⚠  Watch Out"):
    t = Table([[
        Paragraph(label, ms("wl", fontSize=8, textColor=WHITE, fontName="Helvetica-Bold")),
        Paragraph(text, ms("wb", fontSize=8, textColor=BLACK, leading=12))
    ]], colWidths=[2.8*cm, 14.7*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(0,0),  RED),
        ("BACKGROUND",    (1,0),(1,0),  RED_LIGHT),
        ("TOPPADDING",    (0,0),(-1,-1), 6),
        ("BOTTOMPADDING", (0,0),(-1,-1), 6),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ]))
    return t

def ok_card(text, label="✓  Remember"):
    t = Table([[
        Paragraph(label, ms("ol", fontSize=8, textColor=WHITE, fontName="Helvetica-Bold")),
        Paragraph(text, ms("ob", fontSize=8, textColor=BLACK, leading=12))
    ]], colWidths=[2.8*cm, 14.7*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(0,0),  GREEN_OK),
        ("BACKGROUND",    (1,0),(1,0),  GREEN_LIGHT),
        ("TOPPADDING",    (0,0),(-1,-1), 6),
        ("BOTTOMPADDING", (0,0),(-1,-1), 6),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ]))
    return t

def quote_box(text, speaker=""):
    content = f'"{text}"'
    if speaker:
        content += f"  — <i>{speaker}</i>"
    t = Table([[Paragraph(content, QUOTE_S)]], colWidths=[17.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), GOLD_LIGHT),
        ("LINEBEFORE",   (0,0),(0,-1),  4, GOLD),
        ("TOPPADDING",   (0,0),(-1,-1), 7),
        ("BOTTOMPADDING",(0,0),(-1,-1), 7),
        ("LEFTPADDING",  (0,0),(-1,-1), 14),
        ("RIGHTPADDING", (0,0),(-1,-1), 10),
    ]))
    return t

def pill_row(pills, colors_list):
    """Horizontal row of coloured pill badges"""
    cells = []
    for text, bg in zip(pills, colors_list):
        p = Table([[Paragraph(text, ms(f"pi{text[:3]}", fontSize=7.5, textColor=WHITE,
                   fontName="Helvetica-Bold", alignment=TA_CENTER))]],
                  colWidths=[(17.5/len(pills))*cm])
        p.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), bg),
            ("TOPPADDING",    (0,0),(-1,-1), 5),
            ("BOTTOMPADDING", (0,0),(-1,-1), 5),
            ("LEFTPADDING",   (0,0),(-1,-1), 4),
            ("RIGHTPADDING",  (0,0),(-1,-1), 4),
        ]))
        cells.append(p)
    t = Table([cells], colWidths=[(17.5/len(pills))*cm]*len(pills))
    t.setStyle(TableStyle([
        ("LEFTPADDING",  (0,0),(-1,-1), 1),
        ("RIGHTPADDING", (0,0),(-1,-1), 1),
        ("TOPPADDING",   (0,0),(-1,-1), 0),
        ("BOTTOMPADDING",(0,0),(-1,-1), 0),
    ]))
    return t

def tbl(headers, rows, widths=None):
    n = len(headers)
    if not widths:
        widths = [17.5*cm/n]*n
    data = [[Paragraph(h, TH) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), TC) for c in row])
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",     (0,0), (-1,0),  SAP_BLUE),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, GREY_BG]),
        ("GRID",           (0,0), (-1,-1), 0.4, GREY_BORDER),
        ("TOPPADDING",     (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",  (0,0), (-1,-1), 5),
        ("LEFTPADDING",    (0,0), (-1,-1), 6),
        ("VALIGN",         (0,0), (-1,-1), "TOP"),
    ]))
    return t

# ── Cover ─────────────────────────────────────────────────────────────────────
def cover():
    els = []
    cov = Table([
        [Paragraph("GxP Mandatory Training", TITLE)],
        [Paragraph("Key Implementation Highlights for Developers", SUBTITLE)],
        [Paragraph("SAP Advanced Therapy Orchestration (ATO/CGT)  |  BTP Platform", SUBTITLE)],
        [Paragraph("Based on: GxP Training for CGT-TMP Team (2022-02-14)  |  Trainers: Mukul &amp; Robin", META)],
        [Paragraph("Prepared: 2026-06-26  |  Audience: All developers and testers touching the system", META)],
    ], colWidths=[17.5*cm])
    cov.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), SAP_DARK),
        ("TOPPADDING",    (0,0),(-1,-1), 32),
        ("BOTTOMPADDING", (0,0),(-1,-1), 32),
        ("LEFTPADDING",   (0,0),(-1,-1), 20),
    ]))
    els.append(cov)
    els.append(sp(16))

    # section map
    els.append(Paragraph("What This Document Covers", H2))
    section_pills = [
        ("1. Why GxP Matters",        SAP_DARK),
        ("2. GxP Basics",             SAP_BLUE),
        ("3. 21 CFR Part 11",         RED),
        ("4. Data Integrity",         ORANGE),
        ("5. BTP Infrastructure",     BTP_GREEN),
        ("6. Qualification Docs",     PURPLE),
        ("7. Client Agreements",      TEAL),
        ("8. Dev Rules",              colors.HexColor("#333333")),
    ]
    els.append(pill_row([p[0] for p in section_pills], [p[1] for p in section_pills]))
    els.append(sp(14))

    els.append(warn_card(
        "This training is MANDATORY. Every developer and tester who touches the system must "
        "complete it. Attendance is logged and is itself a GxP record — regulators can request "
        "to see training records during an audit.",
        label="⚠  Mandatory"
    ))
    els.append(sp(8))
    els.append(quote_box(
        "When you are building a CGT platform, when you are running against timeline, these are "
        "very painful. But put yourself in that place — when we are trying to take a drug to a "
        "patient, was it doing these activities or not?",
        speaker="Mukul, GxP Compliance Lead"
    ))
    els.append(PageBreak())
    return els

# ── Section 1: Why GxP ────────────────────────────────────────────────────────
def section1():
    els = []
    els.append(sec_hdr(1, "Why GxP Matters for ATO/CGT Developers",
                       "The reason compliance is non-negotiable in this platform", SAP_DARK))
    els.append(sp(10))

    els += highlight_cards([
        ("Patient Safety First",
         "The ATO platform moves clinical trial data and patient treatment data across supply chains. "
         "This data DIRECTLY drives which drug a patient receives and how it is manufactured. "
         "Incorrect data = incorrect drug = patient harm or death."),
        ("IT Systems Must Match Manual Controls",
         "When IT platforms replaced manual processes, regulators required the SAME level of "
         "controls — traceability, attribution, integrity — that existed in paper-based processes. "
         "IT systems must deliver these controls AND more."),
        ("You Are Building a GxP-Regulated System",
         "Every feature you build, every API you write, every table you design is part of a "
         "GxP-regulated system. Compliance is not a post-delivery task — it must be designed in "
         "from the start."),
        ("Non-Compliance Has Legal Consequences",
         "Clients like Roche, Novartis, Gilead sign quality agreements with SAP. They can conduct "
         "announced AND unannounced audits. If your system fails an audit, SAP is liable. "
         "Individual developers are accountable through access records and audit logs."),
    ], bg=SAP_LIGHT, border=SAP_DARK, icon="▸")

    els.append(sp(6))
    els.append(warn_card(
        "Time pressure is NOT a valid reason to skip compliance activities. "
        "Every policy shortcut is itself a compliance violation and is recorded. "
        "If you are challenged for time, escalate — do not short-circuit the process."
    ))
    els.append(PageBreak())
    return els

# ── Section 2: GxP Basics ─────────────────────────────────────────────────────
def section2():
    els = []
    els.append(sec_hdr(2, "GxP Basics — What the 5 Pillars Mean for Your Code",
                       "Every line of code touches at least one of these pillars", SAP_BLUE))
    els.append(sp(10))

    els.append(tbl(
        ["Pillar", "What It Means for Developers", "Implementation Examples"],
        [
            ["Quality Management",
             "Every process you follow in SDLC must be documented. Risk assessments before development. Qualification standards for testing.",
             "Risk assessment doc before sprint. Test plan for each feature. Qualification docs for infrastructure."],
            ["Change Management",
             "Every change to a regulated system must be controlled, tested with evidence, and traceable.",
             "No direct prod hotfixes. Every change linked to a test case. Evidence collected before deployment."],
            ["Access Management",
             "Only authorised users access regulated parts. Role-based access. Identity records maintained.",
             "RBAC implemented for all regulated transactions. No shared credentials. Access logs retained."],
            ["Data Integrity",
             "All regulated data changes must be traceable — who changed what, when, old value, new value. 90% of audits focus here.",
             "Change Document Framework for CDHDR/CDPOS. Audit logs for every regulated field change. Data encryption at rest and in transit."],
            ["Training & Education",
             "All personnel touching the system must be trained. Training is logged and auditable.",
             "This training session. Attendance record kept. Refreshers when regulations change."],
        ],
        widths=[3.5*cm, 7*cm, 7*cm]
    ))
    els.append(sp(8))
    els.append(ok_card(
        "If you are unsure whether a feature impacts a regulated process — ask the GxP compliance "
        "team BEFORE building it, not after. Retrofitting compliance is far more expensive."
    ))
    els.append(PageBreak())
    return els

# ── Section 3: 21 CFR Part 11 ─────────────────────────────────────────────────
def section3():
    els = []
    els.append(sec_hdr(3, "21 CFR Part 11 — What Developers Must Build",
                       "Electronic records and eSignature — decoded for implementation", RED))
    els.append(sp(10))

    els += highlight_cards([
        ("eSignature ≠ Fancy Technology",
         "In regulatory terms, eSignature = proving who took a decision, when, why, in an irrefutable way. "
         "A SAP user ID + password re-entry for a critical transaction is FULLY GxP-compliant. "
         "Biometrics (Pfizer, Roche) are optional enhancements — NOT requirements."),
        ("What MUST Trigger eSignature",
         "Releasing a product. Moving product between stakeholders. Any action impacting patient safety. "
         "Changes to regulated fields (Therapy Type, Clinical Study, Protocol, Patient Reference). "
         "Rule: if a wrong decision here could harm a patient → eSignature required."),
        ("What Does NOT Need eSignature",
         "Display-only activities (user just viewing data). Background/system job activities "
         "(automated processes run by system users — EXCLUDED by GxP rules). Non-regulated field changes "
         "(e.g. payment terms, delivery date)."),
        ("Logging Rule for Authentication",
         "If a user action enables a call that may impact patient safety → the authentication must be "
         "stored in a log. Display-only access → no logging required. Rule: patient safety impact = log it."),
    ], bg=RED_LIGHT, border=RED, icon="▸")

    els.append(sp(6))
    els.append(quote_box(
        "Even if it is ID and a simple password for a critical transaction — they are more than happy, "
        "as long as you follow those.",
        speaker="Mukul — confirming SAP password re-entry is GxP-compliant"
    ))
    els.append(sp(6))

    els.append(Paragraph("Electronic Records Requirements — Build These Into Your Design", H2))
    els.append(tbl(
        ["Requirement", "What to Build", "Do NOT"],
        [
            ["Secured",        "Data cannot be changed without leaving a trace — Change Document Framework", "Allow direct table updates without audit trail"],
            ["Attributed",     "Every record traceable to who created/modified it — USERNAME in CDHDR", "Use shared service accounts for regulated transactions"],
            ["Contemporaneous","Timestamped at time of action — UDATE + UTIME in CDHDR", "Allow backdating or timestamp manipulation"],
            ["Original",       "First capture or verified true copy of the data", "Overwrite without keeping old value — use CDPOS VALUE_OLD"],
            ["Accurate",       "Data matches physical/clinical reality — validation at entry point", "Accept unvalidated external data without boundary check"],
        ],
        widths=[3.5*cm, 7.5*cm, 6.5*cm]
    ))
    els.append(PageBreak())
    return els

# ── Section 4: Data Integrity ─────────────────────────────────────────────────
def section4():
    els = []
    els.append(sec_hdr(4, "Data Integrity — ALCOA+ in Code",
                       "90% of regulatory audits focus here — design it in from day one", ORANGE))
    els.append(sp(10))

    # ALCOA pills
    alcoa_items = [
        ("A — Attributable",   SAP_DARK,  "Who created/changed it",   "USERNAME in every log record"),
        ("L — Legible",        SAP_BLUE,  "Readable and permanent",    "No deletable audit records"),
        ("C — Contemporaneous",ORANGE,    "Timestamped at occurrence", "UDATE+UTIME at point of save"),
        ("O — Original",       BTP_GREEN, "First capture / true copy", "VALUE_OLD preserved in CDPOS"),
        ("A — Accurate",       PURPLE,    "No errors or deviations",   "Validate at data entry point"),
        ("+ Complete",         TEAL,      "Full lifecycle covered",    "Generation through archiving"),
    ]
    header_row = [Paragraph(a[0], ms(f"ah{i}", fontSize=7.5, textColor=WHITE,
                  fontName="Helvetica-Bold", alignment=TA_CENTER))
                  for i, a in enumerate(alcoa_items)]
    meaning_row = [Paragraph(a[2], ms(f"am{i}", fontSize=7, textColor=BLACK,
                   alignment=TA_CENTER, leading=10))
                   for i, a in enumerate(alcoa_items)]
    impl_row = [Paragraph(a[3], ms(f"ai{i}", fontSize=7, textColor=DARK_GREY,
                fontName="Helvetica-Oblique", alignment=TA_CENTER, leading=10))
                for i, a in enumerate(alcoa_items)]

    at = Table([header_row, meaning_row, impl_row],
               colWidths=[17.5*cm/6]*6)
    bg_list = [a[1] for a in alcoa_items]
    style = [
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
        ("LEFTPADDING",   (0,0),(-1,-1), 3),
        ("GRID",          (0,0),(-1,-1), 0.3, GREY_BORDER),
        ("BACKGROUND",    (1,1),(-1,-1), GREY_BG),
    ]
    for i, bg in enumerate(bg_list):
        style.append(("BACKGROUND", (i,0),(i,0), bg))
    at.setStyle(TableStyle(style))
    els.append(at)
    els.append(sp(10))

    els += highlight_cards([
        ("Data Lifecycle — ALL stages matter",
         "Generation → Processing → Storage → Retrieval → ARCHIVING. "
         "Archiving is equally critical. Regulators ask: how long is data retained? Can you recover it? "
         "Design data archiving and retention policies from the start — not as an afterthought."),
        ("External Data Sources",
         "GxP-relevant external data: ask the provider to validate. "
         "If provider cannot validate: at YOUR data entry point (interface/data hub), verify that "
         "data received exactly matches data sent. Once verified — your responsibility ends. "
         "Document this boundary check."),
        ("Data Corruption = Patient Risk",
         "Millions of records flow through ATO for many clients. Data swapped or corrupted for a "
         "patient-specific cell therapy = adverse outcome = potential death. "
         "Regulators go to the Nth level to find root cause. Without audit logs → impossible to defend."),
    ], bg=ORANGE_LIGHT, border=ORANGE, icon="▸")

    els.append(sp(6))
    els.append(warn_card(
        "Data integrity covers more than the database. Change control process, batch records, "
        "shipping records, stakeholder transfer records — ALL are data integrity. "
        "Regulators ask about ALL of these during audits."
    ))
    els.append(PageBreak())
    return els

# ── Section 5: BTP Infrastructure ────────────────────────────────────────────
def section5():
    els = []
    els.append(sec_hdr(5, "BTP Infrastructure Qualification",
                       "Cloud Service Qualification (CSQ) — how SAP keeps BTP GxP-compliant", BTP_GREEN))
    els.append(sp(10))

    els += highlight_cards([
        ("Shared Responsibility Model",
         "Client (Roche/Novartis/Gilead): validates their processes, interfaces, identity mgmt. "
         "SAP (SaaS vendor): qualifies the ATO application and BTP infrastructure layer. "
         "SAP BTP (PaaS): provides HANA, Workflow, Portal, Event Mesh — updates every 1-2 weeks. "
         "YOU as a developer: ensure your code does not break the qualification assumptions."),
        ("Why CSQ Exists",
         "BTP services release hundreds of feature updates, security fixes, hot fixes continuously. "
         "It is impossible to review each individual change. Instead: define what you REQUIRE from each "
         "BTP service (intended use), then continuously test those requirements are still met. "
         "Deviation from expected behavior → escalate immediately."),
        ("Continuous Verification — What It Means for Your Code",
         "Automated tests run every 5 minutes / hourly / daily verify BTP service behavior. "
         "Your solution components must have: defined intended use per BTP service, test cases "
         "linked to those requirements, deviation handling procedures. "
         "Traceability from SaaS application → solution component → BTP service → test evidence."),
        ("Data Encryption — Non-Negotiable",
         "21 CFR Part 11 + open system consideration (BTP is an open system): "
         "data encryption at rest = MANDATORY for all electronic records. "
         "Data encryption in transit = MANDATORY. "
         "Do not store regulated data unencrypted at any layer."),
    ], bg=BTP_LIGHT, border=BTP_GREEN, icon="▸")

    els.append(sp(6))
    els.append(tbl(
        ["BTP Requirement", "Why Mandatory", "How Demonstrated"],
        [
            ["Data encryption at rest",      "21 CFR Part 11 + open system rule", "BTP HANA encryption config + CSQ evidence"],
            ["Data encryption in transit",   "Electronic records in transit must be secured", "TLS/HTTPS enforced — no plain HTTP"],
            ["Backup and restore",           "Regulators ask: can you recover data? How quickly?", "BTP backup config + tested restore procedure"],
            ["ISO 27001 certificate",        "Baseline security assurance for BTP platform", "SAP BTP trust center documentation"],
            ["SOC 2 Type 2 controls",        "Independent audit of security controls", "SAP BTP SOC 2 report — useful but not sufficient alone"],
            ["Change management for BTP",    "Uncontrolled platform changes = compliance gap", "CSQ continuous testing + deviation handling"],
        ],
        widths=[5*cm, 6.5*cm, 6*cm]
    ))
    els.append(PageBreak())
    return els

# ── Section 6: Qualification Docs ────────────────────────────────────────────
def section6():
    els = []
    els.append(sec_hdr(6, "Qualification Documents — What Clients Will Ask For",
                       "If you cannot show it, it did not happen — document everything", PURPLE))
    els.append(sp(10))

    els.append(tbl(
        ["Document", "What It Contains", "Who Asks For It"],
        [
            ["Traceability Matrix",   "Epic → User Story → Requirements → Test Scripts → Test Results → Prod deployment. Every change linked to a test case.", "FIRST thing clients ask — most critical"],
            ["Risk Assessment",       "GAMP5-based: critical components, failure scenarios, severity, detectability. Conducted before development.", "Clients + regulators in audit"],
            ["Design Specification",  "Documents the design approach and technical decisions.", "Clients during audit prep"],
            ["Test Plan",             "How testing is conducted, who, when, what scope, what evidence collected.", "Clients + internal QA"],
            ["Validation Report",     "Summary report generated after ALL testing activities complete. Final evidence package.", "Submitted to client before go-live"],
            ["IQ / OQ / PQ Docs",     "Infrastructure Qualification (IQ), Operational (OQ), Performance (PQ) — confirm system works as intended at infrastructure level.", "Clients operating in regulated markets"],
            ["Training Records",      "Who was trained, when, on what topic. This session is one record.", "Regulators — 21 CFR Part 11 mandates training for all authorized users"],
        ],
        widths=[4*cm, 8.5*cm, 5*cm]
    ))
    els.append(sp(8))

    els += highlight_cards([
        ("Traceability Matrix — Build It as You Go",
         "Do NOT create the traceability matrix at the end of a sprint. "
         "Link each user story → requirement → test case → test result → deployment as you develop. "
         "Retroactive creation is flagged by auditors as a compliance risk."),
        ("Validation Report — Generated, Not Written",
         "The validation report is generated by compiling all preceding evidence — design spec, "
         "test plan, test results, risk assessment. If you keep the artefacts current, "
         "the report writes itself. If you skip artefacts, you cannot generate the report."),
    ], bg=PURPLE_LIGHT, border=PURPLE, icon="▸")

    els.append(sp(6))
    els.append(quote_box(
        "Any change which goes into your platform — is it linked to a test case? How have you "
        "tested it? What are the activities? Right from epic, user story, to your requirements, "
        "to your test scripts and test results — that is the traceability matrix.",
        speaker="Mukul"
    ))
    els.append(PageBreak())
    return els

# ── Section 7: Client Agreements ─────────────────────────────────────────────
def section7():
    els = []
    els.append(sec_hdr(7, "Quality Agreements with Life Science Clients",
                       "What Roche, Novartis, Gilead, Pfizer expect from SAP", TEAL))
    els.append(sp(10))

    els += highlight_cards([
        ("Quality Agreement is Mandatory",
         "Every major Life Science client — Roche, Novartis, Gilead, Pfizer, Sanofi, Merck — "
         "requires a Quality Agreement SEPARATE from the commercial contract. "
         "This agreement defines exactly what GxP requirements SAP must fulfill."),
        ("Two Types of Audits — Be Ready for Both",
         "ANNOUNCED: client notifies SAP in advance — typically scheduled annually. "
         "UNANNOUNCED: client can walk in at any time without notice. "
         "The evidence package (documentation, audit logs, test results) must be ready ON DEMAND "
         "— not assembled after the audit is announced."),
        ("No External Certificate Required",
         "GxP compliance is SELF-ASSESSMENT backed by evidence. SOC 2 Type 2 is useful but "
         "not sufficient on its own — clients want to SEE the documentation, the audit logs, "
         "the traceability matrix, the test evidence. No third party certifies you as GxP compliant."),
        ("Chain of Identity and Chain of Custody",
         "For CGT/ATO specifically: client's most critical requirement is tracing chain of identity "
         "(which patient's cells) and chain of custody (who had the product at every step). "
         "These are the primary regulatory drivers for all ATO field extensions and audit trail requirements."),
    ], bg=TEAL_LIGHT, border=TEAL, icon="▸")

    els.append(PageBreak())
    return els

# ── Section 8: Dev Rules ──────────────────────────────────────────────────────
def section8():
    els = []
    els.append(sec_hdr(8, "8 Key Rules for Developers",
                       "Commit these to memory — they apply to every sprint, every story", colors.HexColor("#333333")))
    els.append(sp(10))

    rules = [
        (RED,      "No Shortcuts on Policies",
                   "Follow all policies and procedures even under time pressure. Everything is recorded. "
                   "Short-circuiting a compliance process is itself a violation."),
        (RED,      "Escalate Incidents Immediately",
                   "If you find a deviation, incident, or compliance gap — escalate, document, and regularize it. "
                   "Do NOT ignore or work around it. Undisclosed incidents are far worse than disclosed ones."),
        (ORANGE,   "Every Change Linked to a Test Case",
                   "No story goes to production without a linked test case and test evidence. "
                   "Traceability matrix is not optional — it is the first thing clients ask for."),
        (ORANGE,   "Audit Trail for ALL Regulated Changes",
                   "Who changed what, when, old value, new value. For ATO: this means CDHDR + CDPOS "
                   "for every change to Therapy Type, Clinical Study, Protocol, Patient Reference fields."),
        (SAP_BLUE, "Access Control is Not Optional",
                   "Only authorized users access regulated parts of the system. No shared accounts. "
                   "Access records must be maintained and auditable."),
        (SAP_BLUE, "Data Encryption at Rest and in Transit",
                   "Not optional for electronic records. BTP open system = encryption mandatory. "
                   "Do not store regulated data unencrypted at any layer."),
        (BTP_GREEN,"Background Jobs Are Excluded from eSignature",
                   "System/technical user processes do not require reauthentication. "
                   "Only human user-triggered critical transactions require re-authentication. "
                   "Build this exclusion logic into the Relevancy Check callback."),
        (BTP_GREEN,"Training is a GxP Record",
                   "Attendance at this training is itself a regulated record. Keep records of who was "
                   "trained, when, and on what. When team members join, ensure they complete training "
                   "before accessing the system."),
    ]

    for i, (color, heading, body) in enumerate(rules):
        num_cell = Table([[Paragraph(str(i+1), ms(f"rn{i}", fontSize=16, textColor=WHITE,
                          fontName="Helvetica-Bold", alignment=TA_CENTER))]],
                         colWidths=[0.9*cm], rowHeights=[1*cm])
        num_cell.setStyle(TableStyle([
            ("BACKGROUND", (0,0),(-1,-1), color),
            ("VALIGN",     (0,0),(-1,-1), "MIDDLE"),
        ]))
        text_cell = Table([
            [Paragraph(heading, ms(f"rh{i}", fontSize=9, textColor=color,
                       fontName="Helvetica-Bold"))],
            [Paragraph(body, BODY_SML)],
        ], colWidths=[16.6*cm])
        text_cell.setStyle(TableStyle([
            ("TOPPADDING",    (0,0),(-1,-1), 4),
            ("BOTTOMPADDING", (0,0),(-1,-1), 4),
            ("LEFTPADDING",   (0,0),(-1,-1), 10),
            ("LINEBELOW",     (0,0),(0,0),   0.3, GREY_BORDER),
        ]))
        row_t = Table([[num_cell, text_cell]], colWidths=[0.9*cm, 16.6*cm])
        row_t.setStyle(TableStyle([
            ("LINEABOVE",    (0,0),(-1,0),  0.5, color),
            ("LINEBELOW",    (0,0),(-1,0),  0.5, GREY_BORDER),
            ("TOPPADDING",   (0,0),(-1,-1), 0),
            ("BOTTOMPADDING",(0,0),(-1,-1), 0),
            ("LEFTPADDING",  (0,0),(-1,-1), 0),
            ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
        ]))
        els.append(row_t)
        els.append(sp(5))

    els.append(sp(10))

    # mapping to 2026 work
    els.append(Paragraph("2022 Training → 2026 Implementation Mapping", H2))
    els.append(tbl(
        ["Training Requirement (2022)", "2026 Implementation"],
        [
            ["eSignature for regulated changes",            "Reauthentication Framework + BTP eSignature SaaS"],
            ["Audit trail — who, what, when, old/new",      "Change Document Framework — CDHDR + CDPOS (verified 2608)"],
            ["ID + password re-entry is GxP-compliant",     "SAP password re-entry in reauthentication dialog — fully compliant"],
            ["Reason for change must be captured",          "Reason Code in reauthentication dialog (configured in BTP)"],
            ["System/background jobs excluded",             "Reauthentication framework skips system-user triggered saves"],
            ["Signature linked to change record",           "BTP Signature ID ↔ CHANGENR link in CDHDR"],
            ["Traceability matrix mandatory",               "Epic → Story → Test Case → Test Result → CDHDR CHANGENR"],
        ],
        widths=[8.5*cm, 9*cm]
    ))
    return els

# ── Build ─────────────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title="GxP Training — Implementation Highlights",
        author="SAP ATO GxP Team",
    )

    story = []
    story.extend(cover())
    story.extend(section1())
    story.extend(section2())
    story.extend(section3())
    story.extend(section4())
    story.extend(section5())
    story.extend(section6())
    story.extend(section7())
    story.extend(section8())

    def on_page(c, doc):
        c.saveState()
        c.setFont("Helvetica", 7)
        c.setFillColor(colors.HexColor("#888888"))
        c.drawString(2*cm, 1.2*cm, "GxP Mandatory Training — Implementation Highlights for Developers")
        c.drawRightString(19.5*cm, 1.2*cm, f"Page {doc.page}")
        c.setStrokeColor(GREY_BORDER)
        c.setLineWidth(0.4)
        c.line(2*cm, 1.5*cm, 19.5*cm, 1.5*cm)
        c.restoreState()

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF created: {OUTPUT}")

build()
