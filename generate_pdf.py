from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus.flowables import Flowable

OUTPUT = r"C:\Users\I308878\GxP-CGTO-eSignature_Requirement\GxP_CGTO_ATO_eSignature_Complete_Guide.pdf"

# ── Colours ──────────────────────────────────────────────────────────────────
SAP_BLUE       = colors.HexColor("#0070F2")
SAP_DARK       = colors.HexColor("#003366")
SAP_LIGHT      = colors.HexColor("#E8F4FD")
SAP_GOLD       = colors.HexColor("#F0AB00")
SAP_GREEN      = colors.HexColor("#188918")
SAP_RED        = colors.HexColor("#BB0000")
GREY_BG        = colors.HexColor("#F5F5F5")
GREY_BORDER    = colors.HexColor("#CCCCCC")
CODE_BG        = colors.HexColor("#1E1E2E")
CODE_FG        = colors.HexColor("#CDD6F4")
WHITE          = colors.white
BLACK          = colors.black

# ── Styles ───────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def make_style(name, parent="Normal", **kwargs):
    return ParagraphStyle(name=name, parent=styles[parent], **kwargs)

TITLE      = make_style("DocTitle",    fontSize=24, textColor=WHITE,      alignment=TA_CENTER, spaceAfter=4, fontName="Helvetica-Bold")
SUBTITLE   = make_style("DocSub",      fontSize=13, textColor=SAP_LIGHT,   alignment=TA_CENTER, spaceAfter=2, fontName="Helvetica")
META       = make_style("Meta",        fontSize=9,  textColor=SAP_LIGHT,   alignment=TA_CENTER, spaceAfter=0, fontName="Helvetica")
H1         = make_style("H1",          fontSize=16, textColor=WHITE,       spaceAfter=6, spaceBefore=4, fontName="Helvetica-Bold")
H2         = make_style("H2",          fontSize=12, textColor=SAP_DARK,    spaceAfter=4, spaceBefore=10, fontName="Helvetica-Bold", borderPad=4)
H3         = make_style("H3",          fontSize=10, textColor=SAP_BLUE,    spaceAfter=3, spaceBefore=6, fontName="Helvetica-Bold")
BODY       = make_style("Body",        fontSize=9,  textColor=BLACK,       spaceAfter=4, spaceBefore=2, leading=14, alignment=TA_JUSTIFY)
BODY_SMALL = make_style("BodySmall",   fontSize=8,  textColor=BLACK,       spaceAfter=2, leading=12)
CODE       = make_style("Code",        fontSize=7.5,textColor=CODE_FG,     fontName="Courier", leading=11, spaceAfter=2, spaceBefore=2)
NOTE       = make_style("Note",        fontSize=8,  textColor=colors.HexColor("#555555"), leading=12, leftIndent=10, spaceAfter=3)
BULLET     = make_style("Bullet",      fontSize=9,  textColor=BLACK,       leading=13, leftIndent=12, spaceAfter=2)
TABLE_HDR  = make_style("TblHdr",      fontSize=8,  textColor=WHITE,       fontName="Helvetica-Bold", alignment=TA_CENTER)
TABLE_CELL = make_style("TblCell",     fontSize=8,  textColor=BLACK,       leading=11)
TABLE_CELL_C=make_style("TblCellC",    fontSize=8,  textColor=BLACK,       leading=11, alignment=TA_CENTER)

# ── Helper flowables ──────────────────────────────────────────────────────────
def hline(color=SAP_BLUE, thickness=1):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=4, spaceBefore=4)

def section_header(title, color=SAP_DARK):
    data = [[Paragraph(title, H1)]]
    t = Table(data, colWidths=[17.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), color),
        ("TOPPADDING",  (0,0), (-1,-1), 8),
        ("BOTTOMPADDING",(0,0),(-1,-1), 8),
        ("LEFTPADDING", (0,0), (-1,-1), 12),
        ("ROUNDEDCORNERS", [4,4,4,4]),
    ]))
    return t

def code_block(text):
    lines = text.strip().split("\n")
    paras = [Paragraph(l.replace(" ","&nbsp;").replace("<","&lt;").replace(">","&gt;") or "&nbsp;", CODE) for l in lines]
    t = Table([[p] for p in paras], colWidths=[17.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), CODE_BG),
        ("TOPPADDING",  (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
        ("RIGHTPADDING",(0,0), (-1,-1), 6),
        ("ROUNDEDCORNERS",[4,4,4,4]),
    ]))
    return t

