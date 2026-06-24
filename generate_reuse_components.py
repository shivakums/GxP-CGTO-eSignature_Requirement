from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUTPUT = r"C:\Users\I308878\GxP-CGTO-eSignature_Requirement\GxP_Reuse_Components_Reference.pdf"

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
GREY_BG       = colors.HexColor("#F5F5F5")
GREY_BORDER   = colors.HexColor("#CCCCCC")
WHITE         = colors.white
BLACK         = colors.black

W, H = A4

# ── Styles ────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def ms(name, **kw):
    return ParagraphStyle(name=name, parent=styles["Normal"], **kw)

TITLE     = ms("T",  fontSize=22, textColor=WHITE,    fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=4)
SUBTITLE  = ms("ST", fontSize=11, textColor=colors.HexColor("#AACCFF"), fontName="Helvetica", alignment=TA_CENTER, spaceAfter=2)
META      = ms("M",  fontSize=8,  textColor=colors.HexColor("#AACCFF"), fontName="Helvetica", alignment=TA_CENTER)
H1        = ms("H1", fontSize=14, textColor=WHITE,    fontName="Helvetica-Bold", spaceAfter=4, spaceBefore=2)
H2        = ms("H2", fontSize=11, textColor=SAP_DARK, fontName="Helvetica-Bold", spaceAfter=4, spaceBefore=8)
H3        = ms("H3", fontSize=9,  textColor=SAP_BLUE, fontName="Helvetica-Bold", spaceAfter=3, spaceBefore=5)
BODY      = ms("B",  fontSize=8.5,textColor=BLACK,    leading=13, spaceAfter=3, alignment=TA_JUSTIFY)
BODY_SML  = ms("BS", fontSize=8,  textColor=BLACK,    leading=12, spaceAfter=2)
NOTE      = ms("N",  fontSize=7.5,textColor=colors.HexColor("#444444"), leading=11, leftIndent=8, spaceAfter=2, fontName="Helvetica-Oblique")
QUOTE     = ms("Q",  fontSize=8,  textColor=colors.HexColor("#333333"), leading=12, leftIndent=14, spaceAfter=3, fontName="Helvetica-Oblique")
BULL      = ms("BU", fontSize=8.5,textColor=BLACK,    leading=13, leftIndent=14, spaceAfter=2)
TH        = ms("TH", fontSize=8,  textColor=WHITE,    fontName="Helvetica-Bold", alignment=TA_CENTER)
TC        = ms("TC", fontSize=8,  textColor=BLACK,    leading=11)
TC_C      = ms("TCC",fontSize=8,  textColor=BLACK,    leading=11, alignment=TA_CENTER)
BADGE_L   = ms("BL", fontSize=9,  textColor=WHITE,    fontName="Helvetica-Bold", alignment=TA_CENTER)

# ── Helpers ───────────────────────────────────────────────────────────────────
def sp(n=6): return Spacer(1, n)

def hline(color=SAP_BLUE, t=0.8):
    return HRFlowable(width="100%", thickness=t, color=color, spaceAfter=4, spaceBefore=4)

def sec_hdr(title, color=SAP_DARK):
    t = Table([[Paragraph(title, H1)]], colWidths=[17.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), color),
        ("TOPPADDING",    (0,0),(-1,-1), 9),
        ("BOTTOMPADDING", (0,0),(-1,-1), 9),
        ("LEFTPADDING",   (0,0),(-1,-1), 14),
    ]))
    return t

