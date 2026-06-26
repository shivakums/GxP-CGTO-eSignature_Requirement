from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUTPUT = r"C:\Users\I308878\GxP-CGTO-eSignature_Requirement\GxP_84P_Scope_Item_Guide.pdf"

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

TITLE     = ms("T",  fontSize=22, textColor=WHITE,   fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=6)
SUBTITLE  = ms("ST", fontSize=11, textColor=colors.HexColor("#AACCFF"), fontName="Helvetica", alignment=TA_CENTER, spaceAfter=3)
META      = ms("M",  fontSize=8,  textColor=colors.HexColor("#AACCFF"), fontName="Helvetica", alignment=TA_CENTER)
H1        = ms("H1", fontSize=13, textColor=WHITE,   fontName="Helvetica-Bold", spaceAfter=3)
H2        = ms("H2", fontSize=11, textColor=SAP_DARK,fontName="Helvetica-Bold", spaceAfter=4, spaceBefore=8)
H3        = ms("H3", fontSize=9,  textColor=SAP_BLUE,fontName="Helvetica-Bold", spaceAfter=3, spaceBefore=5)
BODY      = ms("B",  fontSize=8.5,textColor=BLACK,   leading=13, spaceAfter=3, alignment=TA_JUSTIFY)
BODY_SML  = ms("BS", fontSize=8,  textColor=BLACK,   leading=12, spaceAfter=2)
CODE_S    = ms("CS", fontSize=7.5,textColor=CODE_FG, fontName="Courier", leading=11, spaceAfter=1)
QUOTE_S   = ms("QS", fontSize=8.5,textColor=DARK_GREY,fontName="Helvetica-Oblique", leading=13, leftIndent=10, spaceAfter=3)
TH        = ms("TH", fontSize=8,  textColor=WHITE,   fontName="Helvetica-Bold", alignment=TA_CENTER)
TC        = ms("TC", fontSize=8,  textColor=BLACK,   leading=11)
BADGE_L   = ms("BL", fontSize=28, textColor=WHITE,   fontName="Helvetica-Bold", alignment=TA_CENTER)

def sp(n=6): return Spacer(1, n)

# ── Helpers ───────────────────────────────────────────────────────────────────
def sec_hdr(title, subtitle="", color=SAP_DARK):
    rows = [[Paragraph(title, H1)]]
    if subtitle:
        rows.append([Paragraph(subtitle, ms("sh", fontSize=8,
                    textColor=colors.HexColor("#AACCFF"),
                    fontName="Helvetica-Oblique"))])
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

def warn_box(text): return info_box(text, bg=RED_LIGHT,    border=RED)
def ok_box(text):   return info_box(text, bg=GREEN_LIGHT,  border=GREEN_OK)
def note_box(text): return info_box(text, bg=GOLD_LIGHT,   border=GOLD)

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

def layer_card(title, color, items):
    """Coloured layer card with bullet items"""
    hdr = Table([[Paragraph(title, ms(f"lh{title[:3]}", fontSize=9, textColor=WHITE,
                 fontName="Helvetica-Bold"))]],
                colWidths=[17.5*cm])
    hdr.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), color),
        ("TOPPADDING",   (0,0),(-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("LEFTPADDING",  (0,0),(-1,-1), 12),
    ]))
    body_rows = []
    for item in items:
        body_rows.append([Paragraph(f"▸  {item}", BODY_SML)])
    body = Table(body_rows, colWidths=[17.5*cm])
    body.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), colors.HexColor(
            "#E8F4FD" if color==SAP_BLUE else
            "#E6F4EA" if color==BTP_GREEN else
            "#F0EAF8" if color==PURPLE else
            "#E0F5F7")),
        ("TOPPADDING",   (0,0),(-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
        ("LEFTPADDING",  (0,0),(-1,-1), 14),
    ]))
    bot = Table([[""]], colWidths=[17.5*cm], rowHeights=[2])
    bot.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1), color)]))
    return KeepTogether([hdr, body, bot, sp(6)])

