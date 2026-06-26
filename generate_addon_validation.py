from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUTPUT = r"C:\Users\I308878\GxP-CGTO-eSignature_Requirement\GxP_ATO_Addon_Validation_Guide.pdf"

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
CODE_S    = ms("CS", fontSize=7.5,textColor=CODE_FG,  fontName="Courier", leading=11, spaceAfter=1)
TH        = ms("TH", fontSize=8,  textColor=WHITE,    fontName="Helvetica-Bold", alignment=TA_CENTER)
TC        = ms("TC", fontSize=8,  textColor=BLACK,    leading=11)
METHOD_N  = ms("MN", fontSize=20, textColor=WHITE,    fontName="Helvetica-Bold", alignment=TA_CENTER)
METHOD_T  = ms("MT", fontSize=11, textColor=WHITE,    fontName="Helvetica-Bold")
METHOD_S  = ms("MS", fontSize=8,  textColor=colors.HexColor("#AACCFF"), fontName="Helvetica-Oblique")

def sp(n=6): return Spacer(1, n)

# ── Helpers ───────────────────────────────────────────────────────────────────
def sec_hdr(title, subtitle="", color=SAP_DARK):
    rows = [[Paragraph(title, H1)]]
    if subtitle:
        rows.append([Paragraph(subtitle, METHOD_S)])
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

def warn_box(text): return info_box(text, bg=RED_LIGHT,   border=RED)
def ok_box(text):   return info_box(text, bg=GREEN_LIGHT, border=GREEN_OK)
def note_box(text): return info_box(text, bg=GOLD_LIGHT,  border=GOLD)

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

def method_card(number, title, transaction, priority,
                steps, verify_rows, pass_text, fail_text,
                hdr_color=SAP_BLUE, note=None):
    els = []

    # Header row
    num_t = Table([[Paragraph(str(number), METHOD_N)]],
                  colWidths=[1.4*cm], rowHeights=[1.3*cm])
    num_t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), hdr_color),
        ("VALIGN",    (0,0),(-1,-1),"MIDDLE"),
    ]))
    pri_color = GREEN_OK if priority == "Primary" else (GOLD if priority == "Secondary" else TEAL)
    pri_t = Table([[Paragraph(priority, ms(f"pr{number}", fontSize=7.5, textColor=WHITE,
                   fontName="Helvetica-Bold", alignment=TA_CENTER))]],
                  colWidths=[2.5*cm], rowHeights=[1.3*cm])
    pri_t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), pri_color),
        ("VALIGN",    (0,0),(-1,-1),"MIDDLE"),
    ]))
    title_t = Table([
        [Paragraph(title, METHOD_T)],
        [Paragraph(f"Transaction: {transaction}", METHOD_S)],
    ], colWidths=[13.6*cm])
    title_t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), hdr_color),
        ("TOPPADDING",   (0,0),(-1,-1), 8),
        ("BOTTOMPADDING",(0,0),(-1,-1), 8),
        ("LEFTPADDING",  (0,0),(-1,-1), 12),
    ]))
    hdr = Table([[num_t, title_t, pri_t]], colWidths=[1.4*cm, 13.6*cm, 2.5*cm])
    hdr.setStyle(TableStyle([
        ("TOPPADDING",   (0,0),(-1,-1), 0),
        ("BOTTOMPADDING",(0,0),(-1,-1), 0),
        ("LEFTPADDING",  (0,0),(-1,-1), 0),
        ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
    ]))
    els.append(hdr)

    # Steps
    step_data = [[Paragraph("Step", TH), Paragraph("Action", TH), Paragraph("What to Enter / Look For", TH)]]
    for i, (action, detail) in enumerate(steps):
        step_data.append([
            Paragraph(str(i+1), ms(f"sn{number}{i}", fontSize=9, textColor=hdr_color,
                      fontName="Helvetica-Bold", alignment=TA_CENTER)),
            Paragraph(action, ms(f"sa{number}{i}", fontSize=8, textColor=BLACK,
                      fontName="Helvetica-Bold")),
            Paragraph(detail, BODY_SML),
        ])
    st = Table(step_data, colWidths=[0.9*cm, 4.2*cm, 12.4*cm])
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

    # Verify result rows
    els.append(sp(3))
    vd = [[Paragraph("Result", TH), Paragraph("Meaning", TH), Paragraph("Action", TH)]]
    for result, meaning, action in verify_rows:
        vd.append([Paragraph(result, TC), Paragraph(meaning, TC), Paragraph(action, TC)])
    vt = Table(vd, colWidths=[5*cm, 7*cm, 5.5*cm])
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

    # Pass / Fail
    els.append(sp(3))
    pf = Table([[
        Paragraph("✓  PASS", ms(f"pl{number}", fontSize=8, textColor=WHITE,
                  fontName="Helvetica-Bold")),
        Paragraph(pass_text, BODY_SML),
        Paragraph("✗  FAIL", ms(f"fl{number}", fontSize=8, textColor=WHITE,
                  fontName="Helvetica-Bold", alignment=TA_CENTER)),
        Paragraph(fail_text, BODY_SML),
    ]], colWidths=[1.8*cm, 6.95*cm, 1.8*cm, 6.95*cm])
    pf.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(0,0),  GREEN_OK),
        ("BACKGROUND",   (1,0),(1,0),  GREEN_LIGHT),
        ("BACKGROUND",   (2,0),(2,0),  RED),
        ("BACKGROUND",   (3,0),(3,0),  RED_LIGHT),
        ("TOPPADDING",   (0,0),(-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("LEFTPADDING",  (0,0),(-1,-1), 8),
        ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
    ]))
    els.append(pf)

    if note:
        els.append(sp(3))
        els.append(note_box(note))

    bot = Table([[""]], colWidths=[17.5*cm], rowHeights=[2])
    bot.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1), hdr_color)]))
    els.append(bot)
    els.append(sp(10))
    return KeepTogether(els)

