from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUTPUT = r"C:\Users\I308878\GxP-CGTO-eSignature_Requirement\GxP_Complete_Setup_Guide.pdf"

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

styles = getSampleStyleSheet()
def ms(name, **kw):
    return ParagraphStyle(name=name, parent=styles["Normal"], **kw)

TITLE    = ms("T",  fontSize=19, textColor=WHITE,   fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=4)
SUBTITLE = ms("ST", fontSize=9,  textColor=colors.HexColor("#AACCFF"), fontName="Helvetica", alignment=TA_CENTER, spaceAfter=2)
META     = ms("M",  fontSize=7.5,textColor=colors.HexColor("#AACCFF"), fontName="Helvetica", alignment=TA_CENTER)
H1       = ms("H1", fontSize=12, textColor=WHITE,   fontName="Helvetica-Bold", spaceAfter=3)
H2       = ms("H2", fontSize=10, textColor=SAP_DARK,fontName="Helvetica-Bold", spaceAfter=3, spaceBefore=6)
H3       = ms("H3", fontSize=9,  textColor=SAP_BLUE,fontName="Helvetica-Bold", spaceAfter=2, spaceBefore=4)
BODY     = ms("B",  fontSize=8.5,textColor=BLACK,   leading=13, spaceAfter=3, alignment=TA_JUSTIFY)
BODY_SML = ms("BS", fontSize=8,  textColor=BLACK,   leading=12, spaceAfter=2)
CODE_S   = ms("CS", fontSize=7,  textColor=CODE_FG, fontName="Courier", leading=10.5, spaceAfter=1)
QUOTE_S  = ms("QS", fontSize=8,  textColor=DARK_GREY,fontName="Helvetica-Oblique", leading=12, leftIndent=10, spaceAfter=3)
TH       = ms("TH", fontSize=7.5,textColor=WHITE,   fontName="Helvetica-Bold", alignment=TA_CENTER)
TC       = ms("TC", fontSize=7.5,textColor=BLACK,   leading=10)
PHASE_L  = ms("PL", fontSize=11, textColor=WHITE,   fontName="Helvetica-Bold")
PHASE_S  = ms("PS", fontSize=7.5,textColor=colors.HexColor("#AACCFF"), fontName="Helvetica-Oblique")
STEP_N   = ms("SN", fontSize=14, textColor=WHITE,   fontName="Helvetica-Bold", alignment=TA_CENTER)
STEP_T   = ms("STt",fontSize=9,  textColor=WHITE,   fontName="Helvetica-Bold")

def sp(n=5): return Spacer(1, n)

# ── Helpers ───────────────────────────────────────────────────────────────────
def sec_hdr(num, title, subtitle, hdr_color=SAP_DARK, num_color=None):
    if not num_color: num_color = hdr_color
    num_t = Table([[Paragraph(str(num), STEP_N)]],
                  colWidths=[1.4*cm], rowHeights=[1.2*cm])
    num_t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),num_color),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    txt_t = Table([[Paragraph(title, PHASE_L)],[Paragraph(subtitle, PHASE_S)]],
                  colWidths=[16.1*cm])
    txt_t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), hdr_color),
        ("TOPPADDING",   (0,0),(-1,-1), 7),
        ("BOTTOMPADDING",(0,0),(-1,-1), 7),
        ("LEFTPADDING",  (0,0),(-1,-1), 12),
    ]))
    t = Table([[num_t, txt_t]], colWidths=[1.4*cm, 16.1*cm])
    t.setStyle(TableStyle([("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0),
                           ("LEFTPADDING",(0,0),(-1,-1),0),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    return t

def tbl(headers, rows, widths=None):
    n = len(headers)
    if not widths: widths=[17.5*cm/n]*n
    data=[[Paragraph(h,TH) for h in headers]]
    for row in rows: data.append([Paragraph(str(c),TC) for c in row])
    t=Table(data,colWidths=widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),SAP_BLUE),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,GREY_BG]),
        ("GRID",(0,0),(-1,-1),0.4,GREY_BORDER),
        ("TOPPADDING",(0,0),(-1,-1),4),
        ("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(-1,-1),5),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
    ]))
    return t

def info_box(text, bg=SAP_LIGHT, border=SAP_BLUE):
    t=Table([[Paragraph(text,BODY_SML)]],colWidths=[17.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),bg),
        ("LINEABOVE",(0,0),(-1,0),2,border),
        ("TOPPADDING",(0,0),(-1,-1),6),
        ("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("LEFTPADDING",(0,0),(-1,-1),10),
        ("RIGHTPADDING",(0,0),(-1,-1),8),
    ]))
    return t

def warn_box(t): return info_box(t, RED_LIGHT, RED)
def ok_box(t):   return info_box(t, GREEN_LIGHT, GREEN_OK)
def note_box(t): return info_box(t, GOLD_LIGHT, GOLD)

def code_block(lines):
    rows=[[Paragraph(l.replace(" ","&nbsp;").replace("<","&lt;").replace(">","&gt;") or "&nbsp;",CODE_S)] for l in lines]
    t=Table(rows,colWidths=[17.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),CODE_BG),
        ("TOPPADDING",(0,0),(-1,-1),5),
        ("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),8),
        ("RIGHTPADDING",(0,0),(-1,-1),6),
    ]))
    return t

def quote_box(text, speaker=""):
    c=f'"{text}"'
    if speaker: c+=f"  — <i>{speaker}</i>"
    t=Table([[Paragraph(c,QUOTE_S)]],colWidths=[17.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),GOLD_LIGHT),
        ("LINEBEFORE",(0,0),(0,-1),3,GOLD),
        ("TOPPADDING",(0,0),(-1,-1),6),
        ("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("LEFTPADDING",(0,0),(-1,-1),12),
        ("RIGHTPADDING",(0,0),(-1,-1),8),
    ]))
    return t

