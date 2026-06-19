# GxP / CGTO / eSignature — Architecture Flow Diagrams

---

## 1. Overall Integration Architecture

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    BTP (SAP Business Technology Platform)                    │
│                                                                              │
│  ┌─────────────────────────────────────┐  ┌───────────────────────────────┐ │
│  │  ATO SaaS Application               │  │  eSignature Reusable Service  │ │
│  │  (Advanced Therapy Orchestration)   │  │                               │ │
│  │  Multi-tenant SaaS                  │  │  Already available on BTP     │ │
│  │                                     │  │  21 CFR Part 11 compliant     │ │
│  │  Creates / changes POs via API      │  │  Linked to Change Documents   │ │
│  │  Publishes events on PO changes     │  │                               │ │
│  │  Industry fields:                   │  └───────────────┬───────────────┘ │
│  │   - Therapy type                    │                  │                 │
│  │   - Clinical study ref              │                  │ integration      │
│  │   - Protocol                        │                  │ (planned 2702)   │
│  └──────────────┬──────────────────────┘                  │                 │
│                 │  publish / subscribe events              │                 │
│  ┌──────────────▼──────────────────────────────────────────────────────┐    │
│  │  Event Mesh                                                         │    │
│  └──────────────┬──────────────────────────────────────────────────────┘    │
│                 │                                                            │
│  ┌──────────────▼──────────────────────────────────────────────────────┐    │
│  │  Integration Suite — iFlow                                          │    │
│  │  Schema mapping: BTP event schema ↔ S4 event schema                │    │
│  │  (Both sides have different schemas — iFlow bridges the gap)        │    │
│  └──────────────┬──────────────────────────────────────────────────────┘    │
└─────────────────┼────────────────────────────────────────────────────────────┘
                  │  Inbound / Outbound events + OData API
                  │
┌─────────────────▼────────────────────────────────────────────────────────────┐
│             SAP S/4HANA (Public Cloud or Private Cloud)                      │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  PURCHASE ORDER — WORK STREAM 1: eSignature                          │   │
│  │                                                                       │   │
│  │  ME21N (Create PO — Web GUI)                                          │   │
│  │  ME22N (Change PO — Web GUI)                                          │   │
│  │         │                                                             │   │
│  │         ▼ On PO Save                                                  │   │
│  │  Change Document Framework  ← prerequisite (verified 2608 ✓)         │   │
│  │         │                                                             │   │
│  │         ▼                                                             │   │
│  │  eSignature Trigger (planned 2702)                                    │   │
│  │  → calls BTP eSignature Service                                       │   │
│  │  → captures user signature                                            │   │
│  │  → links signature to change document                                 │   │
│  │                                                                       │   │
│  │  Manage PO App (BOF/Fiori) ← DEFERRED — pending modernisation         │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  PURCHASE ORDER — WORK STREAM 3: CGTO / ATO Field Extension          │   │
│  │                                                                       │   │
│  │  EKKO (PO Header)                                                     │   │
│  │  EKPO (PO Item)                                                       │   │
│  │         │                                                             │   │
│  │         ▼ Industry Object Extension (NOT direct table append)         │   │
│  │  Extension Node — CGTO/ATO fields                                     │   │
│  │  → Therapy type                                                       │   │
│  │  → Clinical study reference                                           │   │
│  │  → Protocol reference                                                 │   │
│  │         │                                                             │   │
│  │         ▼ Outbound events on PO change                                │   │
│  │  Event Mesh → iFlow → ATO SaaS                                        │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  LIFE SCIENCE ADD-ON (Private Cloud only)                             │   │
│  │  ATO + SI + CSAI + CSM + BRH combined add-on                         │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. eSignature Integration Flow

```
User opens ME21N to create a Purchase Order
        │
        ▼
Fills in PO details + relevant fields
        │
        ▼
Clicks SAVE
        │
        ▼  SAP standard PO save processing
EKKO / EKPO written
        │
        ▼
Change Document Framework fires
  Records: which fields changed, old value, new value, timestamp, user
        │
        ▼  (planned 2702)
eSignature trigger
  → Call BTP eSignature SaaS service
  → Show signature dialog to user
  → User signs (PIN/biometric/password based on config)
  → Signature captured + linked to change document
        │
        ▼
Audit trail complete:
  Change Document + eSignature = GxP-compliant PO save
```

### Prerequisite Chain

```
GxP Compliance for PO
        │
        ├── STEP 1: Change Document Enablement
        │          Verify CD framework works for all PO fields
        │          Status: COMPLETED in 2608 ✓
        │
        └── STEP 2: eSignature Integration (built ON TOP of CD)
                   Connect BTP eSignature service to ME21N
                   Status: PLANNED for 2702
```

---

## 3. CGTO / ATO Integration Flow

```
Direction 1 — ATO SaaS creates/changes PO in S4:

ATO SaaS (BTP)
        │ OData API call
        ▼
S4 OData Service (PurchaseOrder API)
        │
        ▼
EKKO / EKPO written + Industry Extension fields
        │
        ▼
Outbound event fired to Event Mesh
        │
        ▼ iFlow (schema mapping)
ATO SaaS notified of PO creation confirmation

Direction 2 — S4 PO change triggers outbound event to ATO:

ME21N / ME22N — PO saved
        │
        ▼
Change Document + standard PO change event
        │
        ▼
Outbound event published to Event Mesh
  (standard PO fields + CGTO extension fields)
        │
        ▼ iFlow (schema mapping BTP→S4 schema)
ATO SaaS subscriber account receives event
        │
        ▼
ATO reacts to PO change in real-time
```

---

## 4. Industry Object Extension Pattern

```
WRONG approach (explicitly rejected):
  EKKO ← append field ZZTHERAPY_TYPE   ✗
  EKPO ← append field ZZPROTOCOL       ✗
  Pollutes standard tables, hard to maintain

CORRECT approach (approved by Suite Architecture):
  EKKO (standard — unchanged)
      │
      │ Industry Object Extension node
      ▼
  /ATO/S4_PO_HEADER_EXT (extension node)
  ┌──────────────────────────────────────┐
  │ Key: EBELN (FK → EKKO)               │
  │ THERAPY_TYPE    CHAR 20              │
  │ CLINICAL_STUDY  CHAR 40             │
  │ PROTOCOL_REF    CHAR 40             │
  └──────────────────────────────────────┘
  Accessed via: Industry Object Extension API
  Exposed via: OData extension of PurchaseOrder entity

  EKPO (standard — unchanged)
      │
      │ Industry Object Extension node
      ▼
  /ATO/S4_PO_ITEM_EXT (extension node)
  ┌──────────────────────────────────────┐
  │ Key: EBELN + EBELP (FK → EKPO)       │
  │ THERAPY_TYPE    CHAR 20              │
  │ PATIENT_REF     CHAR 40             │
  └──────────────────────────────────────┘
```

---

## 5. Delivery Timeline Diagram

```
2025          2026 (2602)    2026 (2608)      2027 (2702)
─────────────────────────────────────────────────────────────►

GxP NOT        Discussions    Change Doc       eSignature
enabled        started        verified ✓       in ME21N ─────►

                              CGTO/ATO         CGTO/ATO
                              POC done         Enablement ───►
                              Dev started
```