# ══════════════════════════════════════════════════════════════════════════════
# PAGES
# ══════════════════════════════════════════════════════════════════════════════
def cover():
    els = []
    cov = Table([
        [Paragraph("ATO Life Science Add-on Validation Guide", TITLE)],
        [Paragraph("How to Verify the Add-on Is Installed in S4 System", SUBTITLE)],
        [Paragraph("SAP S/4HANA Public Cloud  |  System: QJ6-001  |  Package: CGTO_S4HC_POC", SUBTITLE)],
        [Paragraph("Release CE2608 Deliverables  |  Date: 2026-06-26", META)],
    ], colWidths=[17.5*cm])
    cov.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), SAP_DARK),
        ("TOPPADDING",    (0,0),(-1,-1), 28),
        ("BOTTOMPADDING", (0,0),(-1,-1), 28),
        ("LEFTPADDING",   (0,0),(-1,-1), 20),
    ]))
    els.append(cov)
    els.append(sp(14))

    # Quick reference
    els.append(Paragraph("8 Validation Methods — Quick Reference", H2))
    els.append(tbl(
        ["#", "Method", "Transaction", "Priority", "What It Validates"],
        [
            ["1", "SAINT — Add-on Installation Tool",        "SAINT",            "Primary",   "Life Science Add-on fully installed"],
            ["2", "Check ATO Extension Tables",              "SE11",             "Primary",   "/ATO/S4_PO_HEADER_EXT and /ATO/S4_PO_ITEM_EXT exist and Active"],
            ["3", "Check Package Objects",                   "SE80 / SE21",      "Secondary", "Package CGTO_S4HC_POC has expected objects"],
            ["4", "Check Namespace Registration",            "SE03",             "Secondary", "/ATO/ namespace registered and active"],
            ["5", "Check Change Document Object (CE2608)",   "SCDO",             "Primary",   "EINKBELEG object includes ATO table — CE2608 specific"],
            ["6", "Check OData API Extension (CE2608)",      "/IWBEP/V4_ADMIN",  "Primary",   "PurchaseOrder V4 API extensibility enabled — CE2608 specific"],
            ["7", "SE16N Runtime Data Check",                "SE16N",            "Secondary", "ATO tables have data — end-to-end integration working"],
            ["8", "System Component List",                   "SM51",             "Secondary", "Add-on component version visible in system info"],
        ],
        widths=[0.8*cm, 5.5*cm, 3.8*cm, 2.4*cm, 5*cm]
    ))
    els.append(sp(10))

    els.append(ok_box(
        "✅  Start with Method 1 (SAINT) — it gives the definitive answer in one screen. "
        "Then verify Methods 2, 5 and 6 to confirm CE2608-specific objects are applied. "
        "Methods 3, 4, 7, 8 provide additional confirmation."
    ))
    els.append(sp(6))
    els.append(warn_box(
        "⚠  Prerequisites: GxP mandatory training must be completed before accessing QJ6-001. "
        "Training record is logged and auditable. Contact the ATO team "
        "(Loring Wu / Satish Kumar) if access is denied."
    ))
    els.append(PageBreak())
    return els