def info_box(text, color=SAP_LIGHT, border=SAP_BLUE):
    t = Table([[Paragraph(text, BODY_SMALL)]], colWidths=[17.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), color),
        ("LINEABOVE",    (0,0),(-1,0),  1.5, border),
        ("TOPPADDING",   (0,0),(-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("LEFTPADDING",  (0,0),(-1,-1), 10),
    ]))
    return t

def simple_table(headers, rows, col_widths=None):
    n = len(headers)
    if not col_widths:
        col_widths = [17.5*cm/n]*n
    data = [[Paragraph(h, TABLE_HDR) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), TABLE_CELL) for c in row])
    t = Table(data, colWidths=col_widths)
    style = [
        ("BACKGROUND",    (0,0), (-1,0),  SAP_BLUE),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, GREY_BG]),
        ("GRID",          (0,0), (-1,-1), 0.4, GREY_BORDER),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ]
    t.setStyle(TableStyle(style))
    return t

def sp(n=6): return Spacer(1, n)

# ── Cover page ────────────────────────────────────────────────────────────────
def cover_page():
    els = []
    # header band
    cover_data = [[
        Paragraph("GxP Compliance &amp; CGTO/ATO Integration", TITLE),
        Paragraph("eSignature &amp; Reauthentication Framework", SUBTITLE),
        Paragraph("Complete Technical &amp; Process Guide", SUBTITLE),
        Paragraph("SAP S/4HANA | BTP | Life Science | 21 CFR Part 11 / EU Annex 11", META),
        Paragraph("Date: 2026-06-24 &nbsp;&nbsp;|&nbsp;&nbsp; Version: 1.0 &nbsp;&nbsp;|&nbsp;&nbsp; Status: Draft", META),
    ]]
    ct = Table(cover_data, colWidths=[17.5*cm])
    ct.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), SAP_DARK),
        ("TOPPADDING",    (0,0),(-1,-1), 30),
        ("BOTTOMPADDING", (0,0),(-1,-1), 30),
        ("LEFTPADDING",   (0,0),(-1,-1), 20),
        ("RIGHTPADDING",  (0,0),(-1,-1), 20),
    ]))
    els.append(ct)
    els.append(sp(16))

    # scope box
    scope_rows = [
        ["Topic", "Scope", "Target Release"],
        ["GxP Compliance", "Regulatory framework — 21 CFR Part 11 / EU Annex 11", "Ongoing"],
        ["CGTO / ATO Fields", "Industry Object Extension on PO (Therapy, Study, Protocol, Patient)", "2702"],
        ["Change Document", "Field-level audit trail for PO (CDHDR/CDPOS)", "Done 2608 ✓"],
        ["eSignature", "Electronic signature on regulated PO changes via BTP SaaS", "2702"],
        ["Reauthentication", "Platform-level reusable framework — LOB callback integration", "2702"],
    ]
    els.append(Paragraph("Document Scope", H2))
    els.append(simple_table(
        scope_rows[0], scope_rows[1:],
        col_widths=[4*cm, 9*cm, 4.5*cm]
    ))
    els.append(sp(16))

    # contacts
    els.append(Paragraph("Key Contacts", H2))
    contact_rows = [
        ["Name", "Role", "Work Stream"],
        ["Swarnava Chatterjee", "eSignature Integration Lead", "WS1 — eSignature"],
        ["Yadesh Gupta", "Reauthentication Framework Architect", "WS1 — Reauth"],
        ["Prabir Kumar Mallick", "Reauth Framework Dev Lead", "WS1 — Reauth"],
        ["Satish Kumar (Meenakshisundaram)", "ATO/CGTO PM + Architecture", "WS3 — ATO/CGTO"],
        ["Viswanath Natesan", "ATO Architecture", "WS3 — ATO/CGTO"],
        ["Loring Wu", "ATO Development Manager", "WS3 — ATO/CGTO"],
        ["Nils Hartmann", "Purchase Order Product Owner", "Both"],
        ["Felix Vente", "Suite Architecture — North Star Governance", "Governance"],
    ]
    els.append(simple_table(contact_rows[0], contact_rows[1:], col_widths=[5.5*cm, 7.5*cm, 4.5*cm]))
    els.append(PageBreak())
    return els