def contrib_card(role, name, delivers, color):
    t = Table([[
        Paragraph(role, ms(f"cr{role[:3]}", fontSize=8, textColor=WHITE,
                  fontName="Helvetica-Bold")),
        Paragraph(name, ms(f"cn{role[:3]}", fontSize=8, textColor=WHITE,
                  fontName="Helvetica-Oblique")),
        Paragraph(delivers, BODY_SML),
    ]], colWidths=[3.5*cm, 4*cm, 10*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(1,0),  color),
        ("BACKGROUND",   (2,0),(2,0),  WHITE),
        ("LINEABOVE",    (0,0),(-1,0), 0.5, color),
        ("LINEBELOW",    (0,0),(-1,0), 0.5, GREY_BORDER),
        ("TOPPADDING",   (0,0),(-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("LEFTPADDING",  (0,0),(-1,-1), 8),
        ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
    ]))
    return t

# ══════════════════════════════════════════════════════════════════════════════
# PAGES
# ══════════════════════════════════════════════════════════════════════════════
def cover():
    els = []

    # Big 84P badge + title
    badge = Table([[Paragraph("84P", BADGE_L)]], colWidths=[3.5*cm], rowHeights=[3.5*cm])
    badge.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), SAP_BLUE),
        ("VALIGN",    (0,0),(-1,-1),"MIDDLE"),
    ]))
    title_block = Table([
        [Paragraph("Scope Item 84P", TITLE)],
        [Paragraph("GxP Compliance — Complete Reference Guide", SUBTITLE)],
        [Paragraph("What It Is  |  What It Delivers  |  Who Contributes  |  Timeline", SUBTITLE)],
        [Paragraph("SAP S/4HANA + BTP  |  Reauthentication Framework  |  eSignature  |  2026-06-26", META)],
    ], colWidths=[14*cm])
    title_block.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), SAP_DARK),
        ("TOPPADDING",   (0,0),(-1,-1), 20),
        ("BOTTOMPADDING",(0,0),(-1,-1), 20),
        ("LEFTPADDING",  (0,0),(-1,-1), 16),
    ]))
    top = Table([[badge, title_block]], colWidths=[3.5*cm, 14*cm])
    top.setStyle(TableStyle([
        ("TOPPADDING",   (0,0),(-1,-1),0),
        ("BOTTOMPADDING",(0,0),(-1,-1),0),
        ("LEFTPADDING",  (0,0),(-1,-1),0),
        ("VALIGN",       (0,0),(-1,-1),"MIDDLE"),
    ]))
    els.append(top)
    els.append(sp(14))

    # One-line summary
    els.append(ok_box(
        "84P = The on/off switch for GxP compliance in S4 + BTP. "
        "Activating it brings the Reauthentication Framework, S-table config for registered "
        "business objects, and BTP reason code provisioning — all in one step. "
        "Without 84P activated, CHECK_ESIG_ACTIVE returns FALSE and no reauthentication "
        "dialog will ever appear in any LOB application."
    ))
    els.append(sp(10))

    # Summary table
    els.append(Paragraph("At a Glance", H2))
    els.append(tbl(
        ["Aspect", "Detail"],
        [
            ["Scope Item ID",     "84P"],
            ["Full Name",         "GxP Compliance — Central Scope Item"],
            ["Type",              "Shared — used by ALL LOBs (PO, Process Order, Sales Order, Maintenance Order etc.)"],
            ["Primary Activation","Activates Reauthentication Framework in S4 + provisions BTP eSignature SaaS tenant"],
            ["S4 Delivery",       "S-table content (VC_SRA_SOT) delivered via transport — object registrations, field configs"],
            ["BTP Delivery",      "Reason codes auto-provisioned in BTP tenant on activation — customer can fine-tune"],
            ["CE2608 Status",     "84P scope item created. Framework base delivered. OData V4 API extensibility enabled."],
            ["2702 Status",       "Each LOB adds their object + field registrations inside 84P"],
            ["Customer Action",   "After activation: SPRO fine-tuning of regulated fields + custom reason codes in BTP"],
            ["Key Contact",       "Framework: Yadesh Gupta (ya.gupta@sap.com) | eSignature: Swarnava Chatterjee"],
        ],
        widths=[4.5*cm, 13*cm]
    ))
    els.append(PageBreak())
    return els