# ── Method 1: SAINT ───────────────────────────────────────────────────────────
def method1():
    return [method_card(
        1, "SAINT — SAP Add-on Installation Tool",
        "SAINT",
        "Primary",
        [
            ("Open SAINT",      "Transaction code: SAINT → press Enter"),
            ("Go to Status tab", "Click the 'Status' tab at the top of the SAINT screen"),
            ("Search for add-on",
             "In the list, look for one of these entries:\n"
             "  • LS_ADD_ON   (Life Science Add-on — combined product)\n"
             "  • ATO_S4HC    (Advanced Therapy Orchestration for S4HC)\n"
             "  • CGTO_S4HC   (old name — Cell and Gene Therapy Orchestration)"),
            ("Check Status column",
             "The Status column must show: INSTALLED\n"
             "Also note the Version and Patch Level for documentation."),
        ],
        [
            ("LS_ADD_ON / ATO_S4HC status = INSTALLED",
             "Life Science Add-on fully installed — all tables and objects delivered",
             "Proceed to Methods 2 and 5 to verify specific objects"),
            ("Entry visible but status ≠ INSTALLED",
             "Add-on started but not completed — partial installation",
             "Contact Basis team — re-run SAINT installation"),
            ("No entry found",
             "Add-on NOT installed in this system",
             "Contact Basis / SAP Cloud Operations to install"),
        ],
        "LS_ADD_ON or ATO_S4HC shows status INSTALLED with version and patch level.",
        "No entry or non-INSTALLED status — add-on not applied. Contact Basis team.",
        hdr_color=SAP_DARK,
        note="SAINT is the single most reliable check. If SAINT shows INSTALLED, the add-on "
             "transport has been applied. All /ATO/ namespace objects should then exist."
    )]

# ── Method 2: SE11 ────────────────────────────────────────────────────────────
def method2():
    return [method_card(
        2, "SE11 — Check ATO Extension Tables Exist and Are Active",
        "SE11",
        "Primary",
        [
            ("Open SE11",
             "Transaction code: SE11 → select 'Database Table' radio button"),
            ("Check Header Extension Table",
             "Enter: /ATO/S4_PO_HEADER_EXT → click Display\n"
             "Expected: table definition opens showing fields:\n"
             "  EBELN (FK to EKKO), THERAPY_TYPE, CLINICAL_STUDY, PROTOCOL_REF"),
            ("Check Item Extension Table",
             "Enter: /ATO/S4_PO_ITEM_EXT → click Display\n"
             "Expected: table definition opens showing fields:\n"
             "  EBELN+EBELP (FK to EKPO), THERAPY_TYPE, PATIENT_REF"),
            ("Verify Active status",
             "In the table definition screen, top right area shows:\n"
             "  Active (shown in green or as 'Active' text)\n"
             "If it shows 'Inactive' or 'Revised' → table not activated"),
        ],
        [
            ("/ATO/S4_PO_HEADER_EXT exists and Active",
             "ATO header extension table delivered correctly",
             "Check /ATO/S4_PO_ITEM_EXT next"),
            ("/ATO/S4_PO_ITEM_EXT exists and Active",
             "ATO item extension table delivered correctly",
             "Proceed to Method 5 (SCDO)"),
            ("Table does not exist",
             "Add-on transport NOT applied — tables not delivered",
             "Re-verify SAINT result. Apply ATO transport from package CGTO_S4HC_POC"),
            ("Table exists but Inactive",
             "Transport applied but activation failed",
             "SE11 → Activate the table manually or re-apply transport"),
        ],
        "Both /ATO/S4_PO_HEADER_EXT and /ATO/S4_PO_ITEM_EXT exist and show Active status.",
        "Table missing or Inactive — add-on objects not fully delivered.",
        hdr_color=SAP_BLUE
    )]