def tbl(headers, rows, widths=None, stripe=True):
    n = len(headers)
    if not widths:
        widths = [17.5*cm/n]*n
    data = [[Paragraph(h, TH) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), TC) for c in row])
    style = [
        ("BACKGROUND",    (0,0), (-1,0),  SAP_BLUE),
        ("GRID",          (0,0), (-1,-1), 0.4, GREY_BORDER),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ]
    if stripe:
        style.append(("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE, GREY_BG]))
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle(style))
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

def component_card(number, name, comp_type, system, status,
                   description, details_rows, quote=None,
                   hdr_color=SAP_BLUE, bg_color=SAP_LIGHT):
    """Full component card with badge, description, detail table, optional quote."""
    els = []

    # header bar with badge + name
    badge_cell = Paragraph(str(number), BADGE_L)
    name_cell  = Paragraph(f"<b>{name}</b>", ms(f"cn{number}", fontSize=11,
                            textColor=WHITE, fontName="Helvetica-Bold"))
    type_cell  = Paragraph(f"{comp_type}  |  {system}  |  {status}",
                            ms(f"ct{number}", fontSize=8, textColor=colors.HexColor("#CCDDFF"),
                               fontName="Helvetica"))

    hdr = Table(
        [[badge_cell, [name_cell, type_cell]]],
        colWidths=[1*cm, 16.5*cm]
    )
    hdr.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), hdr_color),
        ("TOPPADDING",    (0,0),(-1,-1), 8),
        ("BOTTOMPADDING", (0,0),(-1,-1), 8),
        ("LEFTPADDING",   (0,0),(-1,-1), 10),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ]))
    els.append(hdr)

    # description
    body = Table([[Paragraph(description, BODY_SML)]],
                 colWidths=[17.5*cm])
    body.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), bg_color),
        ("TOPPADDING",   (0,0),(-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
        ("LEFTPADDING",  (0,0),(-1,-1), 10),
        ("RIGHTPADDING", (0,0),(-1,-1), 8),
    ]))
    els.append(body)

    # detail table
    dt = Table(
        [[Paragraph(k, ms(f"dk{number}", fontSize=7.5, textColor=SAP_DARK,
                          fontName="Helvetica-Bold")),
          Paragraph(v, ms(f"dv{number}", fontSize=7.5, textColor=BLACK, leading=11))]
         for k, v in details_rows],
        colWidths=[3.8*cm, 13.7*cm]
    )
    dt.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(0,-1),  colors.HexColor("#F0F4FA")),
        ("BACKGROUND",    (1,0),(1,-1),  bg_color),
        ("GRID",          (0,0),(-1,-1), 0.3, GREY_BORDER),
        ("TOPPADDING",    (0,0),(-1,-1), 4),
        ("BOTTOMPADDING", (0,0),(-1,-1), 4),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
    ]))
    els.append(dt)

    # optional quote
    if quote:
        qt = Table([[Paragraph(f'"{quote}"', QUOTE)]],
                   colWidths=[17.5*cm])
        qt.setStyle(TableStyle([
            ("BACKGROUND",   (0,0),(-1,-1), colors.HexColor("#FFFBE6")),
            ("LINEBEFORE",   (0,0),(0,-1),  3, GOLD),
            ("TOPPADDING",   (0,0),(-1,-1), 5),
            ("BOTTOMPADDING",(0,0),(-1,-1), 5),
            ("LEFTPADDING",  (0,0),(-1,-1), 10),
        ]))
        els.append(qt)

    # bottom border
    border = Table([[""]], colWidths=[17.5*cm], rowHeights=[2])
    border.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1), hdr_color)]))
    els.append(border)
    els.append(sp(10))

    return KeepTogether(els)

