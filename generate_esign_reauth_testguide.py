from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUTPUT = r"C:\Users\I308878\GxP-CGTO-eSignature_Requirement\GxP_eSignature_Reauth_Integration_TestGuide.pdf"

# ── Colours ───────────────────────────────────────────────────────────────────
SAP_BLUE      = colors.HexColor("#0070F2")
SAP_DARK      = colors.HexColor("#003366")
SAP_LIGHT     = colors.HexColor("#E8F4FD")
BTP_GREEN     = colors.HexColor("#1A6632")
BTP_LIGHT     = colors.HexColor("#E6F4EA")
S4_ORANGE     = colors.HexColor("#E87722")
S4_LIGHT      = colors.HexColor("#FFF3E8")
REAUTH_PURPLE = colors.HexColor("#6B3FA0")
REAUTH_LIGHT  = colors.HexColor("#F0EAF8")
ESIGN_TEAL    = colors.HexColor("#007B8A")
ESIGN_LIGHT   = colors.HexColor("#E0F5F7")
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

W, H = A4

# ── Styles ────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def ms(name, **kw):
    return ParagraphStyle(name=name, parent=styles["Normal"], **kw)

TITLE     = ms("T",  fontSize=20, textColor=WHITE,    fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=4)
SUBTITLE  = ms("ST", fontSize=10, textColor=colors.HexColor("#AACCFF"), fontName="Helvetica", alignment=TA_CENTER, spaceAfter=2)
META      = ms("M",  fontSize=8,  textColor=colors.HexColor("#AACCFF"), fontName="Helvetica", alignment=TA_CENTER)
H1        = ms("H1", fontSize=13, textColor=WHITE,    fontName="Helvetica-Bold", spaceAfter=4, spaceBefore=2)
H2        = ms("H2", fontSize=11, textColor=SAP_DARK, fontName="Helvetica-Bold", spaceAfter=4, spaceBefore=8)
H3        = ms("H3", fontSize=9,  textColor=SAP_BLUE, fontName="Helvetica-Bold", spaceAfter=3, spaceBefore=5)
BODY      = ms("B",  fontSize=8.5,textColor=BLACK,    leading=13, spaceAfter=3, alignment=TA_JUSTIFY)
BODY_SML  = ms("BS", fontSize=8,  textColor=BLACK,    leading=12, spaceAfter=2)
NOTE      = ms("N",  fontSize=7.5,textColor=colors.HexColor("#444444"), leading=11, spaceAfter=2, fontName="Helvetica-Oblique")
QUOTE     = ms("Q",  fontSize=8,  textColor=colors.HexColor("#333333"), leading=12, leftIndent=14, spaceAfter=3, fontName="Helvetica-Oblique")
BULL      = ms("BU", fontSize=8.5,textColor=BLACK,    leading=13, leftIndent=14, spaceAfter=2)
CODE_S    = ms("CS", fontSize=7.5,textColor=CODE_FG,  fontName="Courier", leading=11, spaceAfter=1)
TH        = ms("TH", fontSize=8,  textColor=WHITE,    fontName="Helvetica-Bold", alignment=TA_CENTER)
TC        = ms("TC", fontSize=8,  textColor=BLACK,    leading=11)

# ── Helpers ───────────────────────────────────────────────────────────────────
def sp(n=6): return Spacer(1, n)

def sec_hdr(title, color=SAP_DARK):
    t = Table([[Paragraph(title, H1)]], colWidths=[17.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), color),
        ("TOPPADDING",    (0,0),(-1,-1), 9),
        ("BOTTOMPADDING", (0,0),(-1,-1), 9),
        ("LEFTPADDING",   (0,0),(-1,-1), 14),
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

def warn_box(text):
    return info_box(text, bg=RED_LIGHT, border=RED)

def ok_box(text):
    return info_box(text, bg=GREEN_LIGHT, border=GREEN_OK)

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