# ── Method 3: SE80 Package ────────────────────────────────────────────────────
def method3():
    return [method_card(
        3, "SE80 / SE21 — Check Package CGTO_S4HC_POC Objects",
        "SE80 or SE21",
        "Secondary",
        [
            ("Open SE80",
             "Transaction code: SE80 → select 'Package' from the dropdown → "
             "enter: CGTO_S4HC_POC → press Enter"),
            ("Expand the package tree",
             "Click the triangle/arrow to expand CGTO_S4HC_POC.\n"
             "Look for sub-nodes: Dictionary Objects, Function Groups, Classes etc."),
            ("Check key objects",
             "Confirm these objects exist under the package:\n"
             "  • Tables: /ATO/S4_PO_HEADER_EXT, /ATO/S4_PO_ITEM_EXT\n"
             "  • CDS Views: /ATO/ namespace CDS views\n"
             "  • Classes for PO extension logic"),
            ("Alternative: SE21",
             "SE21 → enter package CGTO_S4HC_POC → Display\n"
             "Shows all objects assigned to this package with their types."),
        ],
        [
            ("Package exists with objects listed",
             "POC delivery transport applied — all objects in place",
             "Spot-check individual objects via SE11 / SE24"),
            ("Package exists but is empty",
             "Package created but transport not applied",
             "Apply CGTO_S4HC_POC transport via STMS"),
            ("Package does not exist",
             "Entire POC delivery missing from this system",
             "Contact ATO team (Loring Wu) to get transport request number"),
        ],
        "Package CGTO_S4HC_POC exists with tables, CDS views and classes listed underneath.",
        "Package empty or missing — transport not applied.",
        hdr_color=ORANGE
    )]

# ── Method 4: SE03 Namespace ──────────────────────────────────────────────────
def method4():
    return [method_card(
        4, "SE03 — Check /ATO/ Namespace Registration",
        "SE03",
        "Secondary",
        [
            ("Open SE03",
             "Transaction code: SE03 → select 'Namespace' from the menu on the left"),
            ("Search for /ATO/ namespace",
             "Enter /ATO/ in the search field → press Enter or click Display"),
            ("Check namespace status",
             "The namespace entry should show:\n"
             "  Status: ACTIVE\n"
             "  Role: SAP (delivered by SAP)\n"
             "  Repair flag: should be set appropriately for the system type"),
        ],
        [
            ("/ATO/ namespace found — Status ACTIVE",
             "SAP registered /ATO/ namespace in this system",
             "Namespace is valid — objects can be created/transported"),
            ("/ATO/ namespace not found",
             "Namespace not registered — unusual if SAINT shows INSTALLED",
             "Contact Basis — namespace registration may have failed"),
        ],
        "/ATO/ namespace exists with Status = ACTIVE.",
        "Namespace missing — contact Basis team for namespace registration.",
        hdr_color=PURPLE
    )]