# ── Cover ─────────────────────────────────────────────────────────────────────
def cover():
    els = []
    cov = Table([
        [Paragraph("GxP / CGTO / ATO / eSignature", TITLE)],
        [Paragraph("Reuse Components Reference Guide", SUBTITLE)],
        [Paragraph("SAP S/4HANA + BTP  |  Life Science  |  2026-06-24", META)],
    ], colWidths=[17.5*cm])
    cov.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), SAP_DARK),
        ("TOPPADDING",    (0,0),(-1,-1), 32),
        ("BOTTOMPADDING", (0,0),(-1,-1), 32),
        ("LEFTPADDING",   (0,0),(-1,-1), 20),
    ]))
    els.append(cov)
    els.append(sp(14))

    els.append(Paragraph("Purpose of This Document", H2))
    els.append(Paragraph(
        "This document identifies and describes all reuse components referenced across the "
        "GxP Compliance, CGTO/ATO Integration, eSignature, and Reauthentication project for "
        "SAP S/4HANA Purchase Order. Sources: CGTO PO Alignment meeting (2026-06-12), "
        "ATO to S4 PuC Integration Demo (2026-06-17), and Reauthentication Framework session (2026-06-18).",
        BODY))
    els.append(sp(8))

    # summary table
    els.append(Paragraph("All Reuse Components at a Glance", H2))
    els.append(tbl(
        ["#", "Component", "Type", "System", "Status"],
        [
            ["1", "BTP eSignature SaaS",             "SaaS Service",            "BTP",              "Available — integration planned 2702"],
            ["2", "Reauthentication Framework",       "ABAP Platform Layer",     "S4",               "Available — LOB implements callback"],
            ["3", "Integration Suite iFlow (CPI)",    "Middleware",              "BTP Integ. Suite", "Built for private cloud — porting to public"],
            ["4", "Event Mesh",                       "Async Event Bus",         "BTP",              "Active"],
            ["5", "Change Document Framework",        "S4 Standard Framework",   "S4",               "Verified for PO 2608 ✓ — open issue on ATO fields"],
            ["6", "PurchaseOrder OData API",          "S4 Standard API",         "S4",               "Extension enabled by PO team on request"],
            ["7", "Industry Object Extension",        "Architecture Pattern",    "S4",               "Approved — first public cloud use by ATO"],
            ["8", "Scope Item 84P",                   "SAP Content Delivery",   "S4 + BTP",         "Planned — LOBs contribute field configs"],
        ],
        widths=[0.8*cm, 4.5*cm, 4*cm, 3.5*cm, 4.7*cm]
    ))
    els.append(sp(12))

    # open issue callout
    els.append(warn_box(
        "⚠  Open Issue: Change Document display for ATO extension fields is NOT visible in "
        "ME22N/ME23N change log screen. ATO extension table /ATO/S4_PO_HEADER_EXT is written to "
        "CDPOS but does not surface in the standard PO change log UI. "
        "A potential BAdI 'Change Document Processing' was identified by Jiss (PO team) — "
        "needs investigation. Joint call required: ATO team + PO standard team + Change Document team."
    ))
    els.append(PageBreak())
    return els

