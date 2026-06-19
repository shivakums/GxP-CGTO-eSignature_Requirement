# GxP / CGTO / eSignature — Domain Knowledge

---

## 1. GxP — What It Means

GxP is a collection of quality guidelines for regulated industries:

| Abbreviation | Full Name | Industry |
|---|---|---|
| GMP | Good Manufacturing Practice | Pharma, Biotech, Medical Devices |
| GCP | Good Clinical Practice | Clinical Trials |
| GLP | Good Laboratory Practice | Research Labs |
| GDP | Good Distribution Practice | Drug Distribution |

**Why it matters for SAP:** Any SAP system used by a GxP-regulated company must meet data
integrity, audit trail, and electronic signature requirements. SAP S/4HANA was not GxP-ready
in 2025 — this is the gap being closed in 2026/2027.

---

## 2. Key Regulatory Standards

| Standard | Authority | Relevance |
|---|---|---|
| 21 CFR Part 11 | FDA (US) | Electronic records and signatures |
| EU Annex 11 | EMA (Europe) | Computerised systems in GxP |
| ICH Q10 | International | Pharmaceutical Quality System |

21 CFR Part 11 requires:
- **Audit trail** of all changes to regulated records
- **Electronic signatures** that are attributable to the signing individual
- **Change tracking** with timestamp, user ID, reason for change

---

## 3. CGTO / ATO — Product Details

### 3.1 Name History

| When | Name | Acronym |
|---|---|---|
| Original | Cell and Gene Therapy Orchestration | CGTO |
| May 2026 (renamed) | Advanced Therapy Orchestration | ATO |

### 3.2 What ATO Orchestrates

ATO is an end-to-end supply chain orchestration platform for advanced therapies:

| Therapy Type | Description |
|---|---|
| Cell & Gene Therapy | Patient-specific manufacturing |
| Plasma Therapy | Plasma-derived medicines |
| Advanced Medical Devices | Regulated medical equipment |
| Surgical Therapy | Surgical supply chain |
| Radio Ligand Therapy (RLT) | Isotopes for PET cancer treatment |

### 3.3 ATO Hybrid Architecture

```
BTP (SaaS)                S/4HANA
┌──────────────┐          ┌─────────────────────────────────┐
│ ATO SaaS     │◄────────►│ Life Science Add-on             │
│ Multi-tenant │  Events  │ (Private Cloud only)            │
│              │  OData   │ Components: ATO, SI, CSAI,      │
│ - Orchestrate│          │            CSM, BRH             │
│ - Track      │          └─────────────────────────────────┘
│ - Monitor    │          ┌─────────────────────────────────┐
└──────────────┘          │ Standard S/4HANA (Public Cloud) │
                          │ Industry Object Extensions      │
                          │ PO, SO, Process Order etc.      │
                          └─────────────────────────────────┘
```

---

## 4. eSignature — Concept

### 4.1 What is SAP eSignature on BTP?

A reusable SaaS service already available on BTP that:
- Captures electronic signatures from SAP users
- Links signatures to change documents (audit trail)
- Is configurable per business object and field
- Supports multiple authentication methods (password, PIN, biometric)
- Stores signatures in tamper-proof audit log

### 4.2 eSignature + Change Document — The Relationship

```
Change Document = WHAT changed (field, old value, new value, time, user)
eSignature     = WHO approved it (signature binding the user to the change)

Together = Full GxP audit trail for PO creation/change
```

The eSignature framework calls the Change Document after PO save and attaches
a signature to the change document record. **This is why Change Document must
work before eSignature can be enabled.**

### 4.3 Which PO Applications Are In Scope

| Application | Technology | eSignature Phase |
|---|---|---|
| ME21N / ME22N | Web GUI (ABAP) | Phase 1 — 2702 |
| Manage PO App | BOF / Fiori (modern) | Deferred — post modernisation |
| New Modern PO App | RAP / Fiori (future) | Future target |

**Reason for ME21N first:** Manage PO app has feature parity gaps vs ME21N.
Modernisation is underway. Investing in BOF app eSignature is wasteful when
a new UI is coming. ME21N serves current regulated users in the interim.

---

## 5. CGTO Field Extension — What Fields Are Added

Industry-specific fields added to PO via Industry Object Extension:

### Header Level (Extension on EKKO)

| Field | Description | Use Case |
|---|---|---|
| Therapy Type | Type of therapy (Cell, Gene, Plasma etc.) | Supply chain routing |
| Clinical Study | Reference to clinical study | Regulatory traceability |
| Protocol Reference | Clinical protocol reference | GCP compliance |

### Item Level (Extension on EKPO)

| Field | Description | Use Case |
|---|---|---|
| Therapy Type | Per-item therapy classification | Item-level routing |
| Patient Reference | Anonymous patient ID (for autologous therapies) | Patient-specific supply |

---

## 6. Integration Decisions Log

| Decision | Rationale | Date |
|---|---|---|
| Use Industry Object Extension (not EKKO/EKPO append) | North Star architecture governance, no pollution of standard tables | 2025/2026 |
| ME21N as first eSignature target (not Manage PO app) | Manage PO app modernisation in progress, feature parity gaps exist | 2025/2026 |
| Phased approach: CD first, then eSignature | eSignature built on top of Change Document | 2025/2026 |
| iFlow as middleware for event schema mapping | BTP and S4 have different event schemas | 2026 |
| CGTO renamed to ATO (Advanced Therapy Orchestration) | Expanded scope beyond cell & gene therapy | May 2026 |

---

## 7. Open Items and Future Work

| Item | Status | Target |
|---|---|---|
| eSignature in ME21N | Planned | 2702 |
| CGTO/ATO field extension + OData exposure | Development started | 2702 |
| Outbound events S4→BTP for PO changes | Development started | 2702 |
| eSignature in Manage PO App (BOF) | Deferred | Post modernisation |
| eSignature in new modern PO App (RAP) | Future | Post modernisation |
| Other LOBs eSignature (SO etc.) | Parallel teams | 2702 |

---

## 8. Teams and Contacts Quick Reference

| Team | Contact | Topic |
|---|---|---|
| eSignature (Work Stream 1) | Swarnava Chatterjee | eSignature integration |
| eSignature colleagues | Yadish, Navin Kumar | eSignature |
| CGTO/ATO PM+Arch | Satish Kumar (Meenakshisundaram) | ATO/CGTO scope |
| CGTO/ATO Architecture | Viswanath Natesan | ATO integration |
| ATO Development | Loring Wu | ATO S4 dev |
| PO Product | Nils Hartmann | Purchase Order ownership |
| Suite Architecture | Felix Vente | North Star governance |
| Engineering (China) | via Satish/Viswanath | ATO S4 development |
