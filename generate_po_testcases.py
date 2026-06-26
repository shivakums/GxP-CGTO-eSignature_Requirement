from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUTPUT = r"C:\Users\I308878\GxP-CGTO-eSignature_Requirement\GxP_ATO_PO_ChangeDoc_TestCases.pdf"

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
CODE_BG       = colors.HexColor("#1E1E2E")
CODE_FG       = colors.HexColor("#CDD6F4")
WHITE         = colors.white
BLACK         = colors.black
DARK_GREY     = colors.HexColor("#444444")

W, H = A4

# ── Styles ────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()
def ms(name, **kw):
    return ParagraphStyle(name=name, parent=styles["Normal"], **kw)

TITLE     = ms("T",  fontSize=20, textColor=WHITE,    fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=4)
SUBTITLE  = ms("ST", fontSize=10, textColor=colors.HexColor("#AACCFF"), fontName="Helvetica", alignment=TA_CENTER, spaceAfter=2)
META      = ms("M",  fontSize=8,  textColor=colors.HexColor("#AACCFF"), fontName="Helvetica", alignment=TA_CENTER)
H1        = ms("H1", fontSize=13, textColor=WHITE,    fontName="Helvetica-Bold", spaceAfter=3)
H2        = ms("H2", fontSize=11, textColor=SAP_DARK, fontName="Helvetica-Bold", spaceAfter=4, spaceBefore=8)
H3        = ms("H3", fontSize=9,  textColor=SAP_BLUE, fontName="Helvetica-Bold", spaceAfter=3, spaceBefore=5)
BODY      = ms("B",  fontSize=8.5,textColor=BLACK,    leading=13, spaceAfter=3, alignment=TA_JUSTIFY)
BODY_SML  = ms("BS", fontSize=8,  textColor=BLACK,    leading=12, spaceAfter=2)
STEP_NUM  = ms("SN", fontSize=14, textColor=WHITE,    fontName="Helvetica-Bold", alignment=TA_CENTER)
STEP_TIT  = ms("STt",fontSize=10, textColor=WHITE,    fontName="Helvetica-Bold")
STEP_SUB  = ms("SSb",fontSize=8,  textColor=colors.HexColor("#AACCFF"), fontName="Helvetica-Oblique")
CODE_S    = ms("CS", fontSize=7.5,textColor=CODE_FG,  fontName="Courier", leading=11, spaceAfter=1)
TH        = ms("TH", fontSize=8,  textColor=WHITE,    fontName="Helvetica-Bold", alignment=TA_CENTER)
TC        = ms("TC", fontSize=8,  textColor=BLACK,    leading=11)
BULL      = ms("BU", fontSize=8.5,textColor=BLACK,    leading=13, leftIndent=10, spaceAfter=2)
RESULT_OK = ms("RO", fontSize=8,  textColor=GREEN_OK, fontName="Helvetica-Bold", leading=12)
RESULT_WA = ms("RW", fontSize=8,  textColor=GOLD,     fontName="Helvetica-Bold", leading=12)
RESULT_ER = ms("RE", fontSize=8,  textColor=RED,      fontName="Helvetica-Bold", leading=12)

def sp(n=6): return Spacer(1, n)

# ── Helpers ───────────────────────────────────────────────────────────────────
def sec_hdr(title, subtitle="", color=SAP_DARK):
    rows = [[Paragraph(title, H1)]]
    if subtitle:
        rows.append([Paragraph(subtitle, STEP_SUB)])
    t = Table(rows, colWidths=[17.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), color),
        ("TOPPADDING",    (0,0),(-1,-1), 9),
        ("BOTTOMPADDING", (0,0),(-1,-1), 9),
        ("LEFTPADDING",   (0,0),(-1,-1), 14),
    ]))
    return t

def tbl(headers, rows, widths=None):
    n = len(headers)
    if not widths: widths = [17.5*cm/n]*n
    data = [[Paragraph(h, TH) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), TC) for c in row])
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",     (0,0),(-1,0),  SAP_BLUE),
        ("ROWBACKGROUNDS", (0,1),(-1,-1), [WHITE, GREY_BG]),
        ("GRID",           (0,0),(-1,-1), 0.4, GREY_BORDER),
        ("TOPPADDING",     (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",  (0,0),(-1,-1), 5),
        ("LEFTPADDING",    (0,0),(-1,-1), 6),
        ("VALIGN",         (0,0),(-1,-1), "TOP"),
    ]))
    return t

def info_box(text, bg=SAP_LIGHT, border=SAP_BLUE):
    t = Table([[Paragraph(text, BODY_SML)]], colWidths=[17.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), bg),
        ("LINEABOVE",    (0,0),(-1,0),  2, border),
        ("TOPPADDING",   (0,0),(-1,-1), 7),
        ("BOTTOMPADDING",(0,0),(-1,-1), 7),
        ("LEFTPADDING",  (0,0),(-1,-1), 12),
        ("RIGHTPADDING", (0,0),(-1,-1), 8),
    ]))
    return t

def warn_box(text): return info_box(text, bg=RED_LIGHT, border=RED)
def ok_box(text):   return info_box(text, bg=GREEN_LIGHT, border=GREEN_OK)
def note_box(text): return info_box(text, bg=GOLD_LIGHT, border=GOLD)

