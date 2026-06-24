# Reauthentication Reuse Framework — Integration Guide

**Source:** Reauthentication Framework meeting — 2026-06-18
**Speakers:** Yadesh Gupta (Framework Architect), Prabir Kumar Mallick (Dev Lead),
Swarnava Chatterjee (eSignature), Niranjan Raju, Loring Wu (ATO)
**Document:** Reauthentication Reuse Framework — Application Integration Guide

---

## 1. What Is the Reauthentication Framework?

A **platform-level reusable framework** built for SAP S/4HANA that any LOB application
can integrate with to enforce GxP-compliant reauthentication (eSignature) when a user
makes regulated changes to a business object.

The goal: **one common UX and one common platform layer** — every S4 application that
needs GxP reauthentication integrates to this single framework instead of building
its own signature flow.

---

## 2. How It Works — Core Flow

```
User opens a regulated business object (e.g. Purchase Order in ME21N)
        │
        ▼
User makes changes to the object
        │
        ▼
User triggers Save / Action button
        │
        ▼  BEFORE save is committed
Application calls: Relevancy Check (callback class)
        │
        ├── Returns FALSE → no regulated field changed → SKIP reauthentication
        │
        └── Returns TRUE  → regulated field changed → TRIGGER reauthentication
                │
                ▼
        Reauthentication dialog shown to user
        User enters: Password / PIN / Biometric + Reason Code
                │
                ▼
        BTP eSignature SaaS validates credentials
                │
                ▼
        Signature captured and linked to Change Document
                │
                ▼
        Save proceeds — GxP audit trail complete
```

---

## 3. The 4 APIs Applications Must Call

| API | When to Use | Technology |
|---|---|---|
| `REQUEST_REAUTH` | Trigger reauthentication from OData/HCP GUI | OData + HCP GUI only |
| `REQUEST_REAUTH` (lib) | For all other app types — uses internal library | All technologies |
| `VALIDATE_RESULT` | Check if reauthentication succeeded | Irrespective of technology |
| `CHECK_ESIG_ACTIVE` | Check if eSignature is active in the system — returns true/false | Any |

> **API Rule:** `REQUEST_REAUTH` has two variants — use the OData/HCP GUI version
> only for those specific UI technologies. For all other cases use the library version.

---

## 4. The Relevancy Check — Most Critical Method

The **Relevancy Check callback** is the most important method an application implements.
It decides whether reauthentication is triggered or not.

```
Application implements: Relevancy Check callback class
        │
        ├── INPUT:  current state of the business object
        │           application identifies which fields changed
        │
        ├── LOGIC:  compare changed fields against configured regulated fields
        │           (configuration maintained in SPRO / S-tables)
        │
        ├── OUTPUT: ABAP_TRUE  → reauthentication required
        │           ABAP_FALSE → skip (nothing regulated changed)
        │
        └── CRITICAL: if this returns FALSE in error → reauthentication silently skipped
                      if this raises exception → reauthentication blocked
```

> **Warning:** If the Relevancy Check returns `ABAP_FALSE` due to a bug or error,
> the framework treats it as "nothing changed" and skips reauthentication entirely.
> The application team is responsible for identifying which fields changed — the
> framework does NOT track field changes automatically.

---

## 5. Configuration Model — 3 Levels

```
Level 1 — S-Tables (S4 backend — delivered via transport / 84P scope item)
  ─────────────────────────────────────────────────────────────────────
  Reauthentication Object definition
  ├── Object name (e.g. "PROCESS_ORDER", "PURCHASE_ORDER")
  ├── Reauthentication class name (callback class)
  ├── Authorization class name
  └── Node types (entity → table mapping)
       ├── PROCESS_ORDER_HEADER → table ZPO_HEADER
       ├── PROCESS_ORDER_ITEM   → table ZPO_ITEM
       └── ...

Level 2 — Field Configuration (S4 backend — delivered by LOB as part of 84P)
  ─────────────────────────────────────────────────────────────────────
  Per reauthentication object → per node type → configured field names
  These are the fields that TRIGGER reauthentication when changed
  Customer can fine-tune which fields are regulated

Level 3 — Reason Codes (BTP — provisioned automatically when scope item activated)
  ─────────────────────────────────────────────────────────────────────
  Same object name defined in BTP
  Reason codes attached to that object type
  Customer can define custom reason codes per object
  Only reason codes configured for that object appear in the dropdown
```

---

## 6. Reason Code Behaviour

- Reason codes are **freely definable per business object type**
- Defined in **BTP** (not in S4) — content loaded automatically on provisioning
- Only reason codes configured for the **specific business object** appear in the dropdown
- LOB teams can ship **default/suggested reason codes** via BTP content delivery
- Customer can extend with custom reason codes

---

## 7. Authorization Check

Two scenarios:

