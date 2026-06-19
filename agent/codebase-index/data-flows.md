# Data Flows — GxP / CGTO / eSignature

---

## Flow 1 — ATO Creates PO in S4 (BTP → S4)

```
ATO SaaS (BTP) needs to create a PO in S4
        ↓
OData API call: PurchaseOrder API (standard S4 endpoint)
  + Industry extension fields (CGTO/ATO specific)
        ↓
S4 processes PO creation
  EKKO + EKPO written
  Industry Object Extension node written (CGTO fields)
        ↓
Change Document created (standard)
        ↓
Outbound event published to Event Mesh (S4 schema)
        ↓
iFlow transforms schema (S4 → BTP)
        ↓
ATO SaaS receives PO creation confirmation
```

---

## Flow 2 — PO Changed in S4 → ATO Notified (S4 → BTP)

```
User changes PO in ME21N/ME22N OR ATO triggers change
        ↓
EKKO/EKPO updated
Industry extension fields updated if applicable
        ↓
Change Document records the change
        ↓
Outbound event published to Event Mesh
  Payload: standard fields + CGTO extension fields that changed
        ↓
iFlow subscriber receives event, maps schema
        ↓
ATO SaaS notified of PO change in real-time
        ↓
ATO reacts (e.g. update therapy schedule, notify clinic)
```

---

## Flow 3 — eSignature on PO Save in ME21N (Planned 2702)

```
User saves PO in ME21N
        ↓
Standard PO processing: EKKO/EKPO written
        ↓
Change Document created (prerequisite — done 2608)
        ↓
eSignature trigger (new — 2702)
  → Call BTP eSignature SaaS via Communication Arrangement
  → Show signature dialog to user in ME21N
        ↓
User authenticates and signs
  (Method: SAP password / PIN / external IdP)
        ↓
Signature captured, linked to Change Document
  → Stored in tamper-proof audit log on BTP
        ↓
GxP audit trail complete:
  WHO (eSignature) + WHAT changed (Change Document)
  + WHEN (timestamp) + WHY (optional reason)
```

---

## Key Tables and Services

| Object | System | Type | Description |
|---|---|---|---|
| EKKO | S4 | Table | PO Header (standard) |
| EKPO | S4 | Table | PO Item (standard) |
| /ATO/S4_PO_HDR_EXT | S4 | Extension node | CGTO header fields |
| /ATO/S4_PO_ITM_EXT | S4 | Extension node | CGTO item fields |
| Change Document | S4 | Framework | Audit trail of field changes |
| Event Mesh | BTP | Service | Async event bus |
| iFlow | Integration Suite | Middleware | Schema mapping |
| eSignature | BTP | SaaS Service | Digital signature capture |