def code_block(lines):
    rows = [[Paragraph(
        l.replace(" ","&nbsp;").replace("<","&lt;").replace(">","&gt;") or "&nbsp;",
        CODE_S)] for l in lines]
    t = Table(rows, colWidths=[17.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), CODE_BG),
        ("TOPPADDING",    (0,0),(-1,-1), 6),
        ("BOTTOMPADDING", (0,0),(-1,-1), 6),
        ("LEFTPADDING",   (0,0),(-1,-1), 10),
        ("RIGHTPADDING",  (0,0),(-1,-1), 6),
    ]))
    return t

def step_card(number, title, system, steps_rows, verify_rows,
              expected, status_label="", status_color=SAP_BLUE,
              open_issue=None):
    """steps_rows = list of (action, detail). verify_rows = list of (where, what)"""
    els = []

    # Header
    num_t = Table([[Paragraph(str(number), STEP_NUM)]],
                  colWidths=[1.4*cm], rowHeights=[1.2*cm])
    num_t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), status_color),
        ("VALIGN",    (0,0),(-1,-1),"MIDDLE"),
    ]))
    title_t = Table([
        [Paragraph(title, STEP_TIT)],
        [Paragraph(f"System: {system}  {('  |  ' + status_label) if status_label else ''}",
                   STEP_SUB)],
    ], colWidths=[16.1*cm])
    title_t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), status_color),
        ("TOPPADDING",   (0,0),(-1,-1), 8),
        ("BOTTOMPADDING",(0,0),(-1,-1), 8),
        ("LEFTPADDING",  (0,0),(-1,-1), 12),
    ]))
    hdr = Table([[num_t, title_t]], colWidths=[1.4*cm, 16.1*cm])
    hdr.setStyle(TableStyle([
        ("TOPPADDING",   (0,0),(-1,-1),0),
        ("BOTTOMPADDING",(0,0),(-1,-1),0),
        ("LEFTPADDING",  (0,0),(-1,-1),0),
        ("VALIGN",       (0,0),(-1,-1),"MIDDLE"),
    ]))
    els.append(hdr)

    # Steps table
    step_data = [[Paragraph("Step", TH),
                  Paragraph("Action", TH),
                  Paragraph("Detail / Input", TH)]]
    for i, (action, detail) in enumerate(steps_rows):
        step_data.append([
            Paragraph(str(i+1), ms(f"sn{number}{i}", fontSize=9, textColor=SAP_BLUE,
                      fontName="Helvetica-Bold", alignment=TA_CENTER)),
            Paragraph(action, ms(f"sa{number}{i}", fontSize=8, textColor=BLACK,
                      fontName="Helvetica-Bold")),
            Paragraph(detail, BODY_SML),
        ])
    st = Table(step_data, colWidths=[1*cm, 4.5*cm, 12*cm])
    st.setStyle(TableStyle([
        ("BACKGROUND",     (0,0),(-1,0),  SAP_DARK),
        ("ROWBACKGROUNDS", (0,1),(-1,-1), [WHITE, GREY_BG]),
        ("GRID",           (0,0),(-1,-1), 0.4, GREY_BORDER),
        ("TOPPADDING",     (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",  (0,0),(-1,-1), 5),
        ("LEFTPADDING",    (0,0),(-1,-1), 6),
        ("VALIGN",         (0,0),(-1,-1), "TOP"),
    ]))
    els.append(st)

    # Verify table
    els.append(sp(4))
    verify_data = [[Paragraph("Verify Where", TH), Paragraph("What to Check", TH)]]
    for where, what in verify_rows:
        verify_data.append([Paragraph(where, ms(f"vw{number}", fontSize=8, textColor=TEAL,
                            fontName="Helvetica-Bold")),
                            Paragraph(what, BODY_SML)])
    vt = Table(verify_data, colWidths=[4.5*cm, 13*cm])
    vt.setStyle(TableStyle([
        ("BACKGROUND",     (0,0),(-1,0),  TEAL),
        ("ROWBACKGROUNDS", (0,1),(-1,-1), [TEAL_LIGHT, WHITE]),
        ("GRID",           (0,0),(-1,-1), 0.4, GREY_BORDER),
        ("TOPPADDING",     (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",  (0,0),(-1,-1), 5),
        ("LEFTPADDING",    (0,0),(-1,-1), 6),
        ("VALIGN",         (0,0),(-1,-1), "TOP"),
    ]))
    els.append(vt)

    # Expected result
    els.append(sp(4))
    exp_t = Table([[
        Paragraph("✓  Expected Result", ms(f"el{number}", fontSize=8, textColor=WHITE,
                  fontName="Helvetica-Bold")),
        Paragraph(expected, BODY_SML),
    ]], colWidths=[3.5*cm, 14*cm])
    exp_t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(0,0),  GREEN_OK),
        ("BACKGROUND",   (1,0),(1,0),  GREEN_LIGHT),
        ("TOPPADDING",   (0,0),(-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("LEFTPADDING",  (0,0),(-1,-1), 8),
        ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
    ]))
    els.append(exp_t)

    # Open issue
    if open_issue:
        els.append(sp(4))
        oi_t = Table([[
            Paragraph("⚠  Open Issue", ms(f"oi{number}", fontSize=8, textColor=WHITE,
                      fontName="Helvetica-Bold")),
            Paragraph(open_issue, BODY_SML),
        ]], colWidths=[3.5*cm, 14*cm])
        oi_t.setStyle(TableStyle([
            ("BACKGROUND",   (0,0),(0,0),  RED),
            ("BACKGROUND",   (1,0),(1,0),  RED_LIGHT),
            ("TOPPADDING",   (0,0),(-1,-1), 6),
            ("BOTTOMPADDING",(0,0),(-1,-1), 6),
            ("LEFTPADDING",  (0,0),(-1,-1), 8),
            ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
        ]))
        els.append(oi_t)

    bot = Table([[""]], colWidths=[17.5*cm], rowHeights=[2])
    bot.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1), status_color)]))
    els.append(bot)
    els.append(sp(10))
    return KeepTogether(els)