# ── Components ────────────────────────────────────────────────────────────────
def components():
    els = []
    els.append(sec_hdr("Reuse Component Details", SAP_DARK))
    els.append(sp(10))

    # ── 1. eSignature SaaS ───────────────────────────────────────────────────
    els.append(component_card(
        1, "BTP eSignature SaaS Service",
        "SaaS Service", "BTP", "Available — integration planned 2702",
        "A shared, reusable SaaS service already available on BTP. It does NOT need to be built "
        "per LOB — it exists as a single instance that any S4 application can integrate with via "
        "a Communication Arrangement. It captures re-authentication credentials, creates a "
        "tamper-proof signature record, and links it to the S4 Change Document number (CHANGENR).",
        [
            ("Owner",          "Yadesh Gupta / Prabir Kumar Mallick (framework) + Swarnava Chatterjee (eSignature product)"),
            ("What it stores", "Signature ID, User ID, Timestamp, Reason Code, Credential hash — tamper-proof"),
            ("Auth methods",   "SAP password, PIN, biometric, external IdP — configurable per object"),
            ("Integration",    "Communication Arrangement in S4 — same pattern as SAP_COM_0267"),
            ("Consumers",      "ME21N (WS1), Sales Order, Process Order, Maintenance Order — all share the same service"),
            ("Key rule",       "Must re-enter credentials — existing session token is NOT sufficient for GxP compliance"),
        ],
        quote="The eSignature reusable service is already available as a SaaS on BTP. "
              "It does NOT need to be built — it needs to be integrated into LOB applications.",
        hdr_color=ESIGN_TEAL, bg_color=ESIGN_LIGHT
    ))

    # ── 2. Reauthentication Framework ────────────────────────────────────────
    els.append(component_card(
        2, "Reauthentication Reuse Framework (S4 Platform Layer)",
        "ABAP Platform Framework", "S4", "Available — LOB implements one callback class",
        "A platform-level reusable ABAP framework in S4 that any LOB application registers with "
        "to enforce GxP reauthentication. The design goal is one common UX and one common platform "
        "layer — every S4 application that needs GxP reauthentication integrates here instead of "
        "building its own signature flow. The LOB only implements ONE callback class (Relevancy Check). "
        "Everything else — calling BTP, capturing signature, linking to Change Doc — is handled by the framework.",
        [
            ("S-table config",   "VC_SRA_SOT — registers: object name, callback class, auth class, node types, field list"),
            ("APIs exposed",     "REQUEST_REAUTH (OData variant), REQUEST_REAUTH (library), VALIDATE_RESULT, CHECK_ESIG_ACTIVE"),
            ("Utility method",   "Framework provides utility to read regulated field list from S-table — LOB does not query directly"),
            ("Display reauth",   "Separate dedicated class for display-mode reauthentication (no edit event)"),
            ("LOB implements",   "Only ONE callback class: Relevancy Check → returns ABAP_TRUE/FALSE"),
            ("Warning",          "If Relevancy Check returns ABAP_FALSE due to a bug → reauthentication silently skipped"),
            ("Confirmed users",  "Purchase Order (WS1), Process Order (Asset Mgmt — Niranjan/Ajith), Sales Order, Maintenance Order"),
        ],
        quote="We want to have a reuse framework at least from our platform layer so that each and "
              "every application which is there in S4 side can integrate to this GxP compliance "
              "thing and can have a common user experience for everybody. — Yadesh Gupta",
        hdr_color=REAUTH_PURPLE, bg_color=REAUTH_LIGHT
    ))

    # ── 3. iFlow ─────────────────────────────────────────────────────────────
    els.append(component_card(
        3, "Integration Suite iFlow (CPI — Middleware)",
        "Middleware", "BTP Integration Suite", "Built for private cloud — being ported to public cloud",
        "The iFlow is the middleware layer between ATO SaaS (BTP) and S4. It is required because "
        "ATO SaaS and S4 have DIFFERENT event schemas — the iFlow bridges the schema gap in both "
        "directions. It is not a replication layer; it performs schema mapping and event routing only.",
        [
            ("Why needed",      "ATO BTP schema and S4 event schema are different — iFlow maps between them in both directions"),
            ("Directions",      "BTP→S4: maps ATO event payload → S4 PurchaseOrder API format. S4→BTP: maps PO change event → ATO schema"),
            ("Not replication", "Confirmed by Loring Wu: 'It is not a replication, it is just a linkage between the documents'"),
            ("Subscriber acct", "BTP subscriber account publishes/receives from Event Mesh via iFlow"),
            ("Scope",           "Handles PO create, PO update, PO cancel events. Also Sales Order, Process Order, Production Order"),
            ("Public cloud gap","Private cloud used legacy BAPI-based iFlows — being redesigned for public cloud OData API pattern"),
        ],
        quote="We have the middleware CPI. CPO will convert the payload according to S4 purchase order API "
              "and call the API to create the purchase order. — Loring Wu",
        hdr_color=BTP_GREEN, bg_color=BTP_LIGHT
    ))

    # ── 4. Event Mesh ─────────────────────────────────────────────────────────
    els.append(component_card(
        4, "BTP Event Mesh",
        "Async Event Bus", "BTP", "Active",
        "SAP BTP Event Mesh is the shared async messaging infrastructure used for all bidirectional "
        "event exchange between ATO SaaS (BTP) and S4. It decouples the two systems so they operate "
        "independently — events are published and consumed asynchronously.",
        [
            ("Events from S4",  "PurchaseOrder.Created, PurchaseOrder.Changed — includes standard fields + ATO extension fields"),
            ("Events from ATO", "PO Create request, PO Update request (collection qty, patient ID, protocol ID), PO Cancellation"),
            ("Pattern",         "Publish-subscribe — ATO SaaS subscribes to S4 PO events via subscriber account"),
            ("Outbound events", "S4 publishes outbound event on every PO change relevant to ATO — even when user edits in ME21N"),
            ("Scope",           "Also used for Sales Order, Process Order, Production Order, Stock events"),
        ],
        hdr_color=BTP_GREEN, bg_color=BTP_LIGHT
    ))

    els.append(PageBreak())

    # ── 5. Change Document ────────────────────────────────────────────────────
    els.append(sec_hdr("Reuse Component Details (continued)", SAP_DARK))
    els.append(sp(10))

    els.append(component_card(
        5, "Change Document Framework",
        "S4 Standard Framework", "S4", "Verified for PO 2608 ✓ — open issue on ATO extension fields",
        "The standard SAP Change Document framework (CDHDR/CDPOS) is the audit trail backbone for "
        "GxP compliance. It records who changed what, when, with old and new values. "
        "It is the PREREQUISITE for eSignature — eSignature links its signature record to the "
        "Change Document number (CHANGENR). Without Change Document, eSignature has no anchor point.",
        [
            ("Tables",          "CDHDR: change doc header (object class, PO number, user, date/time). CDPOS: one row per changed field with VALUE_OLD/VALUE_NEW"),
            ("ATO registration","ATO extension table /ATO/S4_PO_HEADER_EXT must be explicitly registered in the CD object to appear in CDPOS"),
            ("eSign dependency","Signature ID from BTP is linked to CHANGENR — CD must fire before eSignature can attach"),
            ("Verified 2608",   "Change Document verified working for all standard PO fields in release 2608 ✓"),
            ("Open issue",      "ATO extension field changes appear in CDPOS but are NOT visible in ME22N/ME23N change log UI"),
            ("Possible BAdI",   "Jiss (PO team) identified BAdI 'Change Document Processing' — may surface extension changes. Not confirmed."),
            ("Action needed",   "Joint call: ATO team (Allen Yuan/Loring Wu) + PO standard team (Jiss) + Change Document team"),
        ],
        quote="For the change log, we needed to extend the standard change document object to include "
              "our ATO table, then the change can be recorded. But since the object is a separate ATO "
              "table, no description is displayed in ME22N directly. — Allen Yuan (ATO team)",
        hdr_color=SAP_DARK, bg_color=colors.HexColor("#EEF2F8")
    ))

    # ── 6. PurchaseOrder OData API ────────────────────────────────────────────
    els.append(component_card(
        6, "PurchaseOrder OData API Extension",
        "S4 Standard API — Extended", "S4", "Extension enabled by PO team on ATO request",
        "The standard S4 PurchaseOrder OData V4 API extended with ATO industry fields. "
        "ATO does NOT have a separate standalone API — it extends the standard one so that "
        "standard PO fields and ATO extension fields are created/updated in a single API call. "
        "The extension was NOT enabled by default and required the PO standard team to enable it.",
        [
            ("Extension type",  "Industry Object Extension node associated to PurchaseOrder entity — TherapyType, ClinicalStudy, ProtocolRef, PatientRef"),
            ("Why not separate","Extension node data is dependent on PO — cannot exist without the standard document. Separate API would break this dependency."),
            ("Who enabled it",  "Nils Hartmann / Jiss (PO standard team) — ATO raised limitation during POC, PO team planned and delivered the enablement"),
            ("ATO usage",       "ATO calls this single API for PO creation — standard fields + ATO extension fields in one payload"),
            ("Confirmed by",    "Loring Wu: 'The extension was not enabled in the purchase order API, so we reached out to your team to enable it'"),
            ("Governance",      "Any further API extension changes require Suite Architecture review (Felix Vente — North Star)"),
        ],
        quote="We should not touch or we should not change anything of the standard objects. "
              "In case we face any restriction, we need to reach out to your team to enable "
              "the extensibility. — Loring Wu",
        hdr_color=S4_ORANGE, bg_color=S4_LIGHT
    ))

    # ── 7. Industry Object Extension ──────────────────────────────────────────
    els.append(component_card(
        7, "Industry Object Extension Pattern",
        "Architecture Pattern", "S4", "Approved — first public cloud use by ATO/CGTO",
        "The SAP-approved extensibility pattern for adding industry-specific fields to standard "
        "S4 business objects (EKKO/EKPO) without modifying the standard tables. "
        "ATO is the FIRST Life Science industry to use this pattern in public cloud — "
        "Discrete and Retail used similar approaches before the code split via a different path.",
        [
            ("Why not native",  "ATO requires THREE levels of extension (header, item, third-level). Native extension supports only two levels."),
            ("POC outcome",     "Loring Wu: 'After POC with native extension and separate BO, conclusion: separate BO because of third-layer extension'"),
            ("Approved by",     "Felix Vente (Suite Architecture — North Star governance)"),
            ("Tables created",  "/ATO/S4_PO_HEADER_EXT (FK → EKKO.EBELN): TherapyType, ClinicalStudy, ProtocolRef"),
            ("",                "/ATO/S4_PO_ITEM_EXT (FK → EKPO.EBELN+EBELP): TherapyType, PatientRef"),
            ("Key rule",        "NEVER append fields directly to EKKO/EKPO — always via Industry Object Extension node"),
            ("Reuse scope",     "Same pattern applied across PO, Sales Order, Process Order, Production Order — not PO-specific"),
        ],
        quote="We are the first one in public cloud to integrate for creation of purchase order for "
              "Life Science. We started working with Nils and Jiss together with the Suite architecture "
              "team in public cloud, which is led by Felix Vente. — Sathishkumar Meenakshisundaram",
        hdr_color=SAP_BLUE, bg_color=SAP_LIGHT
    ))

    # ── 8. Scope Item 84P ─────────────────────────────────────────────────────
    els.append(component_card(
        8, "Scope Item 84P — GxP Compliance",
        "SAP Content Delivery", "S4 + BTP", "Planned — LOBs contribute their field configs",
        "The central SAP scope item for GxP compliance. When activated in S4, it enables the "
        "Reauthentication Framework and loads the S-table entries. It also triggers automatic "
        "provisioning of reason codes in the BTP tenant. LOB teams (e.g. PO team) ship their "
        "specific regulated field lists and S-table configurations inside 84P — all LOBs share "
        "the same scope item, not one per LOB.",
        [
            ("What it activates","Reauthentication Framework in S4, Communication Arrangement to BTP eSignature, S-table baseline entries"),
            ("BTP provisioning", "Reason codes defined for each business object are auto-loaded in BTP tenant when 84P activates"),
            ("LOB contribution", "Each LOB ships their object registration + node types + regulated field list inside 84P transport"),
            ("Customer tuning",  "After activation, customer can fine-tune field list (remove/add fields) and customise reason codes in BTP"),
            ("All LOBs share",   "One 84P scope item used by PO, Sales Order, Process Order, Maintenance Order — not duplicated per LOB"),
            ("Delivery model",   "S-table content (object + fields) delivered via 84P transport. Reason codes delivered via BTP content"),
        ],
        hdr_color=GOLD, bg_color=GOLD_LIGHT
    ))

    return els