# ── Section 1: Relationship overview ─────────────────────────────────────────
def section1():
    els = []
    els.append(section_header("Section 1 — How GxP, ATO/CGTO, eSignature & Reauthentication Relate"))
    els.append(sp(10))

    els.append(Paragraph("1.1  The Four Pillars — One Compliance Goal", H2))
    els.append(Paragraph(
        "GxP compliance for Purchase Order in SAP S/4HANA is delivered through four interconnected "
        "layers. Each layer depends on the one below it. Removing any layer breaks the compliance chain.",
        BODY))

    els.append(code_block(
"""╔══════════════════════════════════════════════════════════════════════╗
║  GxP (Regulatory Framework)                                         ║
║  WHY — Life Science companies must prove what changed, who           ║
║  approved it, and that the person intentionally authorised it        ║
║                                                                      ║
║  ┌──────────────────────────────────────────────────────────────┐   ║
║  │  ATO / CGTO  (What fields need protecting)                   │   ║
║  │  WHAT — Adds regulated fields to PO via Industry Object      │   ║
║  │  Extension: Therapy Type, Clinical Study, Protocol, Patient  │   ║
║  │                                                              │   ║
║  │  ┌────────────────────────────────────────────────────────┐  │   ║
║  │  │  Change Document  (The audit record)                   │  │   ║
║  │  │  RECORD — CDHDR/CDPOS: who, when, field,               │  │   ║
║  │  │  old value, new value — verified 2608 ✓                │  │   ║
║  │  │                                                        │  │   ║
║  │  │  ┌──────────────────────────────────────────────────┐  │  │   ║
║  │  │  │  Reauthentication + eSignature  (The proof)      │  │  │   ║
║  │  │  │  PROOF — Re-entered credentials + reason code    │  │  │   ║
║  │  │  │  Signature ID linked to CHANGENR                 │  │  │   ║
║  │  │  │  = Intentional act proven — 21 CFR Part 11 ✓     │  │  │   ║
║  │  │  └──────────────────────────────────────────────────┘  │  │   ║
║  │  └────────────────────────────────────────────────────────┘  │   ║
║  └──────────────────────────────────────────────────────────────┘   ║
╚══════════════════════════════════════════════════════════════════════╝"""))

    els.append(sp(8))
    els.append(Paragraph("1.2  Dependency Chain", H2))
    els.append(simple_table(
        ["Layer", "Delivers", "Depends On", "Status"],
        [
            ["GxP Regulatory", "The obligation to comply", "—", "Ongoing"],
            ["ATO/CGTO Fields", "Regulated fields on PO (Therapy, Study etc.)", "Life Science Add-on installed", "Dev started 2026"],
            ["Change Document", "Field-level audit trail CDHDR/CDPOS", "Standard S4 framework", "Done 2608 ✓"],
            ["Reauthentication / eSignature", "Proof of intentional approval linked to change doc", "Change Document must work first", "Planned 2702"],
        ],
        col_widths=[4.5*cm, 6*cm, 4.5*cm, 2.5*cm]
    ))
    els.append(sp(8))

    els.append(Paragraph("1.3  What eSignature Actually Captures", H2))
    els.append(info_box(
        "⚠  Common Misconception: eSignature is NOT a handwritten signature image or PDF certificate. "
        "It is NOT simply recording who was logged in. It is cryptographic proof that the user "
        "RE-ENTERED their credentials at the exact moment of the specific change and accepted "
        "responsibility for it with a reason code. This distinction is what 21 CFR Part 11 requires."
    ))
    els.append(sp(4))
    els.append(simple_table(
        ["Aspect", "Normal Audit Log", "GxP eSignature"],
        [
            ["What is recorded", "User ID + timestamp of save", "User ID + timestamp + re-entered credential hash + reason code"],
            ["Proof of intent", "None — user may have walked away", "Yes — user actively re-authenticated at that moment"],
            ["Stored where", "S4 change document (CDHDR)", "BTP eSignature SaaS (linked to CHANGENR)"],
            ["21 CFR Part 11", "Partial — audit trail only", "Full compliance — signature + audit trail"],
            ["Reason code", "Not captured", "Mandatory — e.g. Clinical Protocol Update"],
        ],
        col_widths=[4*cm, 6*cm, 7.5*cm]
    ))
    els.append(PageBreak())
    return els