# ── Method 5: SCDO (CE2608) ───────────────────────────────────────────────────
def method5():
    return [method_card(
        5, "SCDO — Change Document Object Includes ATO Table (CE2608 Check)",
        "SCDO",
        "Primary",
        [
            ("Open SCDO",
             "Transaction code: SCDO → press Enter\n"
             "This shows all Change Document Objects registered in the system."),
            ("Find EINKBELEG",
             "In the list of objects, find: EINKBELEG\n"
             "This is the standard Purchase Order change document object.\n"
             "Double-click EINKBELEG to open its definition."),
            ("Go to Table Names tab",
             "Inside EINKBELEG definition, click the 'Table Names' tab.\n"
             "This shows all tables registered under this change document object."),
            ("Search for ATO table",
             "In the table list, look for:\n"
             "  /ATO/S4_PO_HEADER_EXT\n"
             "If found → ATO table is registered → changes to ATO fields will be "
             "recorded in CDPOS with OBJECTCLAS = EINKBELEG"),
            ("Note the function module",
             "Also check if a custom function module exists for handling ATO changes:\n"
             "SE37 → search for function modules in /ATO/ namespace related to change docs"),
        ],
        [
            ("/ATO/S4_PO_HEADER_EXT in EINKBELEG table list",
             "CE2608 change document work applied — ATO changes will be in CDPOS",
             "Proceed to SE16N to verify actual CDPOS records (Method 7)"),
            ("EINKBELEG exists but /ATO/ table NOT in list",
             "CE2608 change doc registration NOT applied",
             "ATO team must extend EINKBELEG to include /ATO/S4_PO_HEADER_EXT"),
            ("EINKBELEG not found at all",
             "Standard PO change document object missing — system issue",
             "Contact Basis — standard object EINKBELEG should always exist"),
        ],
        "/ATO/S4_PO_HEADER_EXT listed under EINKBELEG in SCDO — CE2608 change doc work applied.",
        "ATO table NOT in EINKBELEG — CE2608 change doc extension not applied. ATO team action needed.",
        hdr_color=BTP_GREEN,
        note="This check is specific to CE2608 deliverable. The ATO team (Allen Yuan) confirmed they "
             "extended EINKBELEG to include the ATO table AND adjusted the function module to handle "
             "ATO field changes. An implicit enhancement was also added for description text display. "
             "All three must be in place for complete change document integration."
    )]

# ── Method 6: V4 API (CE2608) ────────────────────────────────────────────────
def method6():
    return [method_card(
        6, "V4_ADMIN — OData V4 API Extensibility Enabled (CE2608 Check)",
        "/IWBEP/V4_ADMIN",
        "Primary",
        [
            ("Open V4 Admin",
             "Transaction: /IWBEP/V4_ADMIN → press Enter\n"
             "Or navigate via /n/IWBEP/V4_ADMIN"),
            ("Find PurchaseOrder API",
             "In the service list, search for:\n"
             "  Technical Name: API_PURCHASEORDER_2\n"
             "  or Description containing 'Purchase Order'"),
            ("Check extensibility setting",
             "Click the service → go to Properties or Settings tab.\n"
             "Look for: Internal Extensibility = Enabled\n"
             "This is the CE2608 deliverable — 'OData V4 API enabled for internal "
             "extensibility (without the PaaS API extension)'"),
            ("Alternative check via SPRO",
             "SPRO → SAP NetWeaver → Gateway → OData V4 → Service Administration\n"
             "Find PurchaseOrder service → verify extensibility flag"),
        ],
        [
            ("Internal Extensibility = Enabled",
             "CE2608 OData V4 API extensibility delivered — ATO can extend the API",
             "ATO OData extension should work correctly"),
            ("Internal Extensibility = Disabled or not found",
             "CE2608 API enablement not applied to this system",
             "PO standard team must apply CE2608 API extensibility transport"),
            ("Service API_PURCHASEORDER_2 not found",
             "OData V4 PurchaseOrder service not registered in this system",
             "Register via /IWFND/V4_ADMIN or contact Basis"),
        ],
        "API_PURCHASEORDER_2 found with Internal Extensibility = Enabled.",
        "Extensibility disabled or service not found — CE2608 API work not applied.",
        hdr_color=TEAL,
        note="CE2608 delivered: 'The OData V4 API is enabled for internal extensibility "
             "(without the PaaS API extension). Customer extensibility...' — GxP Handover Slide 10. "
             "This was a prerequisite blocker for ATO: they found it was NOT enabled during POC "
             "and the PO standard team (Nils/Jiss) had to plan and deliver this change."
    )]