def step_row(num, action, detail, color=SAP_BLUE):
    n_t=Table([[Paragraph(str(num),ms(f"sn{num}",fontSize=10,textColor=WHITE,
               fontName="Helvetica-Bold",alignment=TA_CENTER))]],
              colWidths=[0.8*cm],rowHeights=[None])
    n_t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),color),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                              ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]))
    a_t=Table([[Paragraph(action,ms(f"sa{num}",fontSize=8,textColor=BLACK,fontName="Helvetica-Bold"))],
               [Paragraph(detail,BODY_SML)]],colWidths=[16.7*cm])
    a_t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),WHITE),
        ("LINEBELOW",(0,1),(0,1),0.3,GREY_BORDER),
        ("TOPPADDING",(0,0),(-1,-1),4),
        ("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(-1,-1),8),
    ]))
    t=Table([[n_t,a_t]],colWidths=[0.8*cm,16.7*cm])
    t.setStyle(TableStyle([
        ("LINEABOVE",(0,0),(-1,0),0.5,color),
        ("LINEBELOW",(0,0),(-1,0),0.5,GREY_BORDER),
        ("TOPPADDING",(0,0),(-1,-1),0),
        ("BOTTOMPADDING",(0,0),(-1,-1),0),
        ("LEFTPADDING",(0,0),(-1,-1),0),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
    ]))
    return [t, sp(3)]

# ══════════════════════════════════════════════════════════════════════════════
def cover():
    els=[]
    cov=Table([
        [Paragraph("GxP / ATO / eSignature", TITLE)],
        [Paragraph("Complete End-to-End Setup Guide", SUBTITLE)],
        [Paragraph("From Add-on Installation to PO Registration → ATO OData V4 → eSignature → Reauthentication → BTP Comm Arrangement", SUBTITLE)],
        [Paragraph("SAP S/4HANA Public Cloud  |  BTP ATO SaaS  |  Scope Item 84P  |  2026-06-26", META)],
    ],colWidths=[17.5*cm])
    cov.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),SAP_DARK),
                              ("TOPPADDING",(0,0),(-1,-1),26),("BOTTOMPADDING",(0,0),(-1,-1),26),
                              ("LEFTPADDING",(0,0),(-1,-1),20)]))
    els.append(cov)
    els.append(sp(12))

    els.append(Paragraph("Complete Setup Sequence", H2))
    els.append(tbl(
        ["Phase","Title","System","When"],
        [
            ["Phase 1","Install Life Science Add-on in S4","S4 — Basis","One-time"],
            ["Phase 2","Activate Scope Item 84P — GxP Framework","S4 — SPRO","One-time"],
            ["Phase 3","Register Purchase Order Object in VC_SRA_SOT","S4 — SPRO","One-time per LOB"],
            ["Phase 4","Implement PO Relevancy Check Callback Class","S4 — SE24","Dev task"],
            ["Phase 5","Enable ATO Fields in PO OData V4 API","S4 — /IWBEP/V4_ADMIN","CE2608 delivered"],
            ["Phase 6","Configure ATO Extension Tables & SEGW","S4 — SE11 + SEGW","POC — CGTO_S4HC_POC"],
            ["Phase 7","Register ATO Fields in Change Document Object","S4 — SCDO","CE2608 / ATO team"],
            ["Phase 8","Set Up BTP eSignature SaaS Communication","S4 + BTP","One-time"],
            ["Phase 9","Configure BTP — Register PO Object & Reason Codes","BTP","One-time per LOB"],
            ["Phase 10","Integrate REQUEST_REAUTH in ME21N Save Flow","S4 — SE24 / BAdI","Dev task — 2702"],
            ["Phase 11","Set Up ATO SaaS — Event Mesh & iFlow","BTP","One-time"],
            ["Phase 12","End-to-End Validation","All systems","After all phases"],
        ],
        widths=[1.8*cm,7*cm,4.2*cm,4.5*cm]
    ))
    els.append(sp(8))
    els.append(info_box(
        "Reading guide: Each phase has numbered steps. Complete them in order — "
        "phases are dependent on each other. Phase 5 (OData V4 extensibility) was delivered "
        "in CE2608 and may already be done. Always verify before repeating."
    ))
    els.append(PageBreak())
    return els

# ── Phase 1 ───────────────────────────────────────────────────────────────────
def phase1():
    els2=[]
    els2.append(sec_hdr("1","Install Life Science Add-on in S4",
                        "Delivers /ATO/ extension tables, OData extensions, Change Document registration",
                        SAP_DARK, SAP_DARK))
    els2.append(sp(8))
    els2.append(Paragraph(
        "The Life Science Add-on (LS_ADD_ON) is delivered by SAP Cloud Operations. "
        "It installs all /ATO/ namespace objects, extension tables, and wires up the PO OData API. "
        "This is NOT a manual step — it requires SAP to apply the transport.", BODY))
    els2.append(sp(5))
    steps=[
        ("Request Add-on Installation",
         "Raise a request with SAP Cloud Operations to install LS_ADD_ON / ATO_S4HC on the target system.\n"
         "Life Science Add-on = ATO + SI + CSAI + CSM + BRH combined package.\n"
         "Specify: target system ID, release version, required by date."),
        ("SAP applies add-on transport",
         "SAP Cloud Operations applies the transport. Delivered objects:\n"
         "  /ATO/S4_PO_HEADER_EXT  — PO Header extension table (FK → EKKO)\n"
         "  /ATO/S4_PO_ITEM_EXT    — PO Item extension table (FK → EKPO)\n"
         "  Industry Object Extension nodes on EKKO and EKPO\n"
         "  PurchaseOrder OData V4 API extended with TherapyType, ClinicalStudy, ProtocolRef, PatientRef\n"
         "  Change Document EINKBELEG extended to include /ATO/S4_PO_HEADER_EXT\n"
         "  Package CGTO_S4HC_POC with all objects"),
        ("Verify: SAINT",
         "Transaction: SAINT → Status tab\n"
         "Expected: LS_ADD_ON or ATO_S4HC → Status = INSTALLED with version"),
        ("Verify: SE11 extension tables",
         "SE11 → /ATO/S4_PO_HEADER_EXT → Status = Active\n"
         "SE11 → /ATO/S4_PO_ITEM_EXT → Status = Active\n"
         "Both must exist before any further configuration"),
        ("Verify: SE03 namespace",
         "SE03 → Namespace → /ATO/ → Status = ACTIVE"),
        ("Verify: SCDO Change Document",
         "SCDO → EINKBELEG → Table Names tab\n"
         "/ATO/S4_PO_HEADER_EXT must be in the list → confirms CE2608 change doc work applied"),
    ]
    for i,(action,detail) in enumerate(steps,1):
        for row in step_row(i, action, detail, SAP_DARK):
            els2.append(row)
    els2.append(ok_box("✅  Phase 1 complete when SAINT=INSTALLED, both SE11 tables Active, SCDO has /ATO/ table."))
    els2.append(PageBreak())
    return els2