# ── Section 1: What 84P Does ──────────────────────────────────────────────────
def section1():
    els = []
    els.append(sec_hdr("Section 1 — What 84P Does: Three Activation Layers",
                       "All three layers activate simultaneously when 84P is switched on", SAP_DARK))
    els.append(sp(10))

    els.append(layer_card(
        "LAYER 1 — S4 Backend (S-table content delivered via transport)",
        SAP_BLUE,
        [
            "Reauthentication Framework activated in S4",
            "VC_SRA_SOT S-table populated with: business object registrations, callback class names, node type definitions, regulated field list per node",
            "SPRO menu for GxP customising becomes available to customer",
            "LOB-specific object registrations delivered as part of 84P transport (each LOB contributes their own entries)",
        ]
    ))

    els.append(layer_card(
        "LAYER 2 — BTP (auto-provisioned on activation)",
        BTP_GREEN,
        [
            "BTP eSignature SaaS tenant provisioned automatically — no manual setup required",
            "Reason codes for all registered business objects loaded into BTP",
            "Customer can fine-tune reason codes in BTP after provisioning completes",
            "Only reason codes configured for a specific object appear in that object's reauthentication dropdown",
        ]
    ))

    els.append(layer_card(
        "LAYER 3 — Communication (pre-wired)",
        PURPLE,
        [
            "Communication Arrangement between S4 and BTP eSignature SaaS configured as part of scope item activation",
            "OAuth / service key exchange between S4 and BTP pre-wired — no separate manual Communication Arrangement needed",
            "CHECK_ESIG_ACTIVE returns TRUE only when BOTH 84P is active AND BTP provisioning is complete",
        ]
    ))

    els.append(sp(4))
    els.append(quote_box(
        "Here we have a standard scope item for every LOB for considering GxP — which is 84P.",
        "Yadesh Gupta, Reauthentication Framework Architect"
    ))
    els.append(sp(6))
    els.append(quote_box(
        "Whenever provisioning activates itself, the content will be loaded in the BTP tenant "
        "automatically — and then customer can fine-tune.",
        "Yadesh Gupta"
    ))
    els.append(PageBreak())
    return els

# ── Section 2: Who Contributes ────────────────────────────────────────────────
def section2():
    els = []
    els.append(sec_hdr("Section 2 — Who Contributes What to 84P",
                       "84P is shared — NOT one scope item per LOB", SAP_BLUE))
    els.append(sp(10))

    els.append(info_box(
        "84P is a SHARED scope item. All LOBs — Purchase Order, Process Order, "
        "Sales Order, Maintenance Order — contribute their object registrations and field "
        "configurations INTO the same 84P. There is no separate 84P-PO or 84P-MM. "
        "One activation covers all LOBs that have registered their objects."
    ))
    els.append(sp(8))

    els.append(Paragraph("Contribution Breakdown", H2))
    els.append(sp(4))

    contribs = [
        ("Framework Team",   "Yadesh Gupta / Prabir Mallick",
         "Delivers: Reauthentication Framework base infrastructure, VC_SRA_SOT table structure, "
         "Framework APIs (REQUEST_REAUTH, VALIDATE_RESULT, CHECK_ESIG_ACTIVE), "
         "BTP eSignature SaaS integration wiring, SPRO customising menu",
         SAP_DARK),
        ("PO LOB Team",      "Nils Hartmann / Jiss",
         "Delivers inside 84P: PURCHASE_ORDER object registration, "
         "Callback class: ZCL_PO_REAUTH_CHECK, "
         "Node: PO_HEADER_EXT → regulated fields (THERAPY_TYPE, CLINICAL_STUDY, PROTOCOL_REF)",
         SAP_BLUE),
        ("Asset Mgmt LOB",   "Niranjan Raju / Ajith",
         "Delivers inside 84P: PROCESS_ORDER / MAINTENANCE_ORDER object registration, "
         "Their callback class + regulated fields (e.g. overall status field)",
         ORANGE),
        ("ATO / CGTO Team",  "Loring Wu / Satish Kumar",
         "Delivers inside 84P: ATO-specific object registration for S4 PO extension, "
         "Regulated ATO fields: THERAPY_TYPE, CLINICAL_STUDY, PROTOCOL_REF, PATIENT_REF",
         BTP_GREEN),
        ("Each Other LOB",   "Respective PO / SO / PP owners",
         "Each LOB contributes their own: object name, callback class, node types, regulated field list. "
         "Customers can fine-tune the field list after activation.",
         PURPLE),
        ("Customer",         "GxP Compliance Admin",
         "After 84P activation: SPRO → fine-tune which fields are regulated (add/remove). "
         "BTP → add custom reason codes or remove SAP-suggested ones.",
         TEAL),
    ]

    for role, name, delivers, color in contribs:
        els.append(contrib_card(role, name, delivers, color))
        els.append(sp(3))

    els.append(sp(6))
    els.append(quote_box(
        "The eSignature framework is built by the central BTP foundation team — it is a service "
        "each LOB has to consume. Which will be available as part of the 2608 release. "
        "So each LOB will be implementing that service in 2702 for their objects.",
        "Sathishkumar Meenakshisundaram, ATO PM"
    ))
    els.append(PageBreak())
    return els