| Scenario | Authorization Handling |
|---|---|
| Create / Change (CRUD operations) | Authorization check done **inside the Relevancy Check callback** — application is responsible |
| Display mode with Reauthentication lock button | Framework provides a **separate display class** — no event fired, different check |

> Authorization for create/change is expected to happen in the Relevancy Check
> callback — the framework does not perform a separate authorization check.
> For display-mode reauthentication, use the dedicated display class.

---

## 8. Mass Update / Bulk Operations

| Scenario | Behaviour |
|---|---|
| User selects multiple objects and changes a field | Single reauthentication popup — user signs once — signature applied to all objects |
| Background job (system user / technical user) | **Excluded from reauthentication** — GxP requirement: automated system jobs do not need signature |
| Background job triggered by user from Fiori UI | Reauthentication collected **once at trigger point** (when user clicks button) — signature covers all resulting objects |
| Scheduled background job | Not in scope — must be run by system/technical user |

> Key insight from Swarnava Chatterjee (eSignature expert): GxP requirement says
> **automated system-context jobs are excluded**. Only user-context actions require
> reauthentication. For background jobs triggered by a user from UI — collect signature
> once at trigger time, apply to all resulting objects.

---

## 9. Action/Button-Based Reauthentication (Not Field-Change Based)

Some applications need reauthentication on **business actions** (e.g. Release Order)
rather than on field value changes. Two approaches:

| Approach | When to Use | Implementation |
|---|---|---|
| Field-change based (standard) | User edits fields in edit mode and saves | Configure regulated fields in S-tables — callback checks if those fields changed |
| Action/button based | User presses a status-change button (e.g. Release, Approve) | Application anticipates field change in callback — knows button press will update field X — triggers reauthentication before save |

> **Current limitation:** Framework supports field-value-change trigger but NOT
> a direct "field changed from value A to value B" check. Value-level triggering
> (e.g. only trigger when status changes to REL, not for all status changes)
> is on the roadmap but not yet delivered.

**Workaround for action-based reauthentication:**
Application knows that pressing "Release" will update field OVERALL_STATUS.
In the callback, detect that the Release action was taken (via anticipation / context)
and return `ABAP_TRUE` to trigger reauthentication — even before the field is physically
written in the table.

---

## 10. GxP Active Check

Application can check at runtime if GxP/eSignature is active:

```abap
" Framework exposes an API that returns TRUE/FALSE
" Both conditions must be true for GxP to be considered active:
"   1. Scope item 84P is activated (S4 side)
"   2. BTP eSignature service integration is provisioned (BTP side)
" Only when BOTH are active does the framework return ACTIVE = TRUE
```

---

## 11. Integration Checklist for a New LOB Application

```
Backend Setup (SE24 / SPRO)
[ ] Implement Reauthentication callback class (Relevancy Check)
[ ] Implement Authorization class
[ ] Register reauthentication object in S-table (object name + class names)
[ ] Define node types and field mappings in S-table
[ ] Configure regulated fields per node type
[ ] Add content delivery to scope item 84P transport

BTP Setup
[ ] Register same reauthentication object name in BTP
[ ] Define / attach reason codes to the object in BTP
[ ] Verify reason codes appear in dropdown for that object only

Application Code
[ ] Call REQUEST_REAUTH at the correct trigger point (before save / on button press)
[ ] Call VALIDATE_RESULT to confirm signature was captured
[ ] Call CHECK_ESIG_ACTIVE before any signature flow (skip gracefully if not active)
[ ] Handle ABAP_FALSE from relevancy check — ensure no silent skip on error

Testing
[ ] Test with GxP scope item 84P active
[ ] Test relevancy check returns TRUE only for regulated field changes
[ ] Test reauthentication dialog appears with correct reason codes
[ ] Test signature is linked to change document
[ ] Test mass update — single sign covers all objects
[ ] Test background job (system user) — reauthentication must be skipped
```

---

## 12. Key Contacts for Reauthentication Framework

| Name | Role |
|---|---|
| Yadesh Gupta | Reauthentication Framework Architect |
| Prabir Kumar Mallick | Framework Development Lead |
| Swarnava Chatterjee | eSignature — GxP requirements expert |
| Niranjan Raju | S4 LOB integration (Asset Management) |
| Loring Wu | ATO — integration consumer |

---

## 13. Relationship to eSignature Architecture

```
GxP Reauthentication Stack
        │
        ├── LAYER 1: Change Document Framework (S4)
        │           Tracks field changes, old/new values, timestamp, user
        │           Status: Verified for PO in 2608 ✓
        │
        ├── LAYER 2: Reauthentication Framework (S4 + BTP)
        │           Relevancy check → trigger → BTP eSignature SaaS
        │           Application integrates via 4 APIs + callback class
        │           Status: Planned for ME21N in 2702
        │
        └── LAYER 3: BTP eSignature SaaS
                    Validates user identity (PIN/password/biometric)
                    Stores signature record
                    Links signature to Change Document
                    21 CFR Part 11 / EU Annex 11 compliant
```