# ── Phase 2 ───────────────────────────────────────────────────────────────────
def phase2():
    els=[]
    els.append(sec_hdr("2","Activate Scope Item 84P — GxP Framework",
                       "S4 + BTP activation — switches on Reauthentication Framework and provisions BTP tenant",
                       SAP_BLUE, SAP_DARK))
    els.append(sp(8))
    steps=[
        ("Access SAP Cloud Solution Configuration",
         "In S4HC Admin Launchpad → Solution Configuration → Scope\n"
         "OR via SAP Central Business Configuration (CBC)"),
        ("Search for Scope Item 84P",
         "Search field: enter '84P' or 'GxP'\n"
         "Scope item name: GxP Compliance\n"
         "Select it and review the description"),
        ("Activate 84P",
         "Click Activate / Include in Scope\n"
         "System will prompt for transport request → assign to your project transport\n"
         "Activation triggers:\n"
         "  • VC_SRA_SOT S-table entries created in S4\n"
         "  • SPRO → GxP Compliance menu becomes available\n"
         "  • BTP eSignature SaaS tenant provisioned automatically"),
        ("Verify S4 activation — SPRO",
         "SPRO → search for 'GxP' or 'Reauthentication'\n"
         "GxP Compliance customising node should appear in SPRO tree"),
        ("Verify BTP provisioning",
         "BTP Cockpit → your subaccount → Instances and Subscriptions\n"
         "eSignature SaaS service should appear as provisioned"),
        ("Test CHECK_ESIG_ACTIVE",
         "After activation → CHECK_ESIG_ACTIVE should return ABAP_TRUE\n"
         "If FALSE: verify Communication Arrangement (Phase 8) is also configured"),
    ]
    for i,(a,d) in enumerate(steps,1):
        for row in step_row(i,a,d,SAP_BLUE): els.append(row)
    els.append(sp(5))
    els.append(warn_box(
        "⚠  84P activation is a system-wide change. Activating it enables GxP compliance mode "
        "for ALL registered business objects. Ensure all LOB teams are ready before activating "
        "in production. Always activate in a test/sandbox system first."
    ))
    els.append(PageBreak())
    return els

# ── Phase 3 ───────────────────────────────────────────────────────────────────
def phase3():
    els=[]
    els.append(sec_hdr("3","Register Purchase Order Object in VC_SRA_SOT",
                       "SPRO configuration — tells the framework which PO fields require reauthentication",
                       PURPLE, SAP_DARK))
    els.append(sp(8))
    steps=[
        ("Open SPRO GxP node",
         "Transaction: SPRO → search 'GxP Compliance' or 'Reauthentication'\n"
         "Navigate to: GxP Compliance → Reauthentication → Define Reauthentication Objects"),
        ("Create PURCHASE_ORDER entry",
         "Click New Entry\n"
         "  Reauth Object:  PURCHASE_ORDER\n"
         "  Description:    Purchase Order GxP Reauthentication\n"
         "  Reauth Class:   ZCL_PO_REAUTH_CHECK   (callback class — implement in Phase 4)\n"
         "  Auth Class:     ZCL_PO_AUTH_CHECK      (authorization class — implement in Phase 4)\n"
         "Save"),
        ("Define Node Types for PO",
         "Select PURCHASE_ORDER entry → Navigate to Node Types\n"
         "Create node 1:\n"
         "  Node Name:     PO_HEADER_EXT\n"
         "  Table Name:    /ATO/S4_PO_HEADER_EXT\n"
         "  Description:   ATO Header Extension Fields\n"
         "Create node 2:\n"
         "  Node Name:     PO_ITEM_EXT\n"
         "  Table Name:    /ATO/S4_PO_ITEM_EXT\n"
         "  Description:   ATO Item Extension Fields"),
        ("Define Regulated Fields per Node",
         "Select PO_HEADER_EXT node → Navigate to Field Configuration\n"
         "Add regulated fields (one row each):\n"
         "  Field Name: THERAPY_TYPE     Description: Therapy Type\n"
         "  Field Name: CLINICAL_STUDY   Description: Clinical Study Reference\n"
         "  Field Name: PROTOCOL_REF     Description: Protocol Reference\n"
         "\n"
         "Select PO_ITEM_EXT node → Field Configuration\n"
         "  Field Name: THERAPY_TYPE\n"
         "  Field Name: PATIENT_REF"),
        ("Save and transport",
         "Save all configuration → assign to transport request\n"
         "This content will be delivered as part of 84P transport to other systems"),
        ("Verify via SE16N",
         "SE16N → VC_SRA_SOT\n"
         "Confirm rows exist for PURCHASE_ORDER with correct class names and nodes"),
    ]
    for i,(a,d) in enumerate(steps,1):
        for row in step_row(i,a,d,PURPLE): els.append(row)
    els.append(sp(5))
    els.append(note_box(
        "The Relevancy Check callback class (ZCL_PO_REAUTH_CHECK) and authorization class "
        "(ZCL_PO_AUTH_CHECK) must be registered here BEFORE implementing them in Phase 4. "
        "The class names must match exactly — VC_SRA_SOT looks them up by name at runtime."
    ))
    els.append(PageBreak())
    return els