# ── Section 3: What 84P Delivers in Detail ────────────────────────────────────
def section3():
    els = []
    els.append(sec_hdr("Section 3 — What 84P Delivers in Detail",
                       "S-table content, BTP provisioning, and customer fine-tuning", BTP_GREEN))
    els.append(sp(10))

    els.append(Paragraph("3.1  VC_SRA_SOT S-Table Content (S4 Backend)", H2))
    els.append(Paragraph(
        "The S-table VC_SRA_SOT is the configuration backbone of the Reauthentication Framework. "
        "84P delivers pre-populated content into this table so the framework knows which business "
        "objects are registered, which callback classes to call, and which fields are regulated.",
        BODY))
    els.append(sp(4))
    els.append(code_block([
        "VC_SRA_SOT — Reauthentication Object Configuration (S-Table)",
        "═══════════════════════════════════════════════════════════════",
        "",
        "Level 1 — Object Registration (one row per business object):",
        "  Object Name:      PURCHASE_ORDER",
        "  Reauth Class:     ZCL_PO_REAUTH_CHECK   ← LOB implements this",
        "  Auth Class:       ZCL_PO_AUTH_CHECK      ← LOB implements this",
        "",
        "Level 2 — Node Types per Object:",
        "  Object: PURCHASE_ORDER",
        "    Node: PO_HEADER_EXT  → Table: /ATO/S4_PO_HEADER_EXT",
        "    Node: PO_ITEM_EXT   → Table: /ATO/S4_PO_ITEM_EXT",
        "",
        "Level 3 — Regulated Fields per Node:",
        "  PO_HEADER_EXT:",
        "    THERAPY_TYPE    ← triggers reauthentication if changed",
        "    CLINICAL_STUDY  ← triggers reauthentication if changed",
        "    PROTOCOL_REF    ← triggers reauthentication if changed",
        "  PO_ITEM_EXT:",
        "    THERAPY_TYPE",
        "    PATIENT_REF",
        "",
        "Customer fine-tune (after 84P activation via SPRO):",
        "  → Remove a field that is not regulated in their context",
        "  → Add a custom field that needs reauthentication",
    ]))

    els.append(sp(8))
    els.append(Paragraph("3.2  BTP Reason Codes (Auto-Provisioned)", H2))
    els.append(Paragraph(
        "When 84P activates, reason codes for each registered business object are automatically "
        "loaded into the BTP eSignature SaaS tenant. The dropdown in the reauthentication dialog "
        "only shows reason codes configured for that specific business object.",
        BODY))
    els.append(sp(4))
    els.append(tbl(
        ["Business Object", "SAP-Suggested Reason Codes (Delivered via 84P)", "Customer Can"],
        [
            ["PURCHASE_ORDER",
             "Clinical Protocol Update  |  Regulatory Submission  |  Error Correction  |  Therapy Type Reassignment",
             "Add custom codes or remove unused ones"],
            ["PROCESS_ORDER",
             "Manufacturing Change  |  Quality Deviation  |  Process Update",
             "Add custom codes specific to their manufacturing process"],
            ["MAINTENANCE_ORDER",
             "Safety Critical Change  |  Maintenance Plan Update  |  Status Release",
             "Add custom codes for their maintenance scenarios"],
        ],
        widths=[3.5*cm, 9*cm, 5*cm]
    ))
    els.append(sp(8))

    els.append(Paragraph("3.3  CHECK_ESIG_ACTIVE — When Does It Return TRUE?", H2))
    els.append(code_block([
        "CHECK_ESIG_ACTIVE returns TRUE only when ALL conditions are met:",
        "",
        "Condition 1: Scope item 84P is activated in S4",
        "  → S-table VC_SRA_SOT has content",
        "  → SPRO GxP menu is available",
        "",
        "Condition 2: BTP eSignature SaaS provisioning is complete",
        "  → Communication Arrangement between S4 and BTP is configured",
        "  → BTP tenant is reachable",
        "",
        "IF condition 1 = TRUE AND condition 2 = TRUE",
        "  → CHECK_ESIG_ACTIVE = ABAP_TRUE  → reauthentication flows proceed",
        "",
        "IF either condition = FALSE",
        "  → CHECK_ESIG_ACTIVE = ABAP_FALSE → all reauthentication SKIPPED",
        "  → No dialog, no signature, no audit trail",
        "",
        "Current state (pre-2702):  CHECK_ESIG_ACTIVE = FALSE (expected)",
        "Target state (post-2702):  CHECK_ESIG_ACTIVE = TRUE",
    ]))
    els.append(PageBreak())
    return els