# ── Method 7: SE16N ───────────────────────────────────────────────────────────
def method7():
    return [method_card(
        7, "SE16N — Runtime Data Check (Confirm Integration Working)",
        "SE16N",
        "Secondary",
        [
            ("Check header extension table",
             "SE16N → Table: /ATO/S4_PO_HEADER_EXT → Execute (no filter)\n"
             "This shows all ATO-enriched PO header records."),
            ("Check item extension table",
             "SE16N → Table: /ATO/S4_PO_ITEM_EXT → Execute (no filter)\n"
             "This shows all ATO-enriched PO item records."),
            ("Check CDHDR for ATO-triggered POs",
             "SE16N → CDHDR → filter OBJECTCLAS = EINKBELEG\n"
             "Look for recent entries triggered by ATO service user"),
            ("Check CDPOS for ATO field entries",
             "SE16N → CDPOS → filter TABNAME = /ATO/S4_PO_HEADER_EXT\n"
             "Rows here confirm ATO changes are being recorded in change document"),
        ],
        [
            ("Rows exist in /ATO/ tables",
             "Add-on installed AND POs already created via ATO integration",
             "End-to-end integration working — run TC-04 to TC-07 for full validation"),
            ("Tables exist but are empty",
             "Add-on installed but no ATO-triggered POs created yet",
             "Normal for fresh system — run TC-02 to TC-04 to create first ATO PO"),
            ("CDPOS has rows with TABNAME = /ATO/ table",
             "Change Document recording ATO field changes — CE2608 working",
             "CE2608 change doc integration confirmed"),
            ("Tables do not exist",
             "Add-on NOT installed — SE11 check will confirm",
             "Go back to Method 1 (SAINT) to verify installation status"),
        ],
        "Tables exist. Rows present (or empty on fresh system). CDPOS has /ATO/ table entries.",
        "Tables do not exist — add-on not installed. CDPOS has no /ATO/ rows — CE2608 change doc not working.",
        hdr_color=ORANGE
    )]

# ── Method 8: SM51 ────────────────────────────────────────────────────────────
def method8():
    return [method_card(
        8, "SM51 / System Status — Component Version Check",
        "SM51 or System → Status",
        "Secondary",
        [
            ("Via System menu",
             "Menu: System → Status → click 'Component Information' button (or F2)\n"
             "A list of installed SAP components with versions appears."),
            ("Via SM51",
             "Transaction: SM51 → select an application server → "
             "click 'Release Notes' or 'Component Info' button"),
            ("Search for ATO/LS component",
             "In the component list, look for:\n"
             "  • LS_ADD_ON — Life Science Add-on\n"
             "  • ATO_S4HC or CGTO_S4HC\n"
             "Note the Release, Patch Level and SP Level for documentation."),
            ("Document the version",
             "Record the version for:\n"
             "  • GxP qualification documentation\n"
             "  • Client audit evidence package\n"
             "  • Change management records"),
        ],
        [
            ("LS_ADD_ON / ATO component visible with version",
             "Add-on installed — version confirmed for documentation",
             "Record version for qualification docs and client audit evidence"),
            ("Component not in list",
             "Add-on not installed or component name differs",
             "Cross-check with SAINT (Method 1) — SAINT is more reliable"),
        ],
        "LS_ADD_ON or ATO_S4HC component visible with version and patch level.",
        "Component not visible — use SAINT (Method 1) as primary confirmation.",
        hdr_color=DARK_GREY
    )]