# ── Section 2: Extension tables ───────────────────────────────────────────────
def section2():
    els = []
    els.append(section_header("Section 2 — ATO Extension Tables in S4", SAP_BLUE))
    els.append(sp(10))

    els.append(Paragraph("2.1  How the Tables Are Delivered", H2))
    els.append(Paragraph(
        "The ATO extension tables are NOT created manually by the LOB team or customer. "
        "They are delivered as part of the Life Science Add-on installation by SAP Cloud Operations. "
        "Once installed, the tables exist in S4 and the PurchaseOrder OData API is automatically "
        "extended to expose these fields.", BODY))

    els.append(code_block(
"""Life Science Add-on Installation delivers:

  /ATO/S4_PO_HEADER_EXT  (Extension on EKKO — PO Header)
  ┌──────────────────────────────────────────────────┐
  │  Key:  EBELN  CHAR 10  (→ EKKO.EBELN, FK)        │
  │        MANDT  CLNT  3                            │
  │  Fields:                                         │
  │  THERAPY_TYPE     CHAR 20  Therapy classification│
  │  CLINICAL_STUDY   CHAR 40  Clinical study ref    │
  │  PROTOCOL_REF     CHAR 40  Protocol reference    │
  └──────────────────────────────────────────────────┘

  /ATO/S4_PO_ITEM_EXT  (Extension on EKPO — PO Item)
  ┌──────────────────────────────────────────────────┐
  │  Key:  EBELN  CHAR 10  (→ EKPO.EBELN)            │
  │        EBELP  NUMC  5  (→ EKPO.EBELP, FK)        │
  │        MANDT  CLNT  3                            │
  │  Fields:                                         │
  │  THERAPY_TYPE     CHAR 20  Per-item therapy type │
  │  PATIENT_REF      CHAR 40  Patient ID (autolog.) │
  └──────────────────────────────────────────────────┘

  Also delivered:
  ✓ Industry Object Extension node registration on EKKO/EKPO
  ✓ PurchaseOrder OData API extended — TherapyType, ClinicalStudy etc.
  ✓ Change Document registration for ATO extension fields
  ✓ Reauthentication S-table entries (via 84P scope item transport)"""))

    els.append(sp(8))
    els.append(Paragraph("2.2  Why NOT Append Directly to EKKO/EKPO", H2))
    els.append(simple_table(
        ["Approach", "Status", "Reason"],
        [
            ["Append ZZTHERAPY directly to EKKO", "❌ Rejected", "Pollutes standard table, blocked by North Star governance"],
            ["Industry Object Extension node", "✅ Approved", "Clean separation, approved by Suite Architecture (Felix Vente)"],
        ],
        col_widths=[5.5*cm, 3*cm, 9*cm]
    ))
    els.append(sp(8))
    els.append(Paragraph("2.3  Where ATO Field Changes Are Stored", H2))
    els.append(simple_table(
        ["Storage Location", "What It Holds", "Purpose"],
        [
            ["/ATO/S4_PO_HEADER_EXT\n/ATO/S4_PO_ITEM_EXT", "Current live values only (like EKKO)", "Latest state — what the PO contains now"],
            ["CDHDR (Change Doc Header)", "OBJECTCLAS, OBJECTID, CHANGENR, USERNAME, UDATE, UTIME", "Who changed what PO and when"],
            ["CDPOS (Change Doc Item)", "TABNAME=/ATO/S4_PO_HEADER_EXT, FNAME, VALUE_OLD, VALUE_NEW", "Field-level history — old and new values per change"],
            ["BTP eSignature SaaS", "Signature ID, User, Timestamp, Reason Code, Credential hash", "Proof of intentional authorisation — linked to CHANGENR"],
        ],
        col_widths=[4.5*cm, 6.5*cm, 6.5*cm]
    ))
    els.append(PageBreak())
    return els