def test_card(number, title, prereq, steps, verify, expected_result,
              status="Testable in 2702", status_color=GOLD):
    els = []
    # header
    hdr_data = [[
        Paragraph(f"Test {number}", ms(f"tb{number}", fontSize=10, textColor=WHITE,
                  fontName="Helvetica-Bold")),
        Paragraph(title, ms(f"tt{number}", fontSize=10, textColor=WHITE,
                  fontName="Helvetica-Bold")),
        Paragraph(status, ms(f"ts{number}", fontSize=8, textColor=WHITE,
                  fontName="Helvetica-Oblique", alignment=TA_CENTER)),
    ]]
    hdr = Table(hdr_data, colWidths=[2*cm, 11*cm, 4.5*cm])
    hdr.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(1,0),  SAP_DARK),
        ("BACKGROUND",    (2,0),(2,0),  status_color),
        ("TOPPADDING",    (0,0),(-1,-1), 7),
        ("BOTTOMPADDING", (0,0),(-1,-1), 7),
        ("LEFTPADDING",   (0,0),(-1,-1), 10),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ]))
    els.append(hdr)

    # body
    body_rows = []
    if prereq:
        body_rows.append(("Prerequisites", prereq))
    body_rows.append(("Test Steps", steps))
    body_rows.append(("Verify", verify))
    body_rows.append(("Expected Result", expected_result))

    for label, content in body_rows:
        row_t = Table([[
            Paragraph(label, ms(f"bl{number}", fontSize=7.5, textColor=SAP_DARK,
                      fontName="Helvetica-Bold")),
            Paragraph(content, BODY_SML)
        ]], colWidths=[3.5*cm, 14*cm])
        row_t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(0,0),  GREY_BG),
            ("BACKGROUND",    (1,0),(1,0),  WHITE),
            ("GRID",          (0,0),(-1,-1), 0.3, GREY_BORDER),
            ("TOPPADDING",    (0,0),(-1,-1), 5),
            ("BOTTOMPADDING", (0,0),(-1,-1), 5),
            ("LEFTPADDING",   (0,0),(-1,-1), 8),
            ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ]))
        els.append(row_t)

    # bottom border
    bot = Table([[""]], colWidths=[17.5*cm], rowHeights=[2])
    bot.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1), SAP_DARK)]))
    els.append(bot)
    els.append(sp(10))
    return KeepTogether(els)

# ── Cover ─────────────────────────────────────────────────────────────────────
def cover():
    els = []
    cov = Table([
        [Paragraph("GxP eSignature &amp; Reauthentication", TITLE)],
        [Paragraph("Integration Details &amp; Test Guide", SUBTITLE)],
        [Paragraph("SAP S/4HANA ME21N  |  BTP eSignature SaaS  |  Reauthentication Framework", SUBTITLE)],
        [Paragraph("Date: 2026-06-26  |  Version: 1.0  |  Status: Pre-2702 Planning", META)],
    ], colWidths=[17.5*cm])
    cov.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), SAP_DARK),
        ("TOPPADDING",    (0,0),(-1,-1), 30),
        ("BOTTOMPADDING", (0,0),(-1,-1), 30),
        ("LEFTPADDING",   (0,0),(-1,-1), 20),
    ]))
    els.append(cov)
    els.append(sp(14))

    # availability status table
    els.append(Paragraph("Availability Status — What Is Ready vs What Is Planned", H2))
    els.append(tbl(
        ["Component", "Status", "Details"],
        [
            ["eSignature BTP SaaS Service",       "✅ Available on BTP",       "Service exists and is ready to integrate — does NOT need to be built"],
            ["Reauthentication Framework (S4)",   "✅ Available in S4",        "Framework built, APIs exposed, S-table config available in SPRO"],
            ["Change Document for PO",            "✅ Done — verified 2608",   "CDHDR/CDPOS working for all standard PO fields including ATO extension fields"],
            ["eSignature integration in ME21N",   "🔲 NOT YET BUILT",         "Trigger point in ME21N save flow — planned for 2702"],
            ["Communication Arrangement S4↔BTP",  "🔲 NOT YET configured",    "OAuth / service key between S4 and BTP eSignature tenant — needed for 2702"],
            ["Reauthentication in ME21N save",    "🔲 NOT YET integrated",    "Relevancy Check callback class + S-table registration — planned for 2702"],
            ["BTP Reason Codes for PO",           "🔲 NOT YET configured",    "Reason codes for PURCHASE_ORDER object in BTP — part of 84P provisioning"],
        ],
        widths=[5.5*cm, 3.5*cm, 8.5*cm]
    ))
    els.append(sp(10))

    # what can be tested today
    els.append(ok_box(
        "✅  Testable TODAY: Change Document for PO (verified 2608), "
        "CHECK_ESIG_ACTIVE API (returns FALSE — expected), "
        "Reauthentication S-table configuration in SPRO (framework is available)."
    ))
    els.append(sp(4))
    els.append(warn_box(
        "⚠  Requires 2702 delivery before full testing: reauthentication dialog in ME21N, "
        "BTP eSignature SaaS connection, signature capture linked to Change Document, "
        "end-to-end GxP audit trail. Contact: Swarnava Chatterjee (eSignature) + "
        "Yadesh Gupta (Reauthentication Framework) for test system access."
    ))
    els.append(PageBreak())
    return els