# ── Section 4: What 84P Does NOT Cover ───────────────────────────────────────
def section4():
    els = []
    els.append(sec_hdr("Section 4 — What 84P Does NOT Cover",
                       "Boundaries of the scope item — what LOB teams must build themselves", RED))
    els.append(sp(10))

    els.append(tbl(
        ["NOT in 84P Scope", "Reason", "Who Owns It"],
        [
            ["Relevancy Check callback class (ZCL_PO_REAUTH_CHECK)",
             "Application-specific logic — framework cannot build it generically",
             "Each LOB application team"],
            ["Authorization callback class (ZCL_PO_AUTH_CHECK)",
             "Application-specific — depends on which users can perform which actions",
             "Each LOB application team"],
            ["eSignature trigger in ME21N save flow",
             "LOB app integration point — each app adds REQUEST_REAUTH at their save hook",
             "PO standard team (Nils/Jiss) for ME21N"],
            ["Field value-level triggering (only trigger when field changes A→B)",
             "Not yet in framework — roadmap item post-2702",
             "Framework team — future release"],
            ["eSignature for background jobs / system users",
             "Explicitly excluded — GxP rule: automated system-context jobs do not require signature",
             "N/A — excluded by design"],
            ["Customer-specific reason codes",
             "Customer adds their own after 84P activation",
             "Customer GxP admin"],
            ["Change Document registration for ATO extension fields",
             "ATO team must extend EINKBELEG — separate from 84P",
             "ATO team (Allen Yuan / Loring Wu)"],
            ["eSignature in Manage PO App (BOF/Fiori)",
             "Deferred — pending app modernisation",
             "Post-2702 delivery"],
        ],
        widths=[5*cm, 7.5*cm, 5*cm]
    ))
    els.append(sp(8))

    els.append(warn_box(
        "⚠  The most common misunderstanding: teams think activating 84P automatically "
        "makes their application GxP-compliant. It does NOT. 84P activates the FRAMEWORK. "
        "Each LOB must still: (1) implement the Relevancy Check callback class, "
        "(2) register REQUEST_REAUTH in their save flow, "
        "(3) call VALIDATE_RESULT after signature capture. "
        "Without these steps, reauthentication never fires even with 84P active."
    ))
    els.append(PageBreak())
    return els

# ── Section 5: Delivery Timeline ─────────────────────────────────────────────
def section5():
    els = []
    els.append(sec_hdr("Section 5 — 84P Delivery Timeline",
                       "What was delivered when and what is still planned", SAP_DARK))
    els.append(sp(10))

    els.append(tbl(
        ["Release", "84P Deliverable", "Status", "Details"],
        [
            ["CE2608",
             "84P scope item created — framework base",
             "✅ Done",
             "Framework infrastructure, VC_SRA_SOT structure, OData V4 API extensibility enabled for PO"],
            ["CE2608",
             "Change Document for PO verified",
             "✅ Done",
             "CDHDR/CDPOS working for all standard PO fields — prerequisite for eSignature met"],
            ["2702",
             "PO LOB: PURCHASE_ORDER object registration in 84P",
             "🔲 Planned",
             "ZCL_PO_REAUTH_CHECK + regulated fields THERAPY_TYPE, CLINICAL_STUDY, PROTOCOL_REF"],
            ["2702",
             "ME21N save flow integration — REQUEST_REAUTH call",
             "🔲 Planned",
             "eSignature trigger point added into ME21N save processing"],
            ["2702",
             "BTP reason codes for PURCHASE_ORDER auto-provisioned",
             "🔲 Planned",
             "Clinical Protocol Update, Regulatory Submission etc. loaded in BTP on 84P activation"],
            ["2702",
             "Each LOB adds their object registrations inside 84P",
             "🔲 Planned",
             "Process Order (Niranjan/Ajith), Maintenance Order, Sales Order teams all contribute"],
            ["Post-2702",
             "eSignature in modernised Manage PO App (BOF replacement)",
             "⏳ Deferred",
             "Pending app modernisation — ME21N is the interim target"],
            ["Post-2702",
             "Field value-level triggering (A→B specific transition)",
             "⏳ Roadmap",
             "Currently: any value change triggers reauth. Specific value transition: future"],
        ],
        widths=[2.5*cm, 5.5*cm, 2.5*cm, 7*cm]
    ))
    els.append(sp(8))

    # Visual timeline
    els.append(Paragraph("Timeline Visual", H2))
    els.append(code_block([
        "CE2608 (2026)                    2702 (2027)                Post-2702",
        "════════════════════════════════════════════════════════════════════════►",
        "",
        "84P scope item          Each LOB adds           eSign in modernised",
        "created                 object registrations    PO App (deferred)",
        "                        to 84P                  ",
        "Framework base    ──►   REQUEST_REAUTH   ──►    Value-level trigger",
        "delivered               in ME21N save            (roadmap)",
        "                        flow",
        "Change Doc for          BTP reason codes",
        "PO verified ✓           provisioned",
        "                                                             ",
        "CHECK_ESIG_ACTIVE       CHECK_ESIG_ACTIVE",
        "= FALSE (expected)      = TRUE (target)",
    ]))
    els.append(PageBreak())
    return els