# ── Open Issue Section ────────────────────────────────────────────────────────
def open_issues():
    els = []
    els.append(PageBreak())
    els.append(sec_hdr("Open Issue — Change Document Display for ATO Extension Fields", RED))
    els.append(sp(10))

    els.append(Paragraph("What Was Raised", H2))
    els.append(Paragraph(
        "In the ATO to S4 PuC Integration Demo meeting (2026-06-17), Allen Yuan (ATO team) "
        "demonstrated a specific challenge: when ATO extension fields (e.g. THERAPY_TYPE) are "
        "changed and written to CDHDR/CDPOS, the change log entries are NOT visible in the "
        "standard ME22N / ME23N change log screen. This is a reuse challenge — the Change Document "
        "Framework works correctly, but the display layer does not surface extension table records "
        "alongside standard PO field changes.", BODY))
    els.append(sp(6))

    els.append(tbl(
        ["Aspect", "Detail"],
        [
            ["What works",     "ATO extension field changes ARE written to CDPOS with TABNAME=/ATO/S4_PO_HEADER_EXT — data is recorded correctly"],
            ["What does not",  "ME22N / ME23N change log screen does not display these CDPOS rows alongside standard PO change rows"],
            ["Root cause",     "The standard PO change document object does not include /ATO/S4_PO_HEADER_EXT in its registered table list"],
            ["Option A",       "Extend the standard PO change document object to include /ATO/S4_PO_HEADER_EXT — requires standard team involvement"],
            ["Option B",       "BAdI 'Change Document Processing' identified by Jiss (PO team) — may surface extension rows. Not yet confirmed."],
            ["Sales Order ref","ATO extension for Sales Order handled by RAP/BOPF framework automatically — different path than PO (Web GUI)"],
            ["Confirmed by",   "Allen Yuan (ATO), Jiss Nimmi Augustine (PO standard), Nils Hartmann (PO Product Owner)"],
            ["Action",         "Joint call required: ATO team (Allen Yuan / Loring Wu) + PO standard team (Jiss) + Change Document team"],
        ],
        widths=[4*cm, 13.5*cm]
    ))
    els.append(sp(8))

    els.append(Paragraph("Why This Matters for GxP", H2))
    els.append(info_box(
        "For GxP compliance (21 CFR Part 11), the complete change history of all regulated fields "
        "must be visible in a single, unified audit trail view. If the ATO extension field changes "
        "(Therapy Type, Clinical Study, Protocol) appear in CDPOS but are invisible in the standard "
        "change log screen, auditors cannot see the complete regulated field history in one place. "
        "This is a GxP compliance gap that must be resolved before 2702 delivery."
    ))
    els.append(sp(8))

    els.append(Paragraph("Sources", H2))
    els.append(tbl(
        ["Meeting", "Date", "Key Speakers", "Relevant Timestamp"],
        [
            ["CGTO PO Alignment",             "2026-06-12", "Nils Hartmann, Loring Wu, Satish Kumar, Jiss", "Throughout"],
            ["ATO to S4 PuC Integration Demo","2026-06-17", "Allen Yuan, Loring Wu, Erwin Sha, Jiss, Nils", "32:09 – 44:00"],
            ["Reauthentication Framework",    "2026-06-18", "Yadesh Gupta, Prabir Kumar Mallick, Swarnava", "Throughout"],
        ],
        widths=[6*cm, 2.5*cm, 6*cm, 3*cm]
    ))
    return els

# ── Build ─────────────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title="GxP Reuse Components Reference",
        author="SAP S/4HANA GxP Team",
    )

    story = []
    story.extend(cover())
    story.extend(components())
    story.extend(open_issues())

    def on_page(c, doc):
        c.saveState()
        c.setFont("Helvetica", 7)
        c.setFillColor(colors.HexColor("#888888"))
        c.drawString(2*cm, 1.2*cm, "GxP / CGTO / ATO / eSignature — Reuse Components Reference Guide")
        c.drawRightString(19.5*cm, 1.2*cm, f"Page {doc.page}")
        c.setStrokeColor(GREY_BORDER)
        c.setLineWidth(0.4)
        c.line(2*cm, 1.5*cm, 19.5*cm, 1.5*cm)
        c.restoreState()

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF created: {OUTPUT}")

build()