# ── Section 1: Integration details ───────────────────────────────────────────
def section1():
    els = []
    els.append(sec_hdr("Section 1 — eSignature Integration Details", ESIGN_TEAL))
    els.append(sp(10))

    els.append(Paragraph("1.1  Where eSignature Is Triggered in ME21N", H2))
    els.append(Paragraph(
        "The eSignature trigger point sits inside the ME21N save flow — AFTER Change Document "
        "fires but BEFORE the Logical Unit of Work (LUW) is committed to the database. "
        "If the user cancels the reauthentication dialog, the ENTIRE save is rolled back — "
        "nothing is committed.", BODY))

    els.append(code_block([
        "ME21N SAVE FLOW — eSignature Integration Point",
        "═══════════════════════════════════════════════════════════════",
        "",
        "  Step 1   User fills PO fields and clicks Save",
        "  Step 2   EKKO / EKPO written (standard PO processing)",
        "  Step 3   /ATO/S4_PO_HEADER_EXT written (ATO extension fields)",
        "  Step 4   Change Document fires → CDHDR + CDPOS created  ← done 2608 ✓",
        "           Records: field, old value, new value, user, timestamp",
        "  ─────────────────────────────────────────────────────────────",
        "  Step 5   [NEW — 2702] CHECK_ESIG_ACTIVE",
        "           → If FALSE: skip all reauthentication, commit normally",
        "           → If TRUE:  proceed to relevancy check",
        "  ─────────────────────────────────────────────────────────────",
        "  Step 6   [NEW — 2702] Relevancy Check callback: ZCL_PO_REAUTH_CHECK",
        "           → Reads S-table VC_SRA_SOT for regulated fields",
        "           → ABAP_FALSE: no regulated field changed → skip, commit",
        "           → ABAP_TRUE:  regulated field changed → LUW PAUSED",
        "  ─────────────────────────────────────────────────────────────",
        "  Step 7   [NEW — 2702] REQUEST_REAUTH (HCP GUI variant for ME21N)",
        "           → Dialog shown: Password re-entry + Reason Code dropdown",
        "           → User CANCELS → ROLLBACK — PO NOT saved",
        "           → User CONFIRMS → BTP eSignature SaaS validates password",
        "  ─────────────────────────────────────────────────────────────",
        "  Step 8   [NEW — 2702] VALIDATE_RESULT",
        "           → Confirms signature captured in BTP",
        "           → Signature ID linked to CHANGENR in CDHDR",
        "  Step 9   COMMIT WORK — all writes committed atomically",
        "  Step 10  Outbound event published → ATO SaaS notified via Event Mesh",
    ]))

    els.append(sp(8))
    els.append(Paragraph("1.2  The 4 APIs Applications Must Call", H2))
    els.append(tbl(
        ["API", "When to Call", "Technology", "Status"],
        [
            ["CHECK_ESIG_ACTIVE",          "Before any signature flow — check if GxP is active", "Any",                "Available"],
            ["REQUEST_REAUTH (OData/GUI)", "Trigger reauthentication dialog in ME21N",           "HCP GUI / Web GUI",  "2702"],
            ["REQUEST_REAUTH (library)",   "Trigger reauthentication in all other app types",    "All technologies",   "2702"],
            ["VALIDATE_RESULT",            "Confirm signature was successfully captured",         "Any technology",     "2702"],
        ],
        widths=[4.5*cm, 6.5*cm, 3.5*cm, 3*cm]
    ))
    els.append(sp(8))

    els.append(Paragraph("1.3  Communication Arrangement Setup (One-Time)", H2))
    els.append(tbl(
        ["Step", "Activity", "Details"],
        [
            ["1", "Create Communication Arrangement in S4",  "System Alias pointing to BTP eSignature SaaS tenant"],
            ["2", "Configure OAuth / Service Key",           "Exchange credentials between S4 and BTP eSignature service"],
            ["3", "Test connectivity",                       "Verify S4 can reach BTP eSignature endpoint before enabling in production"],
            ["4", "Pattern reference",                       "Follows same pattern as SAP_COM_0267 for other BTP integrations"],
        ],
        widths=[1.2*cm, 5.5*cm, 10.8*cm]
    ))
    els.append(PageBreak())
    return els