# ── Phase 4 ───────────────────────────────────────────────────────────────────
def phase4():
    els=[]
    els.append(sec_hdr("4","Implement PO Relevancy Check Callback Class",
                       "SE24 — ABAP class that decides whether reauthentication is required",
                       ORANGE, SAP_DARK))
    els.append(sp(8))
    steps=[
        ("Create ZCL_PO_REAUTH_CHECK in SE24",
         "SE24 → Class → ZCL_PO_REAUTH_CHECK → Create\n"
         "  Class Type: Regular Class\n"
         "  Final: Yes\n"
         "  Description: PO Reauthentication Relevancy Check"),
        ("Add interface IF_REAUTH_RELEVANCY_CHECK",
         "Interfaces tab → Add: IF_REAUTH_RELEVANCY_CHECK\n"
         "This interface provides the IS_REAUTHENTICATION_RELEVANT method signature"),
        ("Implement IS_REAUTHENTICATION_RELEVANT",
         "Methods tab → double-click IS_REAUTHENTICATION_RELEVANT → implement:"),
    ]
    for i,(a,d) in enumerate(steps,1):
        for row in step_row(i,a,d,ORANGE): els.append(row)

    els.append(code_block([
        "METHOD if_reauth_relevancy_check~is_reauthentication_relevant.",
        "",
        "  \" Get regulated field list from S-table via framework utility",
        "  DATA: lt_reg_fields TYPE TABLE OF vc_sra_sot_fields,",
        "        lv_relevant    TYPE abap_bool VALUE abap_false.",
        "",
        "  \" Call framework utility to read configured regulated fields",
        "  \" for PURCHASE_ORDER object from VC_SRA_SOT",
        "  \" (Framework provides this utility — LOB does not query VC_SRA_SOT directly)",
        "",
        "  \" Check if any of the regulated fields changed in this save",
        "  \" For ATO fields on PO header extension:",
        "  IF im_changed_fields-therapy_type    IS NOT INITIAL OR",
        "     im_changed_fields-clinical_study  IS NOT INITIAL OR",
        "     im_changed_fields-protocol_ref    IS NOT INITIAL OR",
        "     im_changed_fields-patient_ref     IS NOT INITIAL.",
        "    lv_relevant = abap_true.",
        "  ENDIF.",
        "",
        "  \" Return result",
        "  re_relevant = lv_relevant.",
        "",
        "ENDMETHOD.",
    ]))

    steps2=[
        ("Create ZCL_PO_AUTH_CHECK",
         "SE24 → ZCL_PO_AUTH_CHECK → Create\n"
         "Implements authorization check interface\n"
         "Logic: check if current user has authority to perform this regulated change\n"
         "For CRUD operations: check CREATE/CHANGE authority on purchase order object"),
        ("Activate both classes",
         "SE24 → ZCL_PO_REAUTH_CHECK → Activate (Ctrl+F3)\n"
         "SE24 → ZCL_PO_AUTH_CHECK → Activate (Ctrl+F3)"),
        ("Test with ABAP Unit",
         "SE24 → Local Test Classes tab → write unit tests:\n"
         "  Test 1: ATO field changed → method returns ABAP_TRUE\n"
         "  Test 2: Non-ATO field changed → method returns ABAP_FALSE\n"
         "  Test 3: No fields changed → method returns ABAP_FALSE"),
    ]
    for i,(a,d) in enumerate(steps2,4):
        for row in step_row(i,a,d,ORANGE): els.append(row)
    els.append(ok_box("✅  Phase 4 complete when both classes are Active and unit tests pass."))
    els.append(PageBreak())
    return els

# ── Phase 5 ───────────────────────────────────────────────────────────────────
def phase5():
    els=[]
    els.append(sec_hdr("5","Enable ATO Fields in PO OData V4 API",
                       "CE2608 deliverable — internal extensibility already enabled by PO standard team",
                       TEAL, SAP_DARK))
    els.append(sp(8))
    els.append(ok_box(
        "✅  CE2608 STATUS: This phase was delivered in CE2608 by the PO standard team (Nils/Jiss). "
        "The OData V4 PurchaseOrder API internal extensibility is already enabled. "
        "Verify it is in place before proceeding. If already enabled — skip to Phase 6."
    ))
    els.append(sp(5))
    steps=[
        ("Verify OData V4 API extensibility",
         "Transaction: /IWBEP/V4_ADMIN\n"
         "Search for service: API_PURCHASEORDER_2\n"
         "Check: Internal Extensibility = Enabled\n"
         "If Enabled → proceed to Phase 6. If NOT → follow steps below."),
        ("Enable extensibility (if not already done)",
         "This requires the PO standard team (Nils Hartmann / Jiss) to apply the enablement.\n"
         "Contact: nils.hartmann@sap.com\n"
         "Reference: CE2608 — 'OData V4 API enabled for internal extensibility\n"
         "(without the PaaS API extension)'"),
        ("Verify ATO extension visible in $metadata",
         "Gateway Client → GET /sap/opu/odata4/sap/api_purchaseorder_2/srvd_a2x/sap/purchaseorder/0001/$metadata\n"
         "Search response XML for: TherapyType, ClinicalStudy, ProtocolRef, PatientRef\n"
         "These properties must appear in the PurchaseOrder entity type"),
        ("Test OData call with ATO fields",
         "Gateway Client → POST to PurchaseOrder API\n"
         "Include ATO fields in request body:\n"
         "  \"to_PurchaseOrderHeaderExtension\": {\n"
         "    \"TherapyType\": \"CELL_GENE\",\n"
         "    \"ClinicalStudy\": \"CS-TEST-001\"\n"
         "  }\n"
         "Verify response includes ATO fields and /ATO/S4_PO_HEADER_EXT row created"),
    ]
    for i,(a,d) in enumerate(steps,1):
        for row in step_row(i,a,d,TEAL): els.append(row)
    els.append(PageBreak())
    return els