# ══════════════════════════════════════════════════════════════════════════════
# DOCUMENT BUILD
# ══════════════════════════════════════════════════════════════════════════════
def cover():
    els = []
    cov = Table([
        [Paragraph("ATO → S4 PO Creation, Change Document &amp; Audit Log", TITLE)],
        [Paragraph("Step-by-Step Test Cases", SUBTITLE)],
        [Paragraph("SAP S/4HANA Public Cloud  |  BTP ATO SaaS  |  GxP Compliance", SUBTITLE)],
        [Paragraph("System: QJ6-001  |  Package: CGTO_S4HC_POC  |  Date: 2026-06-26", META)],
    ], colWidths=[17.5*cm])
    cov.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), SAP_DARK),
        ("TOPPADDING",    (0,0),(-1,-1), 28),
        ("BOTTOMPADDING", (0,0),(-1,-1), 28),
        ("LEFTPADDING",   (0,0),(-1,-1), 20),
    ]))
    els.append(cov)
    els.append(sp(14))

    # Test flow summary
    els.append(Paragraph("End-to-End Test Flow Overview", H2))
    flow_data = [
        [Paragraph("#", TH), Paragraph("Test Case", TH),
         Paragraph("System", TH), Paragraph("Status", TH)],
        ["TC-01", "Prerequisites — System & Data Setup",
         "S4 + BTP", "✅ Before all tests"],
        ["TC-02", "ATO SaaS triggers PO creation event",
         "BTP — ATO SaaS", "✅ Testable NOW"],
        ["TC-03", "iFlow receives and transforms event → S4 OData API call",
         "BTP Integration Suite", "✅ Testable NOW"],
        ["TC-04", "S4 creates PO — standard + ATO extension fields written",
         "S4 — QJ6-001", "✅ Testable NOW"],
        ["TC-05", "Change Document records PO creation (CDHDR + CDPOS)",
         "S4 — QJ6-001", "✅ Verified CE2608"],
        ["TC-06", "ATO field change in ME22N — Change Document updated",
         "S4 — QJ6-001", "✅ Testable NOW"],
        ["TC-07", "Audit log — where is it stored and how to read it",
         "S4 — QJ6-001", "✅ Testable NOW"],
        ["TC-08", "ATO field change log visible in ME22N/ME23N screen",
         "S4 — QJ6-001", "⚠ Open Issue — CE2608"],
        ["TC-09", "S4 publishes outbound event back to ATO SaaS",
         "S4 → Event Mesh → BTP", "✅ Testable NOW"],
        ["TC-10", "PO cancellation from ATO — S4 marks item for deletion",
         "BTP ATO → S4", "✅ Testable NOW"],
    ]
    ct = Table(flow_data, colWidths=[1.8*cm, 7.5*cm, 5.5*cm, 2.7*cm])
    ct.setStyle(TableStyle([
        ("BACKGROUND",     (0,0),(-1,0),  SAP_BLUE),
        ("ROWBACKGROUNDS", (0,1),(-1,-1), [WHITE, GREY_BG]),
        ("GRID",           (0,0),(-1,-1), 0.4, GREY_BORDER),
        ("TOPPADDING",     (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",  (0,0),(-1,-1), 5),
        ("LEFTPADDING",    (0,0),(-1,-1), 6),
        ("VALIGN",         (0,0),(-1,-1), "TOP"),
    ]))
    els.append(ct)
    els.append(sp(10))

    # System info
    els.append(Paragraph("System & Package Reference", H2))
    els.append(tbl(
        ["Item", "Value", "Notes"],
        [
            ["POC System", "QJ6-001", "S4 development system for CGTO/ATO POC"],
            ["Package", "CGTO_S4HC_POC", "All ATO PO extension objects delivered here"],
            ["CE2608 Deliverable", "OData V4 PurchaseOrder API internal extensibility enabled", "Done — no further action needed"],
            ["CE2608 Deliverable", "Change Document verified for PO fields", "Done — CDHDR/CDPOS working"],
            ["2702 Target", "eSignature + Reauthentication integration in ME21N", "Planned"],
            ["ATO CDS View in CDPOS", "ATO CDS view name recorded as TABNAME in CDPOS", "Standard OBJECTCLAS = EINKBELEG used"],
            ["Implicit Enhancement", "Added in standard programme for ATO field description display", "POC approach — acceptability to be confirmed with PO standard team"],
        ],
        widths=[3.5*cm, 8*cm, 6*cm]
    ))
    els.append(PageBreak())
    return els

# ── TC-01 Prerequisites ───────────────────────────────────────────────────────
def tc01():
    els = []
    els.append(sec_hdr("Prerequisites — System & Data Setup",
                       "Complete before running any test case", SAP_DARK))
    els.append(sp(10))
    els.append(Paragraph(
        "All test cases depend on these prerequisites being in place. "
        "Verify each item before starting TC-02.", BODY))
    els.append(sp(6))
    els.append(tbl(
        ["#", "Prerequisite", "How to Verify", "Owner"],
        [
            ["P1", "Access to QJ6-001 S4 system granted",
             "Login to QJ6-001 — confirm ME21N is accessible",
             "Basis / Admin"],
            ["P2", "Mandatory GxP training completed",
             "Training record logged — required before accessing QJ6-001",
             "Developer / Tester"],
            ["P3", "ATO SaaS (BTP) access available",
             "Login to ATO cloud portal — confirm specimen shipment screen is accessible",
             "ATO team"],
            ["P4", "iFlow deployed in Integration Suite",
             "BTP Integration Suite → Monitor → check PO create/update iFlow is active",
             "Integration team"],
            ["P5", "Event Mesh subscription active",
             "BTP Event Mesh → check ATO outbound PO event topic subscription is live",
             "Integration team"],
            ["P6", "Test vendor exists in QJ6-001",
             "ME22N → open any PO — confirm vendor master data present",
             "MM Config"],
            ["P7", "Test material exists in QJ6-001",
             "MM03 → confirm material for therapy type exists",
             "MM Config"],
            ["P8", "SE16N access available for audit log verification",
             "SE16N → open CDHDR — confirm access",
             "Basis"],
            ["P9", "ATO extension tables exist in QJ6-001",
             "SE11 → /ATO/S4_PO_HEADER_EXT — confirm table is Active",
             "ATO Dev team"],
            ["P10", "Change Document object EINKBELEG includes ATO table",
             "SE11 → Change Document Object → EINKBELEG → check ATO table is registered",
             "ATO Dev team"],
        ],
        widths=[0.8*cm, 5*cm, 7*cm, 4.7*cm]
    ))
    els.append(PageBreak())
    return els

# ── TC-02 ATO triggers event ──────────────────────────────────────────────────
def tc02():
    return [step_card(
        "02", "ATO SaaS — Trigger PO Creation Event",
        "BTP — ATO SaaS Portal",
        [
            ("Open ATO Portal",
             "Log in to ATO Cloud application (SaaS). Navigate to 'Manage Schedules' or "
             "'Specimen Shipment' screen."),
            ("Prepare test data",
             "Create or locate a CR ID (Collection Request) that requires a purchase order. "
             "Ensure Clinical Study ID, Protocol ID and Therapy Type are set:\n"
             "  • Therapy Type: CELL_GENE\n"
             "  • Clinical Study: CS-TEST-001\n"
             "  • Protocol: PROT-TEST-01\n"
             "  • Patient Ref: PAT-TEST-001 (autologous)"),
            ("Set planning dates",
             "In 'Manager Schedules' set Pickup Date and Due Date."),
            ("Trigger ERP document creation",
             "Click the 'Trigger ERP Document Creation' button. "
             "Select the specimen shipment. Confirm the trigger."),
            ("Check outbound event",
             "Navigate to BTP Event Mesh → Messages Inbox → find the outbound event. "
             "Event type: PurchaseOrder.Create\n"
             "Confirm payload contains:\n"
             "  • Vendor, Material, Quantity, Delivery Date (standard fields)\n"
             "  • TherapyType, ClinicalStudy, ProtocolRef, PatientRef (ATO fields)"),
        ],
        [
            ("ATO Portal", "Outbound event visible in Event Mesh with correct payload including ATO fields"),
            ("BTP Event Mesh", "Event published to topic — status = Published. Payload contains all ATO fields."),
            ("BTP Monitor", "No error in event publishing — event consumed by iFlow subscriber"),
        ],
        "ATO SaaS publishes a PO creation event to Event Mesh with standard + ATO extension fields in the payload.",
        status_label="Testable NOW",
        status_color=BTP_GREEN
    )]

# ── TC-03 iFlow ───────────────────────────────────────────────────────────────
def tc03():
    return [step_card(
        "03", "iFlow — Transform ATO Event → S4 OData API Call",
        "BTP Integration Suite",
        [
            ("Monitor iFlow execution",
             "BTP Integration Suite → Monitor → All Integration Flows → filter by PO Create flow."),
            ("Check message processing",
             "Find the message triggered by the TC-02 event. Status should be COMPLETED."),
            ("Verify schema mapping",
             "Open the message log — confirm iFlow mapped:\n"
             "  • ATO event schema → S4 PurchaseOrder OData V4 API schema\n"
             "  • TherapyType, ClinicalStudy, ProtocolRef, PatientRef fields mapped correctly"),
            ("Confirm S4 API call",
             "In iFlow log → outbound call → confirm POST to:\n"
             "  /sap/opu/odata4/sap/api_purchaseorder_2/srvd_a2x/sap/purchaseorder/0001/PurchaseOrder\n"
             "HTTP status = 201 Created"),
        ],
        [
            ("Integration Suite Monitor", "Message status = COMPLETED — no errors in processing log"),
            ("iFlow Payload Log", "ATO fields correctly mapped to OData request body"),
            ("Outbound HTTP Log", "S4 OData API responded with HTTP 201 and returned PO number"),
        ],
        "iFlow successfully transforms ATO event schema to S4 OData V4 format and calls the PurchaseOrder API. "
        "Response confirms PO number created.",
        status_label="Testable NOW",
        status_color=BTP_GREEN
    )]

# ── TC-04 S4 PO Creation ──────────────────────────────────────────────────────
def tc04():
    return [step_card(
        "04", "S4 — PO Created with Standard + ATO Extension Fields",
        "S4 — QJ6-001",
        [
            ("Navigate to PO",
             "ME23N → enter PO number returned from TC-03 iFlow log. "
             "Or ME21N search by vendor and date to find the newly created PO."),
            ("Verify standard PO fields",
             "Header: Vendor, Document Date, Purchase Org, Company Code\n"
             "Item: Material, Quantity, Delivery Date, Plant"),
            ("Verify ATO extension tab",
             "Look for 'Advanced Therapy Information' tab on PO Header.\n"
             "Confirm values:\n"
             "  • Therapy Type = CELL_GENE\n"
             "  • Clinical Study = CS-TEST-001\n"
             "  • Protocol Ref = PROT-TEST-01"),
            ("Verify ATO item fields",
             "PO Item → Advanced Therapy Information tab\n"
             "Confirm: Patient Ref = PAT-TEST-001"),
            ("Verify extension tables directly",
             "SE16N → /ATO/S4_PO_HEADER_EXT → filter EBELN = <PO number>\n"
             "Confirm row exists with correct ATO field values.\n"
             "SE16N → /ATO/S4_PO_ITEM_EXT → filter EBELN + EBELP = <PO number + item>\n"
             "Confirm row exists."),
        ],
        [
            ("ME23N", "PO exists with correct standard fields. Advanced Therapy Information tab visible with ATO values."),
            ("SE16N → /ATO/S4_PO_HEADER_EXT", "Row exists: EBELN=<PO#>, THERAPY_TYPE=CELL_GENE, CLINICAL_STUDY=CS-TEST-001, PROTOCOL_REF=PROT-TEST-01"),
            ("SE16N → /ATO/S4_PO_ITEM_EXT", "Row exists: EBELN+EBELP=<PO# + item>, PATIENT_REF=PAT-TEST-001"),
        ],
        "PO created in S4 with all standard fields AND ATO extension fields persisted in "
        "/ATO/S4_PO_HEADER_EXT and /ATO/S4_PO_ITEM_EXT tables.",
        status_label="Testable NOW",
        status_color=BTP_GREEN
    )]

# ── TC-05 Change Document on Create ──────────────────────────────────────────
def tc05():
    return [step_card(
        "05", "Change Document Created on PO Creation (CDHDR + CDPOS)",
        "S4 — QJ6-001 — Verified CE2608",
        [
            ("Check via ME23N",
             "ME23N → open the PO from TC-04 → Menu: Environment → Changes\n"
             "A change log screen opens showing the creation record."),
            ("Check CDHDR directly",
             "SE16N → CDHDR → filter:\n"
             "  OBJECTCLAS = EINKBELEG\n"
             "  OBJECTID = <PO number>\n"
             "Note the CHANGENR value for use in subsequent steps."),
            ("Check CDPOS for standard fields",
             "SE16N → CDPOS → filter CHANGENR = <value from above>\n"
             "Expect rows for standard PO fields created:\n"
             "  TABNAME = EKKO, FNAME = various standard fields"),
            ("Check CDPOS for ATO fields",
             "In same CDPOS filter result, look for rows where:\n"
             "  TABNAME = /ATO/S4_PO_HEADER_EXT or ATO CDS view name\n"
             "  FNAME = THERAPY_TYPE / CLINICAL_STUDY / PROTOCOL_REF\n"
             "  VALUE_NEW = values set in TC-02"),
        ],
        [
            ("SE16N → CDHDR", "One row: OBJECTCLAS=EINKBELEG, OBJECTID=<PO#>, USERNAME=<service user>, UDATE=today"),
            ("SE16N → CDPOS standard", "Rows with TABNAME=EKKO/EKPO, standard field names, VALUE_NEW populated"),
            ("SE16N → CDPOS ATO", "Rows with TABNAME=ATO table/CDS, FNAME=THERAPY_TYPE etc., VALUE_NEW=CELL_GENE etc."),
            ("ME23N → Environment → Changes", "Change log screen shows PO creation entry with date and user"),
        ],
        "CDHDR has one header row. CDPOS has rows for both standard PO fields AND ATO extension fields. "
        "This confirms Change Document is working for ATO fields — verified CE2608.",
        status_label="✅ Verified CE2608",
        status_color=GREEN_OK,
        open_issue="ATO field changes appear in CDPOS but the DESCRIPTION column is blank in ME22N/ME23N change log screen "
                   "because ATO table name is not in standard PO change document object's description mapping. "
                   "ATO team added implicit enhancement as workaround — acceptability to be confirmed with PO standard team."
    )]

# ── TC-06 Change ATO field in ME22N ──────────────────────────────────────────
def tc06():
    return [step_card(
        "06", "User Changes ATO Field in ME22N — Change Document Updated",
        "S4 — QJ6-001",
        [
            ("Open PO in change mode",
             "ME22N → enter PO number from TC-04 → click Edit (pencil icon)"),
            ("Change an ATO field",
             "Navigate to 'Advanced Therapy Information' tab on PO Header.\n"
             "Change Therapy Type from CELL_GENE to PLASMA.\n"
             "Note: this is a REGULATED field — in 2702 this will trigger reauthentication."),
            ("Save the PO",
             "Click Save. PO saved successfully (no reauthentication dialog in current state — 2702 pending)."),
            ("Note the change timestamp",
             "Record the exact time of save for cross-reference with CDHDR."),
        ],
        [
            ("SE16N → CDHDR", "New row added: OBJECTCLAS=EINKBELEG, USERNAME=<your user>, UDATE=today, UTIME=save time. Note new CHANGENR."),
            ("SE16N → CDPOS", "Filter new CHANGENR: row with TABNAME=ATO table, FNAME=THERAPY_TYPE, VALUE_OLD=CELL_GENE, VALUE_NEW=PLASMA"),
            ("SE16N → /ATO/S4_PO_HEADER_EXT", "THERAPY_TYPE field now = PLASMA (current live value updated)"),
            ("ME23N → Environment → Changes", "New change entry appears in change log for this PO"),
        ],
        "CDHDR has a new row for this change. CDPOS has a row with VALUE_OLD=CELL_GENE and VALUE_NEW=PLASMA. "
        "This is the GxP audit trail — who changed what, from what value, to what value, when.",
        status_label="Testable NOW",
        status_color=ORANGE
    )]

# ── TC-07 Audit Log ───────────────────────────────────────────────────────────
def tc07():
    els = []
    els.append(sec_hdr("TC-07 — Where the Audit Log Is Stored and How to Read It",
                       "Complete audit trail reference for GxP compliance", PURPLE))
    els.append(sp(10))

    els.append(Paragraph("7.1  Audit Log Storage Locations", H2))
    els.append(tbl(
        ["Store", "Table / Location", "What It Contains", "System"],
        [
            ["S4 Change Doc Header", "CDHDR",
             "PO number (OBJECTID), Change Doc number (CHANGENR), User (USERNAME), Date (UDATE), Time (UTIME), Object class (EINKBELEG)",
             "QJ6-001"],
            ["S4 Change Doc Item", "CDPOS",
             "CHANGENR (links to CDHDR), Table name (TABNAME), Field name (FNAME), Old value (VALUE_OLD), New value (VALUE_NEW)",
             "QJ6-001"],
            ["S4 ATO Current Values", "/ATO/S4_PO_HEADER_EXT\n/ATO/S4_PO_ITEM_EXT",
             "Latest current values of ATO fields only — NOT history. Query for current state.",
             "QJ6-001"],
            ["BTP eSignature (2702)", "BTP eSignature SaaS",
             "Signature ID, User, Timestamp, Reason Code, Credential hash. Linked to CHANGENR in CDHDR.",
             "BTP — planned 2702"],
        ],
        widths=[3.5*cm, 4.5*cm, 6.5*cm, 3*cm]
    ))
    els.append(sp(8))

    els.append(Paragraph("7.2  How to Read the Complete Audit Trail", H2))
    els.append(code_block([
        "STEP 1 — Find all changes to a specific PO:",
        "  SE16N → CDHDR",
        "  Filter: OBJECTCLAS = EINKBELEG",
        "         OBJECTID   = <PO number e.g. 4500000123>",
        "  Result: list of CHANGENR rows — one row per save event",
        "          each row shows: USERNAME, UDATE, UTIME",
        "",
        "STEP 2 — For each CHANGENR, see what fields changed:",
        "  SE16N → CDPOS",
        "  Filter: CHANGENR = <value from CDHDR>",
        "  Result: one row per changed field",
        "          TABNAME  = table where field lives (EKKO, /ATO/S4_PO_HEADER_EXT etc.)",
        "          FNAME    = field name (THERAPY_TYPE, LIFNR etc.)",
        "          VALUE_OLD = value before change",
        "          VALUE_NEW = value after change",
        "",
        "STEP 3 — See current live values of ATO fields:",
        "  SE16N → /ATO/S4_PO_HEADER_EXT",
        "  Filter: EBELN = <PO number>",
        "  Result: current values of THERAPY_TYPE, CLINICAL_STUDY, PROTOCOL_REF",
        "",
        "STEP 4 — Display via ME23N (standard UI):",
        "  ME23N → open PO → Environment menu → Changes",
        "  Shows: standard PO field changes in formatted view",
        "  NOTE: ATO extension field changes may NOT show description text (open issue)",
        "",
        "STEP 5 — After 2702: correlate with eSignature record:",
        "  Take CHANGENR from CDHDR",
        "  Find matching Signature ID in BTP eSignature SaaS admin console",
        "  Confirms: same user, same timestamp, reason code provided",
        "  Combined CDHDR + CDPOS + BTP Signature = complete 21 CFR Part 11 audit trail",
    ]))
    els.append(sp(8))

    els.append(Paragraph("7.3  CDPOS Key Fields — Quick Reference", H2))
    els.append(tbl(
        ["Field", "Meaning", "Example Value"],
        [
            ["CHANGENR",   "Change Document Number — links CDHDR to CDPOS",   "0000012345"],
            ["TABNAME",    "Table where the changed field lives",               "EKKO or /ATO/S4_PO_HEADER_EXT"],
            ["FNAME",      "Field name that changed",                          "THERAPY_TYPE"],
            ["VALUE_OLD",  "Value BEFORE the change — the audit trail past",   "CELL_GENE"],
            ["VALUE_NEW",  "Value AFTER the change — what it is now",          "PLASMA"],
            ["CHNGIND",    "Change indicator: U=Update, I=Insert, D=Delete",   "U"],
            ["TABKEY",     "Key of the changed record (PO number + item etc.)", "4500000123001"],
        ],
        widths=[3.5*cm, 7.5*cm, 6.5*cm]
    ))
    els.append(PageBreak())
    return els

# ── TC-08 ATO change log display issue ───────────────────────────────────────
def tc08():
    return [step_card(
        "08", "ATO Field Change Log Visible in ME22N/ME23N Screen",
        "S4 — QJ6-001 — OPEN ISSUE",
        [
            ("Open PO change log",
             "ME22N or ME23N → open PO from TC-04 → Environment → Changes"),
            ("Look for ATO field changes",
             "In the change log screen, look for rows where Therapy Type, Clinical Study, "
             "Protocol Ref appear as changed fields."),
            ("Check description column",
             "ATO change rows may show with blank description in the 'Field' column "
             "because the ATO table name is not in the standard description mapping."),
            ("Check if implicit enhancement active",
             "If ATO team's implicit enhancement is deployed, the description should "
             "show the ATO field name. Verify this is working."),
        ],
        [
            ("ME23N → Environment → Changes",
             "Standard PO field changes visible with field labels. "
             "ATO field changes: check if THERAPY_TYPE, CLINICAL_STUDY, PROTOCOL_REF appear."),
            ("CDPOS cross-check",
             "SE16N → CDPOS → CHANGENR → confirm ATO rows exist even if not displayed in ME23N"),
        ],
        "CURRENT STATE: ATO field changes recorded in CDPOS but description blank in ME23N. "
        "Data IS captured — display is the gap. "
        "TARGET STATE: ATO fields appear with proper labels in ME22N/ME23N change log.",
        status_label="⚠ Open Issue",
        status_color=RED,
        open_issue="Resolution being investigated: BAdI 'Change Document Processing' (identified by Jiss, PO team) "
                   "OR confirm if ATO implicit enhancement is sufficient. "
                   "Action: joint call — ATO team (Allen Yuan) + PO team (Jiss) + Change Document team."
    )]

# ── TC-09 S4 outbound event to ATO ───────────────────────────────────────────
def tc09():
    return [step_card(
        "09", "S4 Publishes Outbound Event Back to ATO SaaS",
        "S4 → Event Mesh → BTP ATO SaaS",
        [
            ("Make a change in ME22N",
             "Change a standard or ATO field on the PO (e.g. delivery date or therapy type). Save."),
            ("Check S4 outbound event",
             "S4 Event Mesh configuration → confirm PO change event was published.\n"
             "Event type: sap.s4.beh.purchaseorder.v1.PurchaseOrder.Changed.v1"),
            ("Check Event Mesh",
             "BTP Event Mesh → check the topic for PO change events — new message visible."),
            ("Check iFlow processing",
             "Integration Suite → Monitor → PO Update iFlow → confirm COMPLETED status."),
            ("Verify ATO receives update",
             "ATO Cloud portal → open the specimen shipment linked to this PO → "
             "confirm the changed field value is reflected on the ATO side."),
        ],
        [
            ("S4 Event Framework", "Outbound event published after PO save"),
            ("BTP Event Mesh", "Message visible in PO change topic"),
            ("Integration Suite", "iFlow processed message with status COMPLETED"),
            ("ATO SaaS Portal", "Changed field visible on ATO specimen shipment — linkage confirmed"),
        ],
        "PO change event flows from S4 → Event Mesh → iFlow → ATO SaaS. "
        "ATO side reflects the change — bidirectional sync confirmed.",
        status_label="Testable NOW",
        status_color=BTP_GREEN
    )]

# ── TC-10 Cancellation ────────────────────────────────────────────────────────
def tc10():
    return [step_card(
        "10", "PO Cancellation from ATO — S4 Marks Item for Deletion",
        "BTP ATO → S4",
        [
            ("Trigger cancellation in ATO",
             "ATO Cloud portal → open specimen shipment → change status to CANCELLED."),
            ("ATO sends cancellation event",
             "ATO publishes outbound event to Event Mesh.\n"
             "Event payload: PO number + cancellation instruction."),
            ("iFlow processes cancellation",
             "Integration Suite iFlow transforms event → calls S4 PurchaseOrder API PATCH/DELETE."),
            ("Verify in ME23N",
             "ME23N → open PO → item should show 'Mark for Deletion' indicator (L column = X)."),
            ("Verify change document",
             "SE16N → CDPOS → find new CHANGENR for this PO → "
             "row with FNAME = LOEKZ (deletion indicator), VALUE_OLD = space, VALUE_NEW = X"),
        ],
        [
            ("ME23N", "PO item shows deletion indicator (marked for deletion — NOT hard deleted)"),
            ("ATO Portal", "Specimen shipment status = CANCELLED — PO link shows deletion status"),
            ("SE16N → CDPOS", "New CDPOS row: FNAME=LOEKZ, VALUE_OLD=space, VALUE_NEW=X — audit trail preserved"),
        ],
        "PO item marked for deletion in S4 when cancelled from ATO. "
        "Cancellation recorded in Change Document. ATO portal reflects updated status. "
        "NOTE: S4 does NOT hard-delete PO lines — only marks for deletion (GxP: data must be retained).",
        status_label="Testable NOW",
        status_color=ORANGE
    )]

# ── Audit Log Summary ─────────────────────────────────────────────────────────
def audit_summary():
    els = []
    els.append(sec_hdr("Audit Log — Complete Storage Reference",
                       "Where every piece of the GxP audit trail lives", TEAL))
    els.append(sp(10))

    els.append(code_block([
        "COMPLETE AUDIT TRAIL PICTURE",
        "═══════════════════════════════════════════════════════════════════════",
        "",
        "1. ATO SaaS (BTP)",
        "   ├── Who triggered: user logged into ATO portal",
        "   ├── What: specimen shipment schedule confirmed → PO creation triggered",
        "   ├── When: ATO event timestamp",
        "   └── Stored in: ATO Cloud application database (BTP)",
        "",
        "2. Event Mesh (BTP)",
        "   ├── Event published: PurchaseOrder.Create / PurchaseOrder.Changed",
        "   ├── Payload: all field values including ATO extension fields",
        "   └── Stored in: BTP Event Mesh message log",
        "",
        "3. Integration Suite iFlow (BTP)",
        "   ├── Message processing log: input payload, output payload, HTTP status",
        "   ├── Schema mapping trace: ATO schema → S4 OData schema",
        "   └── Stored in: BTP Integration Suite monitoring",
        "",
        "4. S4 PO Tables (QJ6-001)",
        "   ├── EKKO:                    Standard PO header — current values",
        "   ├── EKPO:                    Standard PO items — current values",
        "   ├── /ATO/S4_PO_HEADER_EXT:  ATO header fields — CURRENT values only",
        "   └── /ATO/S4_PO_ITEM_EXT:    ATO item fields — CURRENT values only",
        "",
        "5. Change Document (QJ6-001) ← THE PRIMARY GxP AUDIT TRAIL",
        "   ├── CDHDR:  WHO changed, WHEN changed, WHICH PO",
        "   │           OBJECTCLAS=EINKBELEG, OBJECTID=PO#, USERNAME, UDATE, UTIME",
        "   └── CDPOS:  WHAT changed — one row per field",
        "               TABNAME=EKKO or /ATO/S4_PO_HEADER_EXT",
        "               FNAME=field name (THERAPY_TYPE etc.)",
        "               VALUE_OLD=before, VALUE_NEW=after",
        "               ← Historical record — never overwritten",
        "",
        "6. BTP eSignature SaaS (Planned 2702)",
        "   ├── Signature ID linked to CHANGENR in CDHDR",
        "   ├── User identity re-verified at moment of change",
        "   ├── Reason Code captured",
        "   └── Combined with CDHDR+CDPOS = 21 CFR Part 11 compliant",
        "",
        "KEY DISTINCTION:",
        "  Tables (EKKO, /ATO/S4_PO_HEADER_EXT):  CURRENT state only",
        "  CDHDR + CDPOS:                          HISTORY of all changes — never deleted",
        "  BTP eSignature:                         PROOF of intentional authorisation",
    ]))

    els.append(sp(10))
    els.append(warn_box(
        "⚠  OPEN ISSUE: ATO field changes (THERAPY_TYPE, CLINICAL_STUDY, PROTOCOL_REF) ARE "
        "correctly recorded in CDPOS with correct TABNAME, FNAME, VALUE_OLD and VALUE_NEW. "
        "However the ME22N/ME23N change log DISPLAY screen does not show ATO field labels — "
        "the description appears blank. The data is captured but the display is the gap. "
        "This must be resolved before GxP compliance can be claimed for ATO field changes."
    ))
    return els

# ── Build ─────────────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title="ATO PO Change Document Test Cases",
        author="SAP GxP Team",
    )
    story = []
    story.extend(cover())
    story.extend(tc01())
    story.extend(tc02())
    story.extend(tc03())
    story.extend(tc04())
    story.extend(tc05())
    story.extend(tc06())
    story.extend(tc07())
    story.extend(tc08())
    story.extend(tc09())
    story.extend(tc10())
    story.extend(audit_summary())

    def on_page(c, doc):
        c.saveState()
        c.setFont("Helvetica", 7)
        c.setFillColor(colors.HexColor("#888888"))
        c.drawString(2*cm, 1.2*cm, "ATO → S4 PO Creation, Change Document & Audit Log — Step-by-Step Test Cases")
        c.drawRightString(19.5*cm, 1.2*cm, f"Page {doc.page}")
        c.setStrokeColor(colors.HexColor("#CCCCCC"))
        c.setLineWidth(0.4)
        c.line(2*cm, 1.5*cm, 19.5*cm, 1.5*cm)
        c.restoreState()

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF created: {OUTPUT}")

build()