# ── Section 2: Reauthentication integration ───────────────────────────────────
def section2():
    els = []
    els.append(sec_hdr("Section 2 — Reauthentication Framework Integration Details", REAUTH_PURPLE))
    els.append(sp(10))

    els.append(Paragraph("2.1  Relevancy Check Callback — What LOB Team Must Implement", H2))
    els.append(Paragraph(
        "The LOB application team must implement ONE callback class. "
        "The framework calls this class to decide whether reauthentication is required. "
        "Everything else — calling BTP, capturing signature, linking to Change Doc — "
        "is handled by the framework invisibly.", BODY))

    els.append(code_block([
        "\" Relevancy Check callback — LOB team implements this",
        "CLASS zcl_po_reauth_check DEFINITION PUBLIC FINAL.",
        "  PUBLIC SECTION.",
        "    INTERFACES if_reauth_relevancy_check.",
        "ENDCLASS.",
        "",
        "CLASS zcl_po_reauth_check IMPLEMENTATION.",
        "  METHOD if_reauth_relevancy_check~is_reauthentication_relevant.",
        "    \" Step 1: Identify which fields changed in this save",
        "    \" Step 2: Call framework utility to get configured regulated fields",
        "    \"         from S-table VC_SRA_SOT for PURCHASE_ORDER object",
        "    \" Step 3: Compare changed fields against regulated field list",
        "    \" Step 4: Return ABAP_TRUE if any regulated field changed",
        "    \"         Return ABAP_FALSE if nothing regulated changed",
        "    \"",
        "    \" WARNING: If this returns ABAP_FALSE due to a bug,",
        "    \"          reauthentication is SILENTLY SKIPPED",
        "  ENDMETHOD.",
        "ENDCLASS.",
    ]))

    els.append(sp(8))
    els.append(Paragraph("2.2  S-Table Configuration (SPRO → VC_SRA_SOT)", H2))
    els.append(Paragraph(
        "Register the PURCHASE_ORDER reauthentication object in S4 via SPRO. "
        "This content is delivered via scope item 84P transport — "
        "customer can fine-tune the regulated field list after activation.", BODY))

    els.append(code_block([
        "SPRO → GxP Compliance → Reauthentication Settings → VC_SRA_SOT",
        "",
        "Object:           PURCHASE_ORDER",
        "Reauth Class:     ZCL_PO_REAUTH_CHECK   ← LOB implements this",
        "Auth Class:       ZCL_PO_AUTH_CHECK      ← LOB implements this",
        "",
        "Node definitions:",
        "  Node:  PO_HEADER_EXT",
        "  Table: /ATO/S4_PO_HEADER_EXT",
        "  Regulated Fields:",
        "    THERAPY_TYPE     ← triggers reauthentication if changed",
        "    CLINICAL_STUDY   ← triggers reauthentication if changed",
        "    PROTOCOL_REF     ← triggers reauthentication if changed",
        "",
        "  Node:  PO_ITEM_EXT",
        "  Table: /ATO/S4_PO_ITEM_EXT",
        "  Regulated Fields:",
        "    THERAPY_TYPE     ← triggers reauthentication if changed",
        "    PATIENT_REF      ← triggers reauthentication if changed",
    ]))

    els.append(sp(8))
    els.append(Paragraph("2.3  BTP Configuration — Reason Codes", H2))
    els.append(tbl(
        ["Step", "Activity", "Who"],
        [
            ["1", "Register PURCHASE_ORDER object in BTP eSignature SaaS",                    "GxP Compliance Team"],
            ["2", "Define reason codes for PURCHASE_ORDER",                                    "GxP Compliance Team"],
            ["3", "Verify only PO reason codes appear in PO reauthentication dropdown",        "GxP Compliance Team"],
            ["4", "Suggested reason codes: Clinical Protocol Update, Regulatory Submission,\nError Correction, Therapy Type Reassignment", "LOB team proposes"],
        ],
        widths=[1.2*cm, 12.3*cm, 4*cm]
    ))
    els.append(PageBreak())
    return els