# ── Phase 6 ───────────────────────────────────────────────────────────────────
def phase6():
    els=[]
    els.append(sec_hdr("6","Configure ATO Extension Tables in SEGW",
                       "Register /ATO/ tables as separate Business Object — Industry Object Extension pattern",
                       BTP_GREEN, SAP_DARK))
    els.append(sp(8))
    els.append(info_box(
        "Architecture decision (confirmed in meetings): ATO fields are stored in SEPARATE "
        "Business Objects (/ATO/S4_PO_HEADER_EXT and /ATO/S4_PO_ITEM_EXT) — NOT appended "
        "directly to EKKO/EKPO. This enables third-level extension which native EKKO append cannot support."
    ))
    els.append(sp(5))
    steps=[
        ("Verify tables exist and are active",
         "SE11 → /ATO/S4_PO_HEADER_EXT → Active\n"
         "SE11 → /ATO/S4_PO_ITEM_EXT → Active\n"
         "Fields: EBELN (FK), THERAPY_TYPE, CLINICAL_STUDY, PROTOCOL_REF (header)\n"
         "        EBELN+EBELP (FK), THERAPY_TYPE, PATIENT_REF (item)"),
        ("Verify Industry Object Extension node is registered",
         "The add-on (Phase 1) registers the extension nodes on EKKO and EKPO.\n"
         "Verify: EKKO has an Industry Object Extension node pointing to /ATO/S4_PO_HEADER_EXT\n"
         "Check via: SE11 → EKKO → Display → Enhancement Categories / Extension nodes"),
        ("Verify SEGW service exposes ATO fields",
         "SEGW → open PurchaseOrder OData service (if custom SEGW service exists for ATO)\n"
         "OR verify via /IWBEP/V4_ADMIN that TherapyType etc. are in the entity type\n"
         "The add-on delivers the OData extension automatically"),
        ("Verify data in extension tables after PO creation",
         "Create a test PO via ATO or ME21N with ATO fields populated\n"
         "SE16N → /ATO/S4_PO_HEADER_EXT → filter EBELN = <PO number>\n"
         "Confirm row exists with correct THERAPY_TYPE, CLINICAL_STUDY, PROTOCOL_REF"),
        ("Verify ME23N shows ATO tab",
         "ME23N → open PO → look for 'Advanced Therapy Information' tab on header\n"
         "Tab should show Therapy Type, Clinical Study, Protocol Ref fields\n"
         "This tab is delivered by the add-on — no custom Fiori development needed"),
    ]
    for i,(a,d) in enumerate(steps,1):
        for row in step_row(i,a,d,BTP_GREEN): els.append(row)
    els.append(ok_box("✅  Phase 6 complete when /ATO/ tables have data and ME23N shows ATO tab."))
    els.append(PageBreak())
    return els

# ── Phase 7 ───────────────────────────────────────────────────────────────────
def phase7():
    els=[]
    els.append(sec_hdr("7","Register ATO Fields in Change Document Object (EINKBELEG)",
                       "Ensures ATO field changes are recorded in CDHDR/CDPOS — GxP audit trail requirement",
                       SAP_DARK, SAP_DARK))
    els.append(sp(8))
    els.append(info_box(
        "Status: ATO team (Allen Yuan) completed a POC of this registration. "
        "Approach: extend EINKBELEG to include /ATO/S4_PO_HEADER_EXT + adjust function module. "
        "Open issue: ATO change rows appear in CDPOS but description is blank in ME23N change log screen."
    ))
    els.append(sp(5))
    steps=[
        ("Verify EINKBELEG already includes ATO table",
         "SCDO → EINKBELEG → Table Names tab\n"
         "If /ATO/S4_PO_HEADER_EXT is listed → Phase 1 add-on applied this. Skip to step 4.\n"
         "If NOT listed → proceed with steps 2-3"),
        ("Extend EINKBELEG with /ATO/S4_PO_HEADER_EXT",
         "SCDO → EINKBELEG → Change\n"
         "Table Names tab → Add row:\n"
         "  Table Name: /ATO/S4_PO_HEADER_EXT\n"
         "  Documentation Key: ATO Header Extension\n"
         "Save → Activate → assign transport\n"
         "NOTE: This requires contact with ATO team (Allen Yuan / Loring Wu) to confirm approach"),
        ("Adjust function module for ATO change recording",
         "ATO team confirmed: a function module was adjusted to SEPARATELY call the\n"
         "change document recording for ATO fields when a PO with ATO data is saved.\n"
         "This is called in the PO BAdI body (ME_PROCESS_PO_CUST or equivalent).\n"
         "Contact: Allen Yuan (ATO dev team) for the exact function module name"),
        ("Add implicit enhancement for description text",
         "ATO team added an implicit enhancement in the standard programme to display\n"
         "description text for /ATO/ table fields in the ME22N/ME23N change log screen.\n"
         "Acceptability of this approach to be confirmed with PO standard team (Jiss/Nils).\n"
         "Alternative: investigate BAdI 'Change Document Processing' as a cleaner approach"),
        ("Verify change log recording",
         "ME21N → create PO with Therapy Type = CELL_GENE → Save\n"
         "ME22N → change Therapy Type to PLASMA → Save\n"
         "SE16N → CDPOS → filter CHANGENR for this PO\n"
         "Expected row: TABNAME=/ATO/S4_PO_HEADER_EXT, FNAME=THERAPY_TYPE, VALUE_OLD=CELL_GENE, VALUE_NEW=PLASMA"),
    ]
    for i,(a,d) in enumerate(steps,1):
        for row in step_row(i,a,d,SAP_DARK): els.append(row)
    els.append(warn_box(
        "⚠  OPEN ISSUE: ATO field changes ARE recorded in CDPOS correctly. "
        "However the ME22N/ME23N change log DISPLAY screen shows blank description for ATO rows. "
        "Joint call needed: ATO team (Allen Yuan) + PO team (Jiss) + Change Document team. "
        "This must be resolved before claiming GxP compliance for ATO field changes."
    ))
    els.append(PageBreak())
    return els