# ── Section 3: eSignature integration ────────────────────────────────────────
def section3():
    els = []
    els.append(section_header("Section 3 — eSignature Integration: When and How It Is Initiated", SAP_GREEN))
    els.append(sp(10))

    els.append(Paragraph("3.1  Exact Trigger Point Inside ME21N Save", H2))
    els.append(Paragraph(
        "The eSignature trigger point is inside ME21N save processing — AFTER EKKO/EKPO are written "
        "but BEFORE the Logical Unit of Work (LUW) is committed to the database. "
        "If reauthentication fails or the user cancels, the entire save is rolled back.", BODY))

    els.append(code_block(
"""ME21N SAVE PROCESSING — TECHNICAL SEQUENCE
══════════════════════════════════════════════════════════════════

PHASE 1 — Standard PO Processing (existing, unchanged)
─────────────────────────────────────────────────────────
  User clicks SAVE in ME21N
        │
        ▼
  BAPI_PO_CREATE1 / ME_PROCESS_PO_CUST called internally
        │
        ▼
  EKKO written                  (PO Header — standard)
  EKPO written                  (PO Line Items — standard)
  /ATO/S4_PO_HEADER_EXT written (ATO therapy/study/protocol)
  /ATO/S4_PO_ITEM_EXT written   (ATO therapy/patient ref)
        │
        ▼
  Change Document Framework fires (CHANGEDOCUMENT_CLOSE)
  → CDHDR row created: USERNAME, UDATE, UTIME, OBJECTID
  → CDPOS rows created: one per changed field with VALUE_OLD/VALUE_NEW
     Includes /ATO/S4_PO_HEADER_EXT fields if registered

PHASE 2 — Reauthentication Check (NEW — added in 2702)
─────────────────────────────────────────────────────────
        │
        ▼  ◄── INTEGRATION POINT
  Framework calls Relevancy Check callback: ZCL_PO_REAUTH
        │
        ├── ABAP_FALSE: no regulated field changed
        │    → Skip reauthentication, LUW commits normally
        │
        └── ABAP_TRUE: regulated field changed (e.g. THERAPY_TYPE)
              → LUW PAUSED — database NOT committed yet

PHASE 3 — BTP Reauthentication Dialog (NEW — 2702)
─────────────────────────────────────────────────────────
              │
              ▼
        S4 calls BTP eSignature SaaS (REQUEST_REAUTH API)
              │
              ▼
        Dialog shown to user in ME21N:
          ┌──────────────────────────────────────────┐
          │  GxP Reauthentication Required           │
          │  You are changing a regulated field      │
          │  Password:    [__________]               │
          │  Reason Code: [Clinical Protocol Update▼]│
          │  [Confirm]          [Cancel]             │
          └──────────────────────────────────────────┘
              │
              ├── User CANCELS → Save ABORTED → ROLLBACK
              │
              └── User CONFIRMS credentials
                    │
                    ▼
              BTP validates password (must re-enter —
              existing session token is NOT sufficient)
                    │
                    ▼
              BTP creates Signature Record:
                SIG-ID, User, Timestamp, Reason, Credential
              S4 calls VALIDATE_RESULT API
              Signature ID linked to CHANGENR in CDHDR

PHASE 4 — LUW Commit
─────────────────────────────────────────────────────────
              │
              ▼
        COMMIT WORK — atomic:
          EKKO / EKPO / ATO extension tables committed
          CDHDR / CDPOS committed
          Signature ID ↔ CHANGENR link committed

        Outbound event published to Event Mesh
          → ATO SaaS notified of PO change in real-time"""))

    els.append(sp(8))
    els.append(Paragraph("3.2  The 4 APIs Applications Must Call", H2))
    els.append(simple_table(
        ["API", "When to Call", "Technology Constraint"],
        [
            ["REQUEST_REAUTH (OData variant)", "Trigger reauthentication dialog", "OData / HCP GUI only"],
            ["REQUEST_REAUTH (library variant)", "Trigger reauthentication dialog", "All other technologies"],
            ["VALIDATE_RESULT", "Confirm signature was captured successfully", "Any technology"],
            ["CHECK_ESIG_ACTIVE", "Check if GxP/eSignature is active — returns true/false", "Any technology — call before any signature flow"],
        ],
        col_widths=[5.5*cm, 7*cm, 5*cm]
    ))
    els.append(sp(8))
    els.append(Paragraph("3.3  Communication Arrangement Setup", H2))
    els.append(info_box(
        "A Communication Arrangement must be configured in S4 pointing to the BTP eSignature SaaS tenant. "
        "Pattern follows SAP_COM_0267 for other BTP integrations. Requires OAuth / service key exchange "
        "between S4 and BTP. This is a one-time setup by the Basis/admin team before any eSignature flow can work."
    ))
    els.append(PageBreak())
    return els