# ── Section 3: Test cases ─────────────────────────────────────────────────────
def section3():
    els = []
    els.append(sec_hdr("Section 3 — Test Cases", SAP_DARK))
    els.append(sp(10))

    els.append(info_box(
        "Test cases are ordered by dependency. Test 1 must pass before Test 2. "
        "Tests 1–2 can be executed TODAY. Tests 3–5 require 2702 delivery."
    ))
    els.append(sp(8))

    # Test 1
    els.append(test_card(
        1, "Verify Change Document for PO",
        prereq=None,
        steps=(
            "1. ME21N → create a new Purchase Order with any vendor and material\n"
            "2. Save the PO — note the PO number (e.g. 4500000123)\n"
            "3. ME22N → open the same PO → change a field (e.g. Delivery Date)\n"
            "4. Save the change\n"
            "5. ME23N → Environment menu → Changes\n"
            "   OR SE16N → CDHDR → filter: OBJECTCLAS = EINKBELEG, OBJECTID = 4500000123\n"
            "6. Check CDPOS for the same CHANGENR"
        ),
        verify=(
            "CDHDR: one row with OBJECTCLAS=EINKBELEG, USERNAME=your user, UDATE=today\n"
            "CDPOS: one row with FNAME=changed field, VALUE_OLD=old value, VALUE_NEW=new value"
        ),
        expected_result="Change Document created correctly — field change recorded with old and new values",
        status="✅ Testable NOW",
        status_color=GREEN_OK
    ))

    # Test 2
    els.append(test_card(
        2, "Verify GxP Active Check (CHECK_ESIG_ACTIVE)",
        prereq="SE24 or ABAP Console access",
        steps=(
            "Run CHECK_ESIG_ACTIVE API from ABAP console or SE38:\n"
            "  DATA lv_active TYPE abap_bool.\n"
            "  \" Call framework CHECK_ESIG_ACTIVE method\n"
            "  \" Log result to console\n\n"
            "Also verify in SPRO:\n"
            "  SPRO → GxP Compliance → check scope item 84P activation status"
        ),
        verify="Result of CHECK_ESIG_ACTIVE call",
        expected_result=(
            "Returns ABAP_FALSE — EXPECTED in current state (Communication Arrangement not yet configured).\n"
            "Returns ABAP_TRUE only when: scope item 84P active AND BTP Communication Arrangement configured"
        ),
        status="✅ Testable NOW",
        status_color=GREEN_OK
    ))

    # Test 3
    els.append(test_card(
        3, "Reauthentication Dialog Appears on Regulated Field Change",
        prereq=(
            "✓ Scope item 84P activated\n"
            "✓ Communication Arrangement configured (S4 → BTP eSignature SaaS)\n"
            "✓ ZCL_PO_REAUTH_CHECK implemented and registered in VC_SRA_SOT\n"
            "✓ PURCHASE_ORDER registered in BTP with reason codes defined"
        ),
        steps=(
            "1. ME21N → create a new PO\n"
            "2. Enter THERAPY_TYPE = CELL_GENE in the ATO Advanced Therapy Information tab\n"
            "3. Click Save"
        ),
        verify="Reauthentication dialog appears before PO is committed",
        expected_result=(
            "Dialog shown with:\n"
            "  - Password field (must re-enter — session token not sufficient)\n"
            "  - Reason Code dropdown showing only PO-specific codes\n"
            "  - Confirm and Cancel buttons"
        ),
        status="🔲 Requires 2702",
        status_color=GOLD
    ))

    # Test 4
    els.append(test_card(
        4, "Signature Captured and Linked to Change Document",
        prereq="All prerequisites from Test 3",
        steps=(
            "1. Complete Test 3 — dialog appears\n"
            "2. Enter correct SAP password\n"
            "3. Select reason code: 'Clinical Protocol Update'\n"
            "4. Click Confirm\n"
            "5. PO saves successfully\n"
            "6. Note the PO number and timestamp"
        ),
        verify=(
            "S4: SE16N → CDHDR → find CHANGENR for the PO\n"
            "    CDPOS → FNAME=THERAPY_TYPE, VALUE_OLD='', VALUE_NEW='CELL_GENE'\n"
            "BTP: eSignature SaaS admin console → find Signature record:\n"
            "    - Signature ID linked to CHANGENR\n"
            "    - User = I308878 (your user)\n"
            "    - Timestamp matches save time\n"
            "    - Reason Code = Clinical Protocol Update\n"
            "    - Credential hash present"
        ),
        expected_result="Complete GxP audit trail: CDHDR/CDPOS (what changed) + BTP Signature (who approved it intentionally)",
        status="🔲 Requires 2702",
        status_color=GOLD
    ))

    # Test 5
    els.append(test_card(
        5, "Cancel Path — Save Must Be Fully Rolled Back",
        prereq="All prerequisites from Test 3",
        steps=(
            "1. ME21N → open a PO → change THERAPY_TYPE\n"
            "2. Click Save → reauthentication dialog appears\n"
            "3. Click CANCEL on the dialog"
        ),
        verify=(
            "S4: SE16N → CDHDR → confirm NO new entry for this PO at this timestamp\n"
            "S4: SE16N → /ATO/S4_PO_HEADER_EXT → confirm field value NOT changed\n"
            "ME21N: reopen the PO → confirm THERAPY_TYPE still has the original value"
        ),
        expected_result=(
            "PO save ABORTED — nothing committed to database.\n"
            "EKKO, EKPO, extension tables, CDHDR/CDPOS all unchanged.\n"
            "GxP integrity preserved — no partial save."
        ),
        status="🔲 Requires 2702",
        status_color=GOLD
    ))

    # Test 6
    els.append(test_card(
        6, "Non-Regulated Field Change — No Dialog",
        prereq="All prerequisites from Test 3",
        steps=(
            "1. ME21N → open a PO → change a NON-regulated field only\n"
            "   (e.g. Purchase Order Text, Payment Terms)\n"
            "2. Click Save"
        ),
        verify="No reauthentication dialog appears — PO saves immediately",
        expected_result=(
            "PO saved without dialog — Relevancy Check returned ABAP_FALSE.\n"
            "Change Document still created for the changed field.\n"
            "No signature record created in BTP — correct behaviour."
        ),
        status="🔲 Requires 2702",
        status_color=GOLD
    ))

    # Test 7
    els.append(test_card(
        7, "Unit Test — Relevancy Check Callback",
        prereq="ZCL_PO_REAUTH_CHECK implemented in SE24",
        steps=(
            "Create ABAP unit test class for ZCL_PO_REAUTH_CHECK:\n\n"
            "Test Case A — Regulated field changed:\n"
            "  Simulate: THERAPY_TYPE changed from '' to 'CELL_GENE'\n"
            "  Expected: returns ABAP_TRUE\n\n"
            "Test Case B — Non-regulated field changed:\n"
            "  Simulate: DELIVERY_DATE changed\n"
            "  Expected: returns ABAP_FALSE\n\n"
            "Test Case C — No fields changed:\n"
            "  Simulate: no field changes\n"
            "  Expected: returns ABAP_FALSE\n\n"
            "Test Case D — Error in callback:\n"
            "  Simulate: exception raised inside callback\n"
            "  Expected: framework treats as FALSE — reauthentication skipped"
        ),
        verify="All 4 test cases pass in SE80 unit test runner",
        expected_result="All test cases pass — Relevancy Check behaves correctly for all scenarios",
        status="✅ Testable NOW (once class built)",
        status_color=GREEN_OK
    ))

    return els