# ── Final Checklist ───────────────────────────────────────────────────────────
def final_checklist():
    els = []
    els.append(sec_hdr("Complete Validation Checklist",
                       "Run in order — tick each item before proceeding to next", GREEN_OK))
    els.append(sp(10))

    els.append(tbl(
        ["#", "Check", "Transaction", "Expected Result", "If Fails"],
        [
            ["□ 1", "LS_ADD_ON / ATO_S4HC shows INSTALLED",
             "SAINT",
             "Status = INSTALLED with version",
             "Contact Basis — apply add-on installation"],
            ["□ 2", "/ATO/S4_PO_HEADER_EXT exists and Active",
             "SE11",
             "Table definition opens, status = Active",
             "Apply CGTO_S4HC_POC transport"],
            ["□ 3", "/ATO/S4_PO_ITEM_EXT exists and Active",
             "SE11",
             "Table definition opens, status = Active",
             "Apply CGTO_S4HC_POC transport"],
            ["□ 4", "Package CGTO_S4HC_POC has objects",
             "SE80",
             "Tables, CDS, Classes listed under package",
             "Get transport from ATO team (Loring Wu)"],
            ["□ 5", "/ATO/ namespace = ACTIVE",
             "SE03",
             "Namespace found, status = Active",
             "Contact Basis for namespace registration"],
            ["□ 6", "EINKBELEG includes /ATO/S4_PO_HEADER_EXT [CE2608]",
             "SCDO",
             "ATO table in EINKBELEG table list",
             "ATO team must extend EINKBELEG object"],
            ["□ 7", "PurchaseOrder V4 API extensibility enabled [CE2608]",
             "/IWBEP/V4_ADMIN",
             "Internal Extensibility = Enabled",
             "PO standard team (Nils/Jiss) to apply CE2608 API transport"],
            ["□ 8", "SE16N — /ATO/ tables accessible (empty OK)",
             "SE16N",
             "Table opens — empty = OK for fresh system",
             "Table not found — SAINT check first"],
            ["□ 9", "CDPOS records exist with TABNAME=/ATO/ table",
             "SE16N → CDPOS",
             "Rows present after first ATO PO creation",
             "Run TC-05 test case to trigger and verify"],
        ],
        widths=[1*cm, 6*cm, 3.5*cm, 4.5*cm, 2.5*cm]
    ))
    els.append(sp(10))

    els.append(Paragraph("Summary — What Each CE2608 Deliverable Means", H2))
    els.append(tbl(
        ["CE2608 Deliverable", "Method to Verify", "Status"],
        [
            ["Change Document verified for all standard PO fields",
             "SE16N → CDHDR/CDPOS for standard PO changes",
             "✅ Verified — standard framework, always worked"],
            ["OData V4 PurchaseOrder API — internal extensibility enabled",
             "Method 6: /IWBEP/V4_ADMIN",
             "✅ Delivered CE2608 — verify with Method 6"],
            ["ATO extension tables /ATO/S4_PO_HEADER_EXT and ITEM_EXT",
             "Method 2: SE11",
             "✅ Delivered CE2608 — verify with Method 2"],
            ["Change Document object EINKBELEG extended for ATO tables",
             "Method 5: SCDO",
             "✅ ATO POC — verify with Method 5"],
            ["Implicit enhancement for ATO field description in change log",
             "ME23N → Environment → Changes → check ATO field labels",
             "⚠ POC approach — acceptability pending with PO team"],
            ["eSignature integration in ME21N",
             "N/A — not yet delivered",
             "🔲 Planned 2702"],
        ],
        widths=[7*cm, 6*cm, 4.5*cm]
    ))
    els.append(sp(8))
    els.append(note_box(
        "📋  For GxP Qualification Documentation: record the results of each check above "
        "with screenshots as evidence. Include: system ID (QJ6-001), transaction name, "
        "date of check, tester name, and result. This forms part of the IQ "
        "(Installation Qualification) evidence package for client audits."
    ))
    return els

# ── Build ─────────────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title="ATO Life Science Add-on Validation Guide",
        author="SAP GxP Team",
    )
    story = []
    story.extend(cover())
    story.extend(method1())
    story.extend(method2())
    story.extend(method3())
    story.extend(method4())
    story.extend(method5())
    story.extend(method6())
    story.extend(method7())
    story.extend(method8())
    story.extend(final_checklist())

    def on_page(c, doc):
        c.saveState()
        c.setFont("Helvetica", 7)
        c.setFillColor(colors.HexColor("#888888"))
        c.drawString(2*cm, 1.2*cm, "ATO Life Science Add-on Validation Guide — System QJ6-001 | Package CGTO_S4HC_POC")
        c.drawRightString(19.5*cm, 1.2*cm, f"Page {doc.page}")
        c.setStrokeColor(colors.HexColor("#CCCCCC"))
        c.setLineWidth(0.4)
        c.line(2*cm, 1.5*cm, 19.5*cm, 1.5*cm)
        c.restoreState()

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF created: {OUTPUT}")

build()