# ── Section 4: Full PO Creation flow ─────────────────────────────────────────
def section4():
    els = []
    els.append(section_header("Section 4 — PO Creation: Complete Sequence (Setup → Config → Process → Runtime)", SAP_DARK))
    els.append(sp(10))

    els.append(Paragraph("4.1  Setup Layer — One-Time SAP/Infrastructure", H2))
    els.append(simple_table(
        ["Step", "Activity", "Performed By", "What It Delivers"],
        [
            ["1.1", "Life Science Add-on installed on S4 Private Cloud", "SAP Cloud Operations", "/ATO extension tables, OData extensions, CD registration"],
            ["1.2", "BTP tenant provisioned", "SAP Cloud Operations", "ATO SaaS, eSignature SaaS, Event Mesh, iFlow deployed"],
            ["1.3", "Communication Arrangement configured in S4", "Basis / Admin", "S4 ↔ BTP eSignature OAuth trust, outbound Event Mesh binding"],
        ],
        col_widths=[1.2*cm, 6*cm, 4.5*cm, 5.8*cm]
    ))
    els.append(sp(8))

    els.append(Paragraph("4.2  Configuration Layer — One-Time Functional Setup", H2))
    els.append(simple_table(
        ["Step", "SPRO / BTP Activity", "Performed By", "Result"],
        [
            ["2.1", "Activate scope item 84P — GxP Compliance", "Functional Configurator", "Reauthentication framework active, S-table entries loaded"],
            ["2.2", "Configure VC_SRA_SOT — Reauth object + class + nodes", "GxP Compliance Team", "PURCHASE_ORDER registered with callback class and node mapping"],
            ["2.3", "Configure regulated field list per node", "GxP Compliance Team", "THERAPY_TYPE, CLINICAL_STUDY, PROTOCOL_REF, PATIENT_REF set as triggers"],
            ["2.4", "Define reason codes in BTP for PURCHASE_ORDER", "GxP Compliance Team", "Clinical Protocol Update, Regulatory Submission etc. available in dropdown"],
            ["2.5", "ATO SaaS master data setup", "ATO Configuration Team", "Therapy types, clinical studies, protocols, patient numbering defined"],
        ],
        col_widths=[1.2*cm, 5.5*cm, 4.5*cm, 6.3*cm]
    ))
    els.append(sp(8))

    els.append(Paragraph("4.3  Process Start — Where the PO Journey Begins", H2))
    els.append(info_box(
        "From a business/process perspective, the PO journey does NOT start in S4. "
        "It starts in ATO SaaS on BTP when a patient is enrolled in a clinical study "
        "and the therapy orchestration engine determines that materials need to be procured."
    ))
    els.append(sp(6))

    els.append(code_block(
"""PROCESS START — OUTSIDE S4, IN ATO SaaS (BTP)
══════════════════════════════════════════════════════════════════

Step 0 — Clinical Demand (ATO SaaS)
  Patient enrolled in clinical study CS-2026-001
  Therapy: Cell & Gene Therapy
  Protocol: PROT-47B
  Patient Reference: PAT-00123 (autologous therapy)
  ATO orchestration engine:
    → "A Purchase Order must be created in S4 to procure materials"

Step 1 — ATO creates PO in S4 via OData API
  ATO SaaS → OData call → S4 PurchaseOrder API
  Payload:
    Standard fields:  Vendor 1000234, Material MAT-CGTH-001
                      Quantity 1 unit, Delivery 2026-08-15
    ATO ext fields:   TherapyType=CELL_GENE
                      ClinicalStudy=CS-2026-001
                      ProtocolRef=PROT-47B
                      PatientRef=PAT-00123

  S4 processes:
    EKKO row created
    EKPO row created
    /ATO/S4_PO_HEADER_EXT row created
    /ATO/S4_PO_ITEM_EXT row created
    Change Document created (system-to-system — NO reauthentication)
    ↳ GxP rule: automated system-context calls are excluded

Step 2 — S4 confirms back to ATO
  Outbound event: PurchaseOrder.Created
    → Event Mesh → iFlow (schema mapping) → ATO SaaS
    → ATO records PO 4500000123 against study CS-2026-001

Step 3 — Human User changes PO in ME21N
  Procurement officer opens PO 4500000123
  Changes THERAPY_TYPE: PLASMA → CELL_GENE
  Clicks SAVE
  → Reauthentication triggered (human user = regulated change)
  → Full Phase 1-4 save flow executes (see Section 3)

Step 4 — ATO SaaS notified of change
  Outbound event: PurchaseOrder.Changed
    → Event Mesh → iFlow → ATO SaaS
    → ATO updates therapy orchestration plan in real-time

Step 5 — GxP Audit Trail Complete
  CDPOS: THERAPY_TYPE changed PLASMA → CELL_GENE by I308878 at 14:30:22
  BTP:   SIG-20260624-00891 — I308878 re-authenticated, Reason: Clinical Protocol Update
  Combined = 21 CFR Part 11 compliant audit trail ✓"""))

    els.append(PageBreak())
    return els

