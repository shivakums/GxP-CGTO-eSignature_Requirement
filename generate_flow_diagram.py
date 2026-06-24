from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfgen import canvas as pdfcanvas

OUTPUT = r"C:\Users\I308878\GxP-CGTO-eSignature_Requirement\GxP_ATO_eSignature_Flow_Diagram.pdf"

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
ARROW_GREY    = colors.HexColor("#555555")
WHITE         = colors.white
BLACK         = colors.black
GREY_LIGHT    = colors.HexColor("#F5F5F5")
GREY_BORDER   = colors.HexColor("#CCCCCC")
GOLD          = colors.HexColor("#F0AB00")

W, H = A4  # 595 x 842 pts

def draw(c):
    # ── page background ───────────────────────────────────────────────────────
    c.setFillColor(colors.HexColor("#FAFAFA"))
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # ── header band ──────────────────────────────────────────────────────────
    c.setFillColor(SAP_DARK)
    c.rect(0, H - 60, W, 60, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(W/2, H - 28, "ATO / CGTO → S4 → Change Document → Reauthentication → eSignature")
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor("#AACCFF"))
    c.drawCentredString(W/2, H - 44, "GxP Compliance Flow  |  SAP S/4HANA + BTP  |  2026-06-24")

    # ── footer ────────────────────────────────────────────────────────────────
    c.setFillColor(GREY_BORDER)
    c.rect(0, 0, W, 22, fill=1, stroke=0)
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.HexColor("#555555"))
    c.drawString(20, 7, "GxP / CGTO / ATO / eSignature — Complete Flow Diagram")
    c.drawRightString(W - 20, 7, "github.com/shivakums/GxP-CGTO-eSignature_Requirement")

    # ─────────────────────────────────────────────────────────────────────────
    # LAYOUT  (all y from bottom of page)
    # We draw 6 swim-lane rows top → bottom
    # ─────────────────────────────────────────────────────────────────────────

    # ── helper functions ──────────────────────────────────────────────────────
    def box(x, y, w, h, fill_color, border_color, radius=6):
        c.setFillColor(fill_color)
        c.setStrokeColor(border_color)
        c.setLineWidth(1.2)
        c.roundRect(x, y, w, h, radius, fill=1, stroke=1)

    def label(x, y, w, h, lines, font="Helvetica", size=8, color=BLACK, bold_first=False):
        total = len(lines) * (size + 2)
        start_y = y + h/2 + total/2 - (size + 2)
        for i, line in enumerate(lines):
            c.setFont("Helvetica-Bold" if (bold_first and i == 0) else font, size)
            c.setFillColor(color)
            c.drawCentredString(x + w/2, start_y - i*(size+2.5), line)

    def arrow_down(x, y_top, length, label_text="", color=ARROW_GREY):
        c.setStrokeColor(color)
        c.setLineWidth(1.5)
        c.line(x, y_top, x, y_top - length)
        # arrowhead
        c.setFillColor(color)
        c.beginPath()
        p = c.beginPath()
        tip = y_top - length
        p.moveTo(x, tip)
        p.lineTo(x - 5, tip + 9)
        p.lineTo(x + 5, tip + 9)
        p.close()
        c.drawPath(p, fill=1, stroke=0)
        if label_text:
            c.setFont("Helvetica", 7)
            c.setFillColor(ARROW_GREY)
            c.drawCentredString(x + 22, y_top - length/2, label_text)

    def arrow_right(x_left, y, length, label_text="", color=ARROW_GREY):
        c.setStrokeColor(color)
        c.setLineWidth(1.5)
        c.line(x_left, y, x_left + length, y)
        p = c.beginPath()
        tip = x_left + length
        p.moveTo(tip, y)
        p.lineTo(tip - 9, y + 5)
        p.lineTo(tip - 9, y - 5)
        p.close()
        c.setFillColor(color)
        c.drawPath(p, fill=1, stroke=0)
        if label_text:
            c.setFont("Helvetica", 7)
            c.setFillColor(ARROW_GREY)
            c.drawCentredString(x_left + length/2, y + 5, label_text)

    def dashed_arrow_right(x_left, y, length, label_text="", color=ARROW_GREY):
        c.setStrokeColor(color)
        c.setLineWidth(1.2)
        c.setDash(4, 3)
        c.line(x_left, y, x_left + length, y)
        c.setDash()
        p = c.beginPath()
        tip = x_left + length
        p.moveTo(tip, y)
        p.lineTo(tip - 9, y + 5)
        p.lineTo(tip - 9, y - 5)
        p.close()
        c.setFillColor(color)
        c.drawPath(p, fill=1, stroke=0)
        if label_text:
            c.setFont("Helvetica-Oblique", 7)
            c.setFillColor(color)
            c.drawCentredString(x_left + length/2, y + 6, label_text)

    def step_badge(x, y, number, bg=SAP_BLUE):
        c.setFillColor(bg)
        c.circle(x, y, 9, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(x, y - 3, str(number))

    # ─────────────────────────────────────────────────────────────────────────
    # SWIM LANE BACKGROUND BANDS
    # ─────────────────────────────────────────────────────────────────────────
    lane_h   = 95
    lane_gap = 8
    top_y    = H - 70  # start just below header

    lanes = [
        ("BTP — ATO SaaS",               BTP_GREEN,   BTP_LIGHT),
        ("S4 — OData API",               S4_ORANGE,   S4_LIGHT),
        ("S4 — PO Tables",               SAP_BLUE,    SAP_LIGHT),
        ("S4 — Change Document",         SAP_DARK,    colors.HexColor("#EEF2F8")),
        ("S4 — Reauthentication",        REAUTH_PURPLE, REAUTH_LIGHT),
        ("BTP — eSignature SaaS",        ESIGN_TEAL,  ESIGN_LIGHT),
    ]

    lane_tops = []
    for i, (name, hdr_color, bg_color) in enumerate(lanes):
        y_lane = top_y - i * (lane_h + lane_gap)
        lane_tops.append(y_lane)

        # background
        c.setFillColor(bg_color)
        c.setStrokeColor(GREY_BORDER)
        c.setLineWidth(0.5)
        c.roundRect(14, y_lane - lane_h, W - 28, lane_h, 4, fill=1, stroke=1)

        # left label band
        c.setFillColor(hdr_color)
        c.roundRect(14, y_lane - lane_h, 68, lane_h, 4, fill=1, stroke=0)
        # fix right edge of label (overlap)
        c.setFillColor(hdr_color)
        c.rect(50, y_lane - lane_h, 32, lane_h, fill=1, stroke=0)

        # lane title — rotated
        c.saveState()
        cx = 14 + 34
        cy = y_lane - lane_h/2
        c.translate(cx, cy)
        c.rotate(90)
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(WHITE)
        c.drawCentredString(0, -3, name)
        c.restoreState()

    # ─────────────────────────────────────────────────────────────────────────
    # BOXES — one per lane, describing what happens
    # ─────────────────────────────────────────────────────────────────────────
    BX = 90   # box x start
    BW = 420  # box width
    BH = 68   # box height

    def lane_box(lane_idx, fill, border, lines, badge_num=None, badge_color=SAP_BLUE):
        y_top = lane_tops[lane_idx]
        bx = BX
        by = y_top - lane_h/2 - BH/2
        box(bx, by, BW, BH, fill, border)
        label(bx, by, BW, BH, lines, size=8, bold_first=True)
        if badge_num:
            step_badge(bx + 14, by + BH - 4, badge_num, badge_color)
        return bx, by, BW, BH

    # Lane 0 — ATO SaaS
    lane_box(0, BTP_LIGHT, BTP_GREEN,
        ["1. ATO SaaS — Clinical Demand Raised (BTP)",
         "Patient enrolled in Study CS-2026-001  |  Therapy: CELL_GENE",
         "Protocol: PROT-47B  |  Patient Ref: PAT-00123",
         "→ Orchestration engine creates PO request via OData API call to S4"],
        badge_num=1, badge_color=BTP_GREEN)

    # Lane 1 — OData API
    lane_box(1, S4_LIGHT, S4_ORANGE,
        ["2. S4 OData API — PurchaseOrder Service receives call",
         "Standard fields:  Vendor, Material, Quantity, Delivery Date",
         "ATO extension fields:  TherapyType, ClinicalStudy, ProtocolRef, PatientRef",
         "→ API routes standard fields to EKKO/EKPO, ATO fields to extension nodes"],
        badge_num=2, badge_color=S4_ORANGE)

    # Lane 2 — PO Tables
    lane_box(2, SAP_LIGHT, SAP_BLUE,
        ["3. S4 PO Tables Written",
         "EKKO  (PO Header — standard, unchanged)         EKPO  (PO Items — standard, unchanged)",
         "/ATO/S4_PO_HEADER_EXT  TherapyType · ClinicalStudy · ProtocolRef  (FK → EKKO.EBELN)",
         "/ATO/S4_PO_ITEM_EXT    TherapyType · PatientRef                   (FK → EKPO.EBELN+EBELP)"],
        badge_num=3, badge_color=SAP_BLUE)

    # Lane 3 — Change Document
    lane_box(3, colors.HexColor("#EEF2F8"), SAP_DARK,
        ["4. Change Document Framework Fires  (CHANGEDOCUMENT_CLOSE)",
         "CDHDR:  OBJECTCLAS=EINKBELEG  |  OBJECTID=4500000123  |  USERNAME=I308878  |  UDATE/UTIME",
         "CDPOS:  TABNAME=/ATO/S4_PO_HEADER_EXT  |  FNAME=THERAPY_TYPE  |  VALUE_OLD=''  |  VALUE_NEW=CELL_GENE",
         "→ Verified working for all PO fields including ATO extension fields  (2608 ✓)"],
        badge_num=4, badge_color=SAP_DARK)

    # Lane 4 — Reauthentication
    lane_box(4, REAUTH_LIGHT, REAUTH_PURPLE,
        ["5. Reauthentication Framework — Relevancy Check Callback",
         "ZCL_PO_REAUTH→RELEVANCY_CHECK reads S-table VC_SRA_SOT",
         "Checks: THERAPY_TYPE changed?  YES → returns ABAP_TRUE  → LUW PAUSED",
         "→ Dialog shown: Password re-entry + Reason Code  (e.g. Clinical Protocol Update)"],
        badge_num=5, badge_color=REAUTH_PURPLE)

    # Lane 5 — eSignature SaaS
    lane_box(5, ESIGN_LIGHT, ESIGN_TEAL,
        ["6. BTP eSignature SaaS — Signature Captured",
         "Validates re-entered password (NOT session token)  |  Creates Signature Record",
         "SIG-ID · User I308878 · Timestamp · Reason Code · Credential hash",
         "→ Signature ID linked to CHANGENR in CDHDR  |  COMMIT WORK  |  ATO notified via Event Mesh"],
        badge_num=6, badge_color=ESIGN_TEAL)

    # ─────────────────────────────────────────────────────────────────────────
    # ARROWS between lanes
    # ─────────────────────────────────────────────────────────────────────────
    arrow_cx = BX + BW/2  # center x for vertical arrows

    for i in range(5):
        y_from = lane_tops[i] - lane_h + 2
        y_to   = lane_tops[i+1] + 2
        gap    = y_from - y_to

        labels_map = {
            0: "OData API call",
            1: "Write tables",
            2: "CD Framework fires",
            3: "Relevancy check → ABAP_TRUE",
            4: "REQUEST_REAUTH API",
        }
        arrow_down(arrow_cx, y_from, gap - 4, labels_map.get(i,""), color=SAP_BLUE)

    # ─────────────────────────────────────────────────────────────────────────
    # RETURN ARROW — Event Mesh back to ATO (right side)
    # ─────────────────────────────────────────────────────────────────────────
    rx = BX + BW + 8
    y_esign_mid = lane_tops[5] - lane_h/2
    y_ato_mid   = lane_tops[0] - lane_h/2

    c.setStrokeColor(BTP_GREEN)
    c.setLineWidth(1.5)
    c.setDash(5, 3)
    # vertical line on right
    c.line(rx + 18, y_esign_mid, rx + 18, y_ato_mid)
    c.setDash()
    # arrowhead at top
    p = c.beginPath()
    p.moveTo(rx + 18, y_ato_mid)
    p.lineTo(rx + 13, y_ato_mid - 10)
    p.lineTo(rx + 23, y_ato_mid - 10)
    p.close()
    c.setFillColor(BTP_GREEN)
    c.drawPath(p, fill=1, stroke=0)

    # label on right arrow
    c.saveState()
    c.translate(rx + 32, (y_esign_mid + y_ato_mid)/2)
    c.rotate(90)
    c.setFont("Helvetica-Oblique", 7)
    c.setFillColor(BTP_GREEN)
    c.drawCentredString(0, 0, "Event Mesh → iFlow → ATO notified of PO change")
    c.restoreState()

    # ─────────────────────────────────────────────────────────────────────────
    # LEGEND
    # ─────────────────────────────────────────────────────────────────────────
    leg_y = 30
    leg_x = 14
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(BLACK)
    c.drawString(leg_x, leg_y, "Legend:")
    items = [
        (BTP_GREEN,    "BTP / ATO SaaS"),
        (S4_ORANGE,    "S4 OData API"),
        (SAP_BLUE,     "S4 PO Tables"),
        (SAP_DARK,     "Change Document"),
        (REAUTH_PURPLE,"Reauthentication"),
        (ESIGN_TEAL,   "eSignature SaaS"),
    ]
    lx = leg_x + 48
    for col, txt in items:
        c.setFillColor(col)
        c.roundRect(lx, leg_y - 1, 10, 10, 2, fill=1, stroke=0)
        c.setFillColor(BLACK)
        c.setFont("Helvetica", 7)
        c.drawString(lx + 13, leg_y + 1, txt)
        lx += 80

    # ─────────────────────────────────────────────────────────────────────────
    # CANCEL PATH note
    # ─────────────────────────────────────────────────────────────────────────
    note_x = BX + BW + 45
    note_y = lane_tops[4] - lane_h/2 - 14
    c.setFillColor(colors.HexColor("#FFF0F0"))
    c.setStrokeColor(colors.HexColor("#BB0000"))
    c.setLineWidth(0.8)
    c.roundRect(note_x - 4, note_y - 8, 88, 30, 4, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(colors.HexColor("#BB0000"))
    c.drawString(note_x, note_y + 10, "⚠ User Cancels:")
    c.setFont("Helvetica", 7)
    c.setFillColor(BLACK)
    c.drawString(note_x, note_y, "Save ABORTED")
    c.drawString(note_x, note_y - 9, "Full ROLLBACK")

# ── Build PDF ────────────────────────────────────────────────────────────────
c = pdfcanvas.Canvas(OUTPUT, pagesize=A4)
draw(c)
c.showPage()
c.save()
print(f"Flow diagram PDF created: {OUTPUT}")
