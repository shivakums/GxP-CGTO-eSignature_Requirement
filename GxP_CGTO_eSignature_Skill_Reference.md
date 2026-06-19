# GxP / CGTO / eSignature — Skill Reference Guide

**Project:** GxP Compliance, CGTO/ATO Integration, eSignature for Purchase Orders
**Skill Name:** gxp-cgto-esignature-expert
**Location:** `C:\Users\I308878\GxP-CGTO-eSignature_Requirement`
**Date:** 2026-06-19
**Version:** 1.0
**Sources:** GxP Handover (Lift & Shift), CGTO PO Alignment meeting documents

---

## 1. What This Is About — Three Topics in One

This skill covers three interconnected topics all affecting the **Purchase Order** in SAP S/4HANA:

| Topic | What It Is | Status |
|---|---|---|
| **GxP** | Life Science compliance framework requiring audit trails + eSignature | Enablement started 2026 |
| **eSignature** | Digital signature captured on PO save — linked to Change Document | Planned 2702 |
| **CGTO / ATO** | Life Science industry fields added to PO (Therapy, Study, Protocol) | Development started 2026 |

---

## 2. GxP — The Compliance Context

**GxP** = Good x Practice — quality standards for regulated Life Science industries.

| Standard | Authority | Requirement |
|---|---|---|
| 21 CFR Part 11 | FDA (USA) | Electronic records + signatures |
| EU Annex 11 | EMA (Europe) | Computerised systems |

**What GxP requires for SAP PO:**
- Change Document tracking (who changed what, when, old/new value)
- Electronic Signature on regulated changes
- Tamper-proof audit log

**In 2025:** GxP was NOT enabled in SAP S/4HANA Cloud.
**In 2608:** Change Document for PO verified working. ✓
**In 2702:** eSignature integration in ME21N planned.

---

## 3. CGTO / ATO — Who and What

**CGTO** (Cell & Gene Therapy Orchestration) → renamed **ATO** (Advanced Therapy Orchestration) in May 2026.

ATO is a **hybrid product** — SaaS on BTP + Life Science Add-on for S/4HANA Private Cloud.

ATO orchestrates supply chains for:

| Therapy | Example |
|---|---|
| Cell & Gene Therapy | CAR-T therapy, gene editing |
| Plasma Therapy | Plasma-derived medicines |
| Advanced Medical Devices | Regulated devices |
| Surgical Therapy | Surgical supply chain |
| Radio Ligand Therapy | Isotopes for PET cancer |

**Life Science Add-on** (Private Cloud) = ATO + SI + CSAI + CSM + BRH combined.

---

## 4. Skill Structure

```
GxP-CGTO-eSignature_Requirement/
├── Claude.md                                  ← Skill definition
│     Trigger words, architecture,
│     work streams, key decisions,
│     contacts, quick reference
│
├── repos.yaml                                 ← Source documents
│
└── agent/
    ├── knowledge/
    │   ├── architecture/
    │   │   └── gxp-esig-architecture.md       ← Full architecture diagrams
    │   │         BTP↔S4 integration layout
    │   │         eSignature flow
    │   │         CGTO field extension pattern
    │   │         Delivery timeline
    │   ├── domain/
    │   │   └── gxp-domain.md                  ← GxP/CGTO/ATO domain concepts
    │   │         Regulatory standards
    │   │         ATO product details
    │   │         eSignature concept
    │   │         Integration decisions log
    │   └── product/
    │       └── esignature-integration.md      ← eSignature product details
    └── codebase-index/
        ├── codebase-overview.md               ← Object index and tech stack
        ├── business-rules.md                  ← 6 critical rules
        └── data-flows.md                      ← 3 integration flows
```

---

## 5. Architecture Overview

### Two Work Streams for Purchase Order