# ── Section 4: contacts ───────────────────────────────────────────────────────
def section4():
    els = []
    els.append(PageBreak())
    els.append(sec_hdr("Section 4 — Contacts &amp; Current Status Summary", SAP_BLUE))
    els.append(sp(10))

    els.append(Paragraph("4.1  Key Contacts for Testing", H2))
    els.append(tbl(
        ["Name", "Role", "Contact For"],
        [
            ["Swarnava Chatterjee", "eSignature Integration Lead",           "BTP eSignature SaaS test system access, Communication Arrangement setup"],
            ["Yadesh Gupta",        "Reauthentication Framework Architect",  "Framework APIs, S-table config, VC_SRA_SOT questions"],
            ["Prabir Kumar Mallick","Reauthentication Framework Dev Lead",   "Technical implementation questions, BTP side config"],
            ["Nils Hartmann",       "Purchase Order Product Owner",          "ME21N integration point, PO app questions"],
            ["Satish Kumar",        "ATO/CGTO PM + Architecture",            "ATO extension fields, /ATO/S4_PO_HEADER_EXT questions"],
        ],
        widths=[4.5*cm, 5.5*cm, 7.5*cm]
    ))
    els.append(sp(8))

    els.append(Paragraph("4.2  Test Execution Status Summary", H2))
    els.append(tbl(
        ["Test", "Description", "Can Test Now?", "Blocker"],
        [
            ["Test 1", "Change Document for PO",                    "✅ YES",  "None — already verified 2608"],
            ["Test 2", "GxP Active Check (CHECK_ESIG_ACTIVE)",      "✅ YES",  "None — will return FALSE (expected)"],
            ["Test 7", "Unit Test Relevancy Check Callback",        "✅ YES*", "*Once ZCL_PO_REAUTH_CHECK is built"],
            ["Test 3", "Reauthentication dialog in ME21N",          "🔲 NO",   "Needs 2702: ME21N integration + Comm Arrangement"],
            ["Test 4", "Signature captured + linked to Change Doc", "🔲 NO",   "Needs 2702: BTP eSignature SaaS connected"],
            ["Test 5", "Cancel path — full rollback",               "🔲 NO",   "Needs 2702: ME21N integration"],
            ["Test 6", "Non-regulated field — no dialog",           "🔲 NO",   "Needs 2702: Relevancy Check integrated into ME21N"],
        ],
        widths=[1.5*cm, 6.5*cm, 3*cm, 6.5*cm]
    ))
    els.append(sp(8))

    els.append(Paragraph("4.3  Delivery Roadmap", H2))
    els.append(tbl(
        ["Release", "Deliverable", "Status"],
        [
            ["2608 (done)", "Change Document for PO verified for all regulated fields",        "✅ Complete"],
            ["2702 (planned)", "eSignature trigger in ME21N save flow",                        "🔲 Planned"],
            ["2702 (planned)", "Communication Arrangement S4 ↔ BTP eSignature SaaS",          "🔲 Planned"],
            ["2702 (planned)", "Relevancy Check callback ZCL_PO_REAUTH_CHECK",                "🔲 Planned"],
            ["2702 (planned)", "S-table VC_SRA_SOT registration for PURCHASE_ORDER",          "🔲 Planned"],
            ["2702 (planned)", "BTP: Reason codes for PURCHASE_ORDER via 84P provisioning",   "🔲 Planned"],
            ["2702 (planned)", "ATO extension field registration in Change Document object",   "🔲 Planned — open issue"],
            ["Post 2702",      "eSignature in modernised Manage PO App (BOF replacement)",    "⏳ Deferred"],
        ],
        widths=[3.5*cm, 10*cm, 4*cm]
    ))
    return els

# ── Build ─────────────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title="GxP eSignature Reauthentication Integration Test Guide",
        author="SAP S/4HANA GxP Team",
    )

    story = []
    story.extend(cover())
    story.extend(section1())
    story.extend(section2())
    story.extend(section3())
    story.extend(section4())

    def on_page(c, doc):
        c.saveState()
        c.setFont("Helvetica", 7)
        c.setFillColor(colors.HexColor("#888888"))
        c.drawString(2*cm, 1.2*cm, "GxP eSignature & Reauthentication — Integration Details & Test Guide")
        c.drawRightString(19.5*cm, 1.2*cm, f"Page {doc.page}")
        c.setStrokeColor(GREY_BORDER)
        c.setLineWidth(0.4)
        c.line(2*cm, 1.5*cm, 19.5*cm, 1.5*cm)
        c.restoreState()

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF created: {OUTPUT}")

build()