# ── Phase 8 ───────────────────────────────────────────────────────────────────
def phase8():
    els=[]
    els.append(sec_hdr("8","Set Up BTP eSignature SaaS Communication Arrangement",
                       "S4 ↔ BTP OAuth trust — enables S4 to call BTP eSignature service",
                       PURPLE, SAP_DARK))
    els.append(sp(8))
    els.append(info_box(
        "This Communication Arrangement is pre-wired when 84P is activated (Phase 2). "
        "If 84P was activated correctly, this may already be in place. "
        "Verify before setting up manually. Contact: Swarnava Chatterjee for BTP service details."
    ))
    els.append(sp(5))
    steps=[
        ("Verify if pre-wired by 84P activation",
         "Transaction: /IWFND/MAINT_SERVICE or Communication Arrangements app in S4HC Admin\n"
         "Search for a communication arrangement related to eSignature or GxP\n"
         "If found and active → skip to step 5 (verify connectivity)"),
        ("Create Communication System in S4",
         "S4HC Admin → Communication Systems → New\n"
         "  System ID:     BTP_ESIGNATURE\n"
         "  System Name:   BTP eSignature SaaS\n"
         "  Host Name:     <BTP eSignature SaaS endpoint URL>\n"
         "  OAuth 2.0:     Enabled\n"
         "  Token URL:     <BTP OAuth token endpoint>\n"
         "  Client ID:     <from BTP service key>\n"
         "  Client Secret: <from BTP service key>"),
        ("Get BTP service key credentials",
         "BTP Cockpit → Subaccount → Instances → eSignature SaaS instance\n"
         "Create a Service Key if not existing\n"
         "Copy: clientid, clientsecret, url, tokenurl from the JSON service key"),
        ("Create Communication Arrangement",
         "S4HC Admin → Communication Arrangements → New\n"
         "  Scenario:          SAP_COM_XXXX (GxP eSignature — exact ID from SAP docs)\n"
         "  Arrangement Name:  CA_BTP_ESIGNATURE\n"
         "  Communication System: BTP_ESIGNATURE (from step 2)\n"
         "  Authentication:    OAuth 2.0 Client Credentials\n"
         "Save"),
        ("Test connectivity",
         "In Communication Arrangement → Test Connection button\n"
         "Expected: Green connection indicator — HTTP 200 from BTP eSignature endpoint\n"
         "If red: verify OAuth credentials, check BTP service is running, verify URLs"),
        ("Verify CHECK_ESIG_ACTIVE returns TRUE",
         "After Communication Arrangement is active AND 84P is activated:\n"
         "CHECK_ESIG_ACTIVE API should now return ABAP_TRUE\n"
         "Test via ABAP Console or SE38 test report"),
    ]
    for i,(a,d) in enumerate(steps,1):
        for row in step_row(i,a,d,PURPLE): els.append(row)
    els.append(ok_box("✅  Phase 8 complete when Communication Arrangement test = green AND CHECK_ESIG_ACTIVE = TRUE."))
    els.append(PageBreak())
    return els

# ── Phase 9 ───────────────────────────────────────────────────────────────────
def phase9():
    els=[]
    els.append(sec_hdr("9","Configure BTP — Register PO Object and Reason Codes",
                       "BTP eSignature SaaS — define PURCHASE_ORDER and its reason codes",
                       BTP_GREEN, SAP_DARK))
    els.append(sp(8))
    els.append(info_box(
        "When 84P is activated, SAP-suggested reason codes are auto-provisioned in BTP. "
        "This phase covers verifying they are in place and adding custom ones if needed."
    ))
    els.append(sp(5))
    steps=[
        ("Access BTP eSignature SaaS Admin",
         "BTP Cockpit → Subaccount → eSignature SaaS application → Open\n"
         "Log in with admin credentials"),
        ("Verify PURCHASE_ORDER object is registered",
         "In eSignature Admin → Business Objects section\n"
         "PURCHASE_ORDER should be listed (auto-provisioned by 84P activation)\n"
         "If not listed → create manually (step 3)"),
        ("Register PURCHASE_ORDER manually if needed",
         "Business Objects → Add New\n"
         "  Object Name:   PURCHASE_ORDER\n"
         "  Description:   SAP S4 Purchase Order\n"
         "  S4 System:     <your S4 system ID>\n"
         "Save"),
        ("Verify SAP-suggested reason codes are loaded",
         "Select PURCHASE_ORDER → Reason Codes tab\n"
         "SAP-suggested codes (auto-provisioned by 84P):\n"
         "  • Clinical Protocol Update\n"
         "  • Regulatory Submission\n"
         "  • Error Correction\n"
         "  • Therapy Type Reassignment"),
        ("Add custom reason codes if needed",
         "Reason Codes → Add New\n"
         "  Code:        CUSTOM_01\n"
         "  Description: Patient-Specific Order Change\n"
         "Save\n"
         "Note: Only reason codes assigned to PURCHASE_ORDER appear in the PO reauthentication dropdown"),
        ("Test reason code dropdown",
         "In ME21N → change Therapy Type → Save\n"
         "Reauthentication dialog should appear (only after Phase 10 is complete)\n"
         "Dropdown should show only PURCHASE_ORDER reason codes"),
    ]
    for i,(a,d) in enumerate(steps,1):
        for row in step_row(i,a,d,BTP_GREEN): els.append(row)
    els.append(PageBreak())
    return els