```
Work Stream 1: eSignature
─────────────────────────
ME21N Save
    ↓
Change Document ← prerequisite (done 2608 ✓)
    ↓
eSignature trigger (2702)
    ↓ calls
BTP eSignature SaaS
    ↓
Signature captured + linked to Change Document
    ↓
GxP audit trail complete

Work Stream 3: CGTO / ATO Field Extension
──────────────────────────────────────────
EKKO / EKPO (standard — NOT modified directly)
    │ Industry Object Extension
    ▼
/ATO/S4_PO_HEADER_EXT  → Therapy, Study, Protocol
/ATO/S4_PO_ITEM_EXT    → Therapy, Patient reference
    │
    ▼
OData API extension (PurchaseOrder entity)
    │
    ▼ Outbound events on PO change
Event Mesh → iFlow → ATO SaaS
```

### Full Integration Landscape

```
BTP                               S/4HANA
┌──────────────────────┐         ┌──────────────────────────────┐
│ ATO SaaS (ATO)        │◄───────►│ EKKO + EKPO                  │
│ eSignature Service    │ Events  │ Industry Object Extensions   │
│ Event Mesh            │ OData   │ ME21N / ME22N                │
│ iFlow (schema map)    │         │ Change Document              │
└──────────────────────┘         └──────────────────────────────┘
```

---

## 6. Industry Object Extension Pattern

**Decision:** CGTO/ATO fields are NOT appended directly to EKKO/EKPO.

| Wrong | Correct |
|---|---|
| EKKO ← append ZZTHERAPY | Industry Object Extension node on EKKO |
| Pollutes standard table | Clean separation from standard |
| Not approved for public cloud | Approved by Suite Architecture (North Star) |

Extension nodes:
- `/ATO/S4_PO_HEADER_EXT` — header fields (linked to EKKO via EBELN)
- `/ATO/S4_PO_ITEM_EXT` — item fields (linked to EKPO via EBELN+EBELP)

---

## 7. Key Business Rules

| # | Rule | Why |
|---|---|---|
| 1 | NEVER append CGTO fields directly to EKKO/EKPO | North Star governance — use Industry Object Extension |
| 2 | eSignature REQUIRES Change Document working first | eSignature attaches to Change Document |
| 3 | ME21N is phase 1 for eSignature — Manage PO App is deferred | BOF app modernisation in progress |
| 4 | iFlow handles schema mapping BTP↔S4 | Different event schemas on each side |
| 5 | Public cloud extensions need Suite Architecture review | North Star governance (Felix Vente) |
| 6 | CGTO = ATO (renamed May 2026) | Expanded scope to multi-modal therapies |

---

## 8. Delivery Timeline

| Release | What Was Done | Status |
|---|---|---|
| 2025 | GxP not enabled in S/4HANA | — |
| 2602 | Discussions started, POCs | Done |
| 2608 | Change Document for PO verified | ✓ Done |
| 2702 | eSignature in ME21N + CGTO enablement | Planned |
| Future | eSignature in modernised PO app | Deferred |

---

## 9. Key Contacts

| Name | Role | Topic |
|---|---|---|
| Swarnava Chatterjee | eSignature main contact | Work Stream 1 |
| Satish Kumar (Meenakshisundaram) | ATO/CGTO PM + Architecture | Work Stream 3 |
| Viswanath Natesan | ATO Architecture | Work Stream 3 |
| Nils Hartmann | PO Product Owner | Both |
| Loring Wu | ATO Development Manager | Work Stream 3 |
| Felix Vente | Suite Architecture — North Star | Governance |

---

## 10. What Makes It Extensible

### Adding New CGTO/ATO Fields

1. Add field to Industry Object Extension node (not EKKO/EKPO directly)
2. Expose via OData extension of PurchaseOrder entity
3. Add to outbound event payload for S4→BTP

### Adding New eSignature Scope (new app/object)

1. Confirm Change Document works for that object
2. Add eSignature trigger point in the save flow
3. Configure which fields require signature

### Adding New Knowledge Documents

Place in:
- `agent/knowledge/domain/` — new domain rules, regulatory updates
- `agent/knowledge/product/` — ATO product updates, eSignature updates
- `agent/knowledge/architecture/` — new integration diagrams
- Update `repos.yaml` source_documents list

---

*Skill created: 2026-06-19*
*Sources: GxP Handover (Lift & Shift team), CGTO PO Alignment meeting*
*Skill file: C:\Users\I308878\GxP-CGTO-eSignature_Requirement\Claude.md*