# ── Section 6: LOB Integration Checklist ─────────────────────────────────────
def section6():
    els = []
    els.append(sec_hdr("Section 6 — LOB Integration Checklist",
                       "What every LOB team must deliver to integrate with 84P", PURPLE))
    els.append(sp(10))

    els.append(Paragraph("6.1  What Each LOB Must Deliver Inside 84P (Transport)", H2))
    els.append(tbl(
        ["#", "Deliverable", "Type", "Example for PO"],
        [
            ["1", "Reauthentication object name registered in VC_SRA_SOT",
             "S-table content via transport", "PURCHASE_ORDER"],
            ["2", "Relevancy Check callback class",
             "ABAP class", "ZCL_PO_REAUTH_CHECK"],
            ["3", "Authorization class",
             "ABAP class", "ZCL_PO_AUTH_CHECK"],
            ["4", "Node types defined per object",
             "S-table content", "PO_HEADER_EXT → /ATO/S4_PO_HEADER_EXT"],
            ["5", "Regulated field list per node",
             "S-table content", "THERAPY_TYPE, CLINICAL_STUDY, PROTOCOL_REF"],
            ["6", "BTP reason codes defined for the object",
             "BTP content delivery", "Clinical Protocol Update, Regulatory Submission"],
        ],
        widths=[0.8*cm, 6.5*cm, 4.5*cm, 5.7*cm]
    ))
    els.append(sp(8))

    els.append(Paragraph("6.2  What Each LOB Must Build in Their Application Code", H2))
    els.append(tbl(
        ["#", "Code to Write", "Where", "Notes"],
        [
            ["1", "Call CHECK_ESIG_ACTIVE before any signature flow",
             "Application save method", "Skip gracefully if FALSE"],
            ["2", "Call REQUEST_REAUTH at the regulated save trigger",
             "ME21N / LOB app save hook", "Use HCP GUI variant for Web GUI apps"],
            ["3", "Call VALIDATE_RESULT after dialog closes",
             "After REQUEST_REAUTH returns", "Confirms signature was captured"],
            ["4", "Implement Relevancy Check callback class logic",
             "ZCL_PO_REAUTH_CHECK", "Returns ABAP_TRUE/FALSE based on field changes"],
            ["5", "Implement Authorization class logic",
             "ZCL_PO_AUTH_CHECK", "Role-based check for the specific transaction"],
        ],
        widths=[0.8*cm, 5.5*cm, 4.5*cm, 6.7*cm]
    ))
    els.append(sp(8))

    els.append(Paragraph("6.3  How CHECK_ESIG_ACTIVE Fits into Application Code", H2))
    els.append(code_block([
        "\" Application save method (ME21N integration point — 2702)",
        "METHOD on_po_save.",
        "",
        "  \" Step 1: Check if GxP is active in this system",
        "  DATA lv_active TYPE abap_bool.",
        "  \" Call CHECK_ESIG_ACTIVE framework API",
        "  IF lv_active = abap_false.",
        "    \" 84P not activated or BTP not provisioned — skip all reauth",
        "    RETURN.",
        "  ENDIF.",
        "",
        "  \" Step 2: Check if any regulated field changed (Relevancy Check)",
        "  DATA lv_relevant TYPE abap_bool.",
        "  \" lv_relevant = result of ZCL_PO_REAUTH_CHECK callback",
        "  IF lv_relevant = abap_false.",
        "    RETURN.  \" No regulated field changed — no signature needed",
        "  ENDIF.",
        "",
        "  \" Step 3: Request reauthentication — LUW paused",
        "  \" Call REQUEST_REAUTH (HCP GUI variant for ME21N)",
        "",
        "  \" Step 4: Validate signature was captured",
        "  \" Call VALIDATE_RESULT",
        "",
        "  \" Step 5: COMMIT WORK — all changes committed with signature linked",
        "",
        "ENDMETHOD.",
    ]))
    els.append(PageBreak())
    return els

