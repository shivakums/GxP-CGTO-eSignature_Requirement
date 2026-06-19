# Business Rules — GxP / CGTO / eSignature

## Rule 1 — Never Append Directly to EKKO/EKPO for CGTO Fields

**Rule:** CGTO/ATO industry-specific fields MUST use Industry Object Extension pattern.
Never add them as direct append fields to EKKO or EKPO.

**Why:** Approved architecture for public cloud (North Star governance). Direct appends
pollute standard tables, create upgrade risks, and are not the approved extensibility model.

**How to apply:** Any new CGTO/ATO field requirement → Industry Object Extension node
on EKKO/EKPO. Validate with Suite Architecture (Felix Vente's team) before implementing.

---

## Rule 2 — eSignature Requires Change Document

**Rule:** eSignature integration cannot be built until Change Document framework is
working correctly for the relevant PO fields.

**Why:** SAP eSignature attaches signatures to Change Documents. No CD = no signature anchor.

**How to apply:** Always verify CD is working first. In 2608 this was verified for PO — it works.
Do not invest in eSignature integration without CD working.

---

## Rule 3 — ME21N First, Manage PO App Deferred

**Rule:** Phase 1 eSignature integration targets ME21N (Web GUI). Do NOT invest in
Manage Purchase Order app (BOF-based Fiori) for eSignature.

**Why:** Manage PO app has feature parity gaps. Modernisation is in progress. New UI will be
the correct target for eSignature. Investing in BOF app eSignature is wasted effort.

**How to apply:** Any eSignature task → confirm it is for ME21N scope before starting.
If it is for Manage PO app → flag as deferred and redirect to correct scope.

---

## Rule 4 — iFlow Handles Schema Mapping

**Rule:** Do NOT attempt to match event schemas between BTP/ATO and S4 in application code.
The Integration Suite iFlow is responsible for all schema transformation.

**Why:** BTP SaaS (ATO) and S4 have different event schemas. The iFlow subscriber account
handles the mapping. Bypassing it breaks the integration.

**How to apply:** S4 publishes events in S4 schema. BTP consumes in BTP schema.
iFlow in between translates. Never hardcode BTP schema expectations in S4 code.

---

## Rule 5 — North Star Architecture Governance for Public Cloud

**Rule:** Any extension in SAP S/4HANA Public Cloud must be reviewed and approved
by the Suite Architecture team (Felix Vente) as part of North Star governance.

**Why:** Public cloud has stricter extension rules than private cloud. Unapproved extensions
may not be shippable or maintainable.

**How to apply:** Before implementing any new extension pattern → architecture review.
Reference: CGTO/ATO went through this process and received approval for Industry Object Extension.

---

## Rule 6 — CGTO is Now Called ATO

**Rule:** The product was renamed from CGTO (Cell and Gene Therapy Orchestration) to
ATO (Advanced Therapy Orchestration) in May 2026.

**Why:** Scope expanded beyond cell & gene therapy to include plasma, medical devices,
surgical therapy, and radio ligand therapy.

**How to apply:** Use ATO in new documentation and communications. Recognise CGTO in
legacy documents and meeting references — they refer to the same product.