# ── Phase 10 ──────────────────────────────────────────────────────────────────
def phase10():
    els=[]
    els.append(sec_hdr("10","Integrate REQUEST_REAUTH in ME21N Save Flow",
                       "SE24 — BAdI ME_PROCESS_PO_CUST — 2702 planned development task",
                       RED, SAP_DARK))
    els.append(sp(8))
    els.append(warn_box(
        "⚠  This phase is planned for 2702 and has NOT been implemented yet. "
        "This is the core eSignature integration work. Complete Phases 1-9 first."
    ))
    els.append(sp(5))
    steps=[
        ("Create BAdI implementation for ME_PROCESS_PO_CUST",
         "SE19 → BAdI: ME_PROCESS_PO_CUST (Enhancement Spot: ME_PURCHORD)\n"
         "Create implementation: ZCL_PO_ESIGN_BADI_IMPL\n"
         "Methods to implement: PROCESS_HEADER, PROCESS_ITEM"),
        ("Implement PROCESS_HEADER method",
         "This fires when PO header is saved. Add reauthentication call:"),
    ]
    for i,(a,d) in enumerate(steps,1):
        for row in step_row(i,a,d,RED): els.append(row)

    els.append(code_block([
        "METHOD if_ex_me_process_po_cust~process_header.",
        "",
        "  DATA(lv_ebeln) = im_header->get_data( )-ebeln.",
        "  IF lv_ebeln IS INITIAL. RETURN. ENDIF.",
        "",
        "  \" Step 1: Check if GxP is active in this system",
        "  DATA lv_active TYPE abap_bool.",
        "  \" CALL METHOD cl_gxp_framework=>check_esig_active RECEIVING rv_active = lv_active.",
        "  IF lv_active = abap_false. RETURN. ENDIF.",
        "",
        "  \" Step 2: Relevancy check — did any ATO regulated field change?",
        "  DATA lv_relevant TYPE abap_bool.",
        "  \" Framework calls ZCL_PO_REAUTH_CHECK automatically via VC_SRA_SOT lookup",
        "  IF lv_relevant = abap_false. RETURN. ENDIF.",
        "",
        "  \" Step 3: Trigger reauthentication dialog (LUW paused until user signs)",
        "  \" CALL METHOD cl_gxp_framework=>request_reauth",
        "  \"   EXPORTING iv_object = 'PURCHASE_ORDER'",
        "  \"             iv_ebeln  = lv_ebeln.",
        "",
        "  \" Step 4: Validate result",
        "  \" CALL METHOD cl_gxp_framework=>validate_result",
        "  \"   RECEIVING rv_signed = DATA(lv_signed).",
        "  \" IF lv_signed = abap_false. RAISE ... ENDIF.",
        "",
        "ENDMETHOD.",
    ]))

    steps2=[
        ("Implement PROCESS_ITEM method",
         "Same pattern as PROCESS_HEADER but for item-level ATO fields\n"
         "Read im_item->get_data()-ebelp for the item number\n"
         "Check if THERAPY_TYPE or PATIENT_REF on the item changed"),
        ("Activate BAdI implementation",
         "SE19 → ZCL_PO_ESIGN_BADI_IMPL → Activate\n"
         "BAdI is now active — fires on every ME21N / ME22N save"),
        ("Test end-to-end in ME21N",
         "ME21N → create PO → enter TherapyType = CELL_GENE → Save\n"
         "Expected: reauthentication dialog appears\n"
         "Enter password + select reason code → Confirm\n"
         "PO saved. CDHDR has new CHANGENR. BTP Signature ID linked."),
        ("Verify complete audit trail",
         "SE16N → CDHDR → find PO → note CHANGENR\n"
         "SE16N → CDPOS → CHANGENR → THERAPY_TYPE row with VALUE_NEW=CELL_GENE\n"
         "BTP eSignature Admin → Signature record linked to CHANGENR\n"
         "Combined = 21 CFR Part 11 compliant audit trail ✓"),
    ]
    for i,(a,d) in enumerate(steps2,3):
        for row in step_row(i,a,d,RED): els.append(row)
    els.append(ok_box("✅  Phase 10 complete when reauthentication dialog appears in ME21N and CDHDR/BTP both have records."))
    els.append(PageBreak())
    return els

# ── Phase 11 ──────────────────────────────────────────────────────────────────
def phase11():
    els=[]
    els.append(sec_hdr("11","Set Up ATO SaaS — Event Mesh and iFlow",
                       "BTP — enables bidirectional PO event exchange between ATO SaaS and S4",
                       TEAL, SAP_DARK))
    els.append(sp(8))
    steps=[
        ("Provision BTP Event Mesh",
         "BTP Cockpit → Subaccount → Service Marketplace → Event Mesh → Create Instance\n"
         "Plan: Standard or Enterprise (based on event volume)\n"
         "Create service key → note connection details"),
        ("Configure S4 outbound event binding",
         "S4HC Admin → Enterprise Event Enablement\n"
         "Add topic binding for PO events:\n"
         "  Topic: sap/s4/beh/purchaseorder/v1/PurchaseOrder/Changed/v1\n"
         "  Topic: sap/s4/beh/purchaseorder/v1/PurchaseOrder/Created/v1\n"
         "  Channel: your Event Mesh namespace\n"
         "Save → events will be published to Event Mesh on PO save"),
        ("Deploy iFlow in Integration Suite",
         "BTP → Integration Suite → Design → Import iFlow package from SAP API Hub:\n"
         "  Package: ATO S4 Integration iFlows\n"
         "  Contains: PO Create iFlow, PO Update iFlow, PO Cancel iFlow\n"
         "Configure:\n"
         "  Source: Event Mesh topic subscription\n"
         "  Target: S4 PurchaseOrder OData V4 API endpoint\n"
         "  Auth: OAuth credentials from Phase 8 Communication Arrangement"),
        ("Configure iFlow schema mapping",
         "ATO SaaS event schema ≠ S4 OData API schema\n"
         "iFlow mapping handles:\n"
         "  ATO TherapyId → S4 TherapyType\n"
         "  ATO StudyRef → S4 ClinicalStudy\n"
         "  ATO ProtocolId → S4 ProtocolRef\n"
         "  ATO PatientId → S4 PatientRef\n"
         "Deploy and activate iFlow"),
        ("Configure ATO SaaS event subscription",
         "ATO Cloud Admin → Integration Settings\n"
         "  S4 Endpoint: your S4 OData V4 PurchaseOrder API URL\n"
         "  Event Mesh: connection details from step 1\n"
         "  Subscribe to topics: PurchaseOrder.Created, PurchaseOrder.Changed"),
        ("Test event flow",
         "ATO SaaS → trigger PO creation (Manage Schedules → Trigger ERP Document Creation)\n"
         "Verify:\n"
         "  BTP Event Mesh → message published\n"
         "  Integration Suite Monitor → iFlow COMPLETED\n"
         "  S4 ME23N → PO created with ATO fields\n"
         "  S4 → outbound event published back to ATO\n"
         "  ATO portal → PO number linked to specimen shipment"),
    ]
    for i,(a,d) in enumerate(steps,1):
        for row in step_row(i,a,d,TEAL): els.append(row)
    els.append(ok_box("✅  Phase 11 complete when ATO triggers PO in S4 and S4 notifies ATO of changes."))
    els.append(PageBreak())
    return els