# ── Section 7: Sources ────────────────────────────────────────────────────────
def section7():
    els = []
    els.append(sec_hdr("Section 7 — Sources & Key Contacts",
                       "All information sourced from meeting transcripts and GxP Handover slides", TEAL))
    els.append(sp(10))

    els.append(Paragraph("7.1  Source Documents", H2))
    els.append(tbl(
        ["Document", "Date", "Key Content on 84P"],
        [
            ["GxP Handover — Lift & Shift team (pptx + vtt)",
             "2026-06-02",
             "Slides 8-10: eSignature overview, CGTO enablement, CE2608 API deliverable, scope item reference"],
            ["Reauthentication Framework meeting (transcript)",
             "2026-06-18",
             "Yadesh Gupta explains VC_SRA_SOT config, reason code delivery, S-table levels, 84P delivery model"],
            ["CGTO PO Alignment meeting (transcript)",
             "2026-06-12",
             "Satish Kumar confirms 84P as central scope item, each LOB implements in 2702"],
            ["GxP Mandatory Training (transcript)",
             "2022-02-14",
             "Background context on why GxP framework is needed — patient safety, data integrity"],
        ],
        widths=[6.5*cm, 2.5*cm, 8.5*cm]
    ))
    els.append(sp(8))

    els.append(Paragraph("7.2  Key Contacts for 84P", H2))
    els.append(tbl(
        ["Name", "Role", "Topic", "Email"],
        [
            ["Yadesh Gupta",        "Reauthentication Framework Architect", "VC_SRA_SOT config, APIs, 84P framework base", "ya.gupta@sap.com"],
            ["Prabir Kumar Mallick","Reauthentication Framework Dev Lead",  "Technical 84P implementation",                "—"],
            ["Swarnava Chatterjee", "eSignature Lead",                      "BTP eSignature SaaS, reason codes, BTP side", "swarnava.chatterjee@sap.com"],
            ["Karthikeyan K.A.L",  "eSignature team",                      "eSignature integration",                      "karthikeyan.k.a.l@sap.com"],
            ["Nils Hartmann",       "PO Product Owner",                     "PO LOB contribution to 84P",                  "—"],
            ["Satish Kumar",        "ATO/CGTO PM + Architecture",           "ATO object registration in 84P",              "—"],
        ],
        widths=[4*cm, 4.5*cm, 5.5*cm, 3.5*cm]
    ))
    els.append(sp(8))

    els.append(note_box(
        "Wiki Reference: GxP enablement details available at:\n"
        "https://wiki.one.int.sap/wiki/spaces/S4HPROC011/pages/5681941152/GxP+enablement\n"
        "(Mentioned in GxP Handover Slide 8)"
    ))
    return els

# ── Build ─────────────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title="Scope Item 84P — GxP Compliance Reference Guide",
        author="SAP GxP Team",
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

    def on_page(c, doc):
        c.saveState()
        c.setFont("Helvetica", 7)
        c.setFillColor(colors.HexColor("#888888"))
        c.drawString(2*cm, 1.2*cm, "Scope Item 84P — GxP Compliance: What It Is | What It Delivers | Who Contributes | Timeline")
        c.drawRightString(19.5*cm, 1.2*cm, f"Page {doc.page}")
        c.setStrokeColor(colors.HexColor("#CCCCCC"))
        c.setLineWidth(0.4)
        c.line(2*cm, 1.5*cm, 19.5*cm, 1.5*cm)
        c.restoreState()

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF created: {OUTPUT}")

build()