# ── Section 5: Reauthentication config ───────────────────────────────────────
def section5():
    els = []
    els.append(section_header("Section 5 — Reauthentication Framework: Configuration & Behaviour", SAP_GOLD))
    els.append(sp(10))

    els.append(Paragraph("5.1  Three-Level Configuration Model", H2))
    els.append(simple_table(
        ["Level", "Location", "What Is Configured", "Delivered By"],
        [
            ["Level 1 — Object Registration", "S4 S-table VC_SRA_SOT (SPRO)", "Reauthentication object name, callback class, authorization class", "LOB team via 84P transport"],
            ["Level 2 — Field Mapping", "S4 S-table per node type", "Which fields on which node trigger reauthentication", "LOB team via 84P transport — customer can fine-tune"],
            ["Level 3 — Reason Codes", "BTP eSignature SaaS", "Reason codes attached to each business object type", "Auto-provisioned on 84P activation — customer can extend"],
        ],
        col_widths=[3.5*cm, 4*cm, 6*cm, 4*cm]
    ))
    els.append(sp(8))

    els.append(Paragraph("5.2  Relevancy Check — The Most Critical Method", H2))
    els.append(Paragraph(
        "The Relevancy Check callback is implemented by the LOB application team. "
        "It is the single decision point that determines whether reauthentication fires or not. "
        "If it returns FALSE — even due to a bug — reauthentication is silently skipped.", BODY))
    els.append(simple_table(
        ["Scenario", "Return Value", "Framework Action"],
        [
            ["No regulated field changed in this save", "ABAP_FALSE", "Skip reauthentication entirely — LUW commits normally"],
            ["A configured regulated field changed", "ABAP_TRUE", "Trigger reauthentication dialog — LUW paused until signed"],
            ["Exception raised / error in callback", "Treated as FALSE", "⚠ Reauthentication skipped — application bug risk"],
        ],
        col_widths=[6.5*cm, 3.5*cm, 7.5*cm]
    ))
    els.append(sp(8))

    els.append(Paragraph("5.3  Mass Update & Background Job Behaviour", H2))
    els.append(simple_table(
        ["Scenario", "Reauthentication Behaviour"],
        [
            ["User selects 10 objects, changes a regulated field", "Single dialog — user signs ONCE — signature covers all 10 objects"],
            ["Background job run by system/technical user", "EXCLUDED — GxP rule: automated system-context jobs do not require signature"],
            ["Background job triggered by user from Fiori UI", "Collect signature ONCE at trigger point (button click) — covers all resulting objects"],
            ["Scheduled job (independent background process)", "Out of scope — must run as system user"],
        ],
        col_widths=[7*cm, 10.5*cm]
    ))
    els.append(sp(8))

    els.append(Paragraph("5.4  Current Limitation — Value-Level Triggering", H2))
    els.append(info_box(
        "Current capability: reauthentication triggers when a configured field changes TO ANY VALUE. "
        "Not yet supported: trigger only when field changes from value A to specific value B "
        "(e.g. trigger only when status changes to REL, not for all status changes). "
        "This is on the framework roadmap but NOT delivered in 2702. "
        "Confirmed by Yadesh Gupta: 'We do not have that capability as of now — it will be delivered later.'"
    ))
    els.append(PageBreak())
    return els