# ── Phase 12 ──────────────────────────────────────────────────────────────────
def phase12():
    els=[]
    els.append(sec_hdr("12","End-to-End Validation Checklist",
                       "Run after all phases complete — covers ATO → S4 → eSign → Reauth",
                       GREEN_OK, SAP_DARK))
    els.append(sp(8))
    els.append(tbl(
        ["#","Validation","How","Expected Result"],
        [
            ["□ 1","Add-on installed","SAINT → LS_ADD_ON","Status = INSTALLED"],
            ["□ 2","84P activated","SPRO → GxP node visible, CHECK_ESIG_ACTIVE=TRUE","Both conditions met"],
            ["□ 3","VC_SRA_SOT configured","SE16N → VC_SRA_SOT → PURCHASE_ORDER row","Object + class names present"],
            ["□ 4","Callback class active","SE24 → ZCL_PO_REAUTH_CHECK → Active (blue)","Methods implemented and active"],
            ["□ 5","OData V4 extensibility","GET /PurchaseOrder/$metadata → TherapyType visible","ATO properties in metadata"],
            ["□ 6","ATO tables have data","SE16N → /ATO/S4_PO_HEADER_EXT after PO creation","Row with ATO field values"],
            ["□ 7","Change Doc records ATO fields","SE16N → CDPOS → TABNAME=/ATO/S4_PO_HEADER_EXT","Rows with VALUE_OLD/VALUE_NEW"],
            ["□ 8","Comm Arrangement active","Comm Arrangement → Test Connection → green","HTTP 200 from BTP"],
            ["□ 9","BTP object registered","BTP eSign Admin → PURCHASE_ORDER listed","Object with reason codes"],
            ["□ 10","Reauth dialog in ME21N","ME21N → change Therapy Type → Save → dialog appears","Password + reason code shown"],
            ["□ 11","Signature linked to CHANGENR","CDHDR CHANGENR matches BTP Signature ID","End-to-end audit trail"],
            ["□ 12","ATO event creates PO","ATO portal → trigger → PO created in S4","ME23N shows PO with ATO tab"],
            ["□ 13","S4 notifies ATO of change","ME22N change → Event Mesh → ATO portal updated","ATO shows changed value"],
            ["□ 14","Cancel flow works","ATO cancel → S4 PO item deletion indicator","ME23N item shows LOEKZ=X"],
        ],
        widths=[0.8*cm,5.5*cm,5.7*cm,5.5*cm]
    ))
    els.append(sp(8))

    els.append(Paragraph("Key Contacts for Each Phase", H2))
    els.append(tbl(
        ["Phase","Area","Contact","Email"],
        [
            ["1","Life Science Add-on install","SAP Cloud Operations","Via support ticket"],
            ["2","84P activation","SAP Cloud Operations / Basis","Via support ticket"],
            ["3","VC_SRA_SOT config","Yadesh Gupta (Framework)","ya.gupta@sap.com"],
            ["4","Callback class dev","PO LOB development team","Nils Hartmann"],
            ["5","OData V4 API extensibility","Nils Hartmann / Jiss","PO standard team"],
            ["6","ATO extension tables","Loring Wu / Allen Yuan","ATO dev team"],
            ["7","Change Doc + EINKBELEG","Allen Yuan + Jiss","ATO + PO standard"],
            ["8","Comm Arrangement / BTP","Swarnava Chatterjee","swarnava.chatterjee@sap.com"],
            ["9","BTP reason codes","Swarnava Chatterjee / Yadesh","eSignature + framework team"],
            ["10","ME21N BAdI integration","PO LOB dev team","Nils Hartmann"],
            ["11","Event Mesh / iFlow","Loring Wu / Viswanath Natesan","ATO integration team"],
        ],
        widths=[1.5*cm,4.5*cm,5*cm,6.5*cm]
    ))
    return els

# ── Build ─────────────────────────────────────────────────────────────────────
def build():
    doc=SimpleDocTemplate(
        OUTPUT,pagesize=A4,
        leftMargin=2*cm,rightMargin=2*cm,
        topMargin=2*cm,bottomMargin=2*cm,
        title="GxP Complete Setup Guide",
        author="SAP GxP Team",
    )
    story=[]
    story.extend(cover())
    story.extend(phase1())
    story.extend(phase2())
    story.extend(phase3())
    story.extend(phase4())
    story.extend(phase5())
    story.extend(phase6())
    story.extend(phase7())
    story.extend(phase8())
    story.extend(phase9())
    story.extend(phase10())
    story.extend(phase11())
    story.extend(phase12())

    def on_page(c,doc):
        c.saveState()
        c.setFont("Helvetica",7)
        c.setFillColor(colors.HexColor("#888888"))
        c.drawString(2*cm,1.2*cm,"GxP/ATO/eSignature — Complete End-to-End Setup Guide | 12 Phases")
        c.drawRightString(19.5*cm,1.2*cm,f"Page {doc.page}")
        c.setStrokeColor(colors.HexColor("#CCCCCC"))
        c.setLineWidth(0.4)
        c.line(2*cm,1.5*cm,19.5*cm,1.5*cm)
        c.restoreState()

    doc.build(story,onFirstPage=on_page,onLaterPages=on_page)
    print(f"PDF created: {OUTPUT}")

build()