# ── Section 6: Delivery timeline ─────────────────────────────────────────────
def section6():
    els = []
    els.append(section_header("Section 6 — Delivery Timeline & Open Items", colors.HexColor("#555555")))
    els.append(sp(10))

    els.append(Paragraph("6.1  Release Timeline", H2))
    els.append(simple_table(
        ["Release", "Deliverable", "Status"],
        [
            ["2025", "GxP NOT enabled in S/4HANA Cloud", "Historical"],
            ["2602 (2026)", "Discussions started, POC work, architecture decisions", "Done"],
            ["2608 (2026)", "Change Document for PO verified working for all relevant fields", "✓ Done"],
            ["2702 (2027)", "eSignature in ME21N + ATO/CGTO field extension + Reauthentication framework", "Planned"],
            ["Post-2702", "eSignature in modernised Manage PO App (BOF replacement)", "Deferred — pending app modernisation"],
            ["Future", "eSignature in new RAP-based modern PO UI", "Future"],
        ],
        col_widths=[3.5*cm, 10*cm, 4*cm]
    ))
    els.append(sp(8))

    els.append(Paragraph("6.2  Open Items", H2))
    els.append(simple_table(
        ["#", "Open Item", "Work Stream", "Target"],
        [
            ["1", "eSignature trigger integration in ME21N save flow", "WS1", "2702"],
            ["2", "Change Document registration for /ATO/S4_PO_HEADER_EXT fields", "WS1 + WS3", "2702"],
            ["3", "ATO/CGTO field extension OData API exposure", "WS3", "2702"],
            ["4", "Outbound event publishing S4 → Event Mesh for PO changes", "WS3", "2702"],
            ["5", "iFlow schema mapping for ATO extension fields", "WS3", "2702"],
            ["6", "Value-level triggering (field changes FROM value A TO value B)", "WS1", "Post-2702"],
            ["7", "eSignature in Manage PO App (BOF/Fiori)", "WS1", "Deferred"],
            ["8", "Mass update background job reauthentication handling", "WS1", "Under review"],
        ],
        col_widths=[0.8*cm, 8.5*cm, 3.2*cm, 5*cm]
    ))
    els.append(sp(8))

    els.append(Paragraph("6.3  Integration Checklist for LOB Application", H2))
    checklist = [
        ("Backend / ABAP", [
            "Implement Reauthentication callback class (Relevancy Check)",
            "Implement Authorization class",
            "Register reauthentication object in S-table VC_SRA_SOT",
            "Define node types and field mappings",
            "Configure regulated fields per node type",
            "Add content delivery to scope item 84P transport",
        ]),
        ("BTP Setup", [
            "Register reauthentication object name in BTP",
            "Define / attach reason codes to the object",
            "Verify reason codes appear for correct object only",
        ]),
        ("Application Code", [
            "Call REQUEST_REAUTH at correct trigger point (before save / on button press)",
            "Call VALIDATE_RESULT to confirm signature captured",
            "Call CHECK_ESIG_ACTIVE before any signature flow",
            "Handle ABAP_FALSE from relevancy check — no silent skip on error",
        ]),
        ("Testing", [
            "Test with scope item 84P active",
            "Test relevancy check returns TRUE only for regulated field changes",
            "Test dialog shows correct reason codes",
            "Test signature is linked to change document CHANGENR",
            "Test mass update — single sign covers all objects",
            "Test background job (system user) — reauthentication must be skipped",
        ]),
    ]
    for section_name, items in checklist:
        els.append(Paragraph(f"<b>{section_name}</b>", BODY))
        for item in items:
            els.append(Paragraph(f"☐  {item}", BULLET))
        els.append(sp(4))

    return els

# ── Build document ────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title="GxP CGTO ATO eSignature Complete Guide",
        author="SAP S/4HANA GxP Team",
    )

    story = []
    story.extend(cover_page())
    story.extend(section1())
    story.extend(section2())
    story.extend(section3())
    story.extend(section4())
    story.extend(section5())
    story.extend(section6())

    def on_page(canvas, doc):
        canvas.saveState()
        # footer
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(colors.HexColor("#888888"))
        canvas.drawString(2*cm, 1.2*cm, "GxP / CGTO / ATO / eSignature — Complete Technical & Process Guide")
        canvas.drawRightString(19.5*cm, 1.2*cm, f"Page {doc.page}")
        canvas.setStrokeColor(GREY_BORDER)
        canvas.setLineWidth(0.4)
        canvas.line(2*cm, 1.5*cm, 19.5*cm, 1.5*cm)
        canvas.restoreState()

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF created: {OUTPUT}")

build()
