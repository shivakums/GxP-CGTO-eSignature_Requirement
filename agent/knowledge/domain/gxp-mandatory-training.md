# GxP Mandatory Training for Development Teams
## SAP Advanced Therapy Orchestration (ATO/CGT) — GxP Compliance Training

**Source:** GxP Training for CGT-TMP team — 2022-02-14 (Meeting Recording + Training Notes)
**Trainers:** Mukul (GxP Compliance Lead), Robin (Infrastructure Qualification Lead)
**Audience:** SAP Development teams building CGT/ATO platform on BTP
**Mandatory:** Yes — required for all developers/testers touching the system (21 CFR Part 11 requirement)

---

## 1. Why GxP Matters for ATO/CGT Development Teams

GxP compliance is **not optional** for the CGT/ATO platform. The ATO platform:
- Works with clinical trial data and patient treatment data
- Moves data across multiple platforms and supply chains
- Drives decisions about drugs that patients receive
- Patient safety is the ultimate consequence of data integrity failure

**Key principle from training:**
> "When you are building a CGT platform, when you are running against timeline, these are very
> painful — oh my God, these guys are stopping us from developing. But put yourself in that
> place — when we are trying to take a drug to a patient, was it doing these activities or not?"

**Mandatory training rule:** Every developer, tester, or person who touches the system must
complete this GxP training. It is logged and auditable — regulators can ask to see the training
records as part of a GxP audit.

---

## 2. What GxP Means — The Basics

**GxP** = Good x Practice where x = Manufacturing (GMP), Clinical (GCP), Laboratory (GLP),
Distribution (GDP), Documentation (GDocP). The X covers everything under "good practices."

### Two Core Objectives for ATO/CGT:
1. **Patient Safety** — data drives the drugs patients receive; incorrect data = patient harm
2. **Product Consistency** — predictable, traceable manufacturing across all stakeholders

### 5 Key Pillars of GxP Compliance (Integrated Compliance Framework):

| Pillar | What It Covers |
|---|---|
| **Quality Management** | Policies, procedures, risk assessment strategy, qualification standards, SDLC documentation |
| **Change Management** | How system integrity is maintained through changes; testing evidence; infrastructure qualification |
| **Access Management** | Role-based access control; who does what; identity management; accountability |
| **Data Integrity** | Completeness, consistency, accuracy, traceability — 90% of audits focus here |
| **Training & Education** | This session itself — all personnel touching the system must be trained |

---

## 3. What Is 21 CFR Part 11 — Developer Perspective

**21 CFR Part 11** (FDA, USA) = the primary regulation governing electronic records and
electronic signatures for drug makers, medical device manufacturers, biotech companies.

### What it requires that directly impacts development:

**Electronic Records must be:**
- Secured — data cannot be changed without a trace
- Attributed — who created/modified it
- Contemporaneous — time-stamped at time of action
- Original — or a verified true copy
- Accurate — matches the physical reality

**Electronic Signature is NOT fancy technology:**
> "E-signature in regulator terms is: you should be able to trace the person who took that
> decision or took that call in an irrefutable way with the timestamp, trace, ability to trace
> who did what, when, why, where. That is the key. Even if it is ID and a simple password for
> a critical transaction — they are more than happy as long as you follow those."
> — Mukul, GxP Compliance Lead

**Key implication for developers:** A simple SAP user ID + password re-entry for critical
transactions is GxP-compliant for eSignature — it does NOT require biometrics or PKI certificates.
Biometrics (used by Pfizer, Roche etc.) are optional enhancements, not requirements.

### What triggers eSignature requirement:
- Releasing a product
- Moving product from one stakeholder to another
- Any action that impacts patient safety
- Critical data changes in regulated fields

### What does NOT require eSignature:
- Display-only activities (user just viewing data — no logging required)
- System/background job activities (automated processes run by system users)
- Non-regulated field changes

### Dual Authentication — Q&A from training:
**Q:** Does each user password entry into the dual authentication process need to be stored in a log?
**A:** Yes — IF the user access enables them to take a call which may impact patient safety.
If it is just for display — no logging required.

---

## 4. Data Integrity — What Developers Must Ensure

**90% of regulatory audits focus on data integrity.** Regulators (FDA, EMA) walk in and ask:
- Can you show your change control process?
- Can you trace batch records — where was the drug manufactured, how was it shipped?
- Can you show audit logs for every transaction?
- Where do you retain data? How long? Can I access it? Can you recover it?

### ALCOA+ Standard — The Data Integrity Framework:

| Letter | Meaning | Development implication |
|---|---|---|
| A | Attributable | Every record must be traceable to who created/changed it |
| L | Legible | Records must be readable and permanent |
| C | Contemporaneous | Recorded at the time it occurred — timestamped |
| O | Original | First capture or verified true copy |
| A | Accurate | No errors or deviations from the truth |
| + | Complete, Consistent, Enduring, Available | Full lifecycle — generation to archiving |

### Data Integrity for CGT/ATO specifically:
- Live patient-specific products (cell therapies) move through the platform
- Data gets swapped or corrupted → adverse patient outcome → potential patient death
- Regulators go to the Nth level to find root cause — system fault or decision fault
- Without audit logs, policies and procedures — impossible to defend

### External Data Sources:
**Q from training:** Does the external data source need to be GxP compliant for our system to be compliant?

**A:** Divide external data into two parts:
1. GxP-relevant data → ask external provider to verify and validate their data
2. If external provider cannot validate → at your data entry point (data hub, interface) validate
   that data received exactly matches data sent. Once verified, your responsibility is fulfilled.

### Data Lifecycle — all stages equally important:
Generation → Processing → Storage → Retrieval → Archiving

Archiving is equally critical — regulators ask how long data is retained and whether it is recoverable.

---

## 5. Infrastructure Qualification — BTP Specific (Covered by Robin)

**Key insight:** The ATO/CGT application runs on SAP BTP. BTP services (HANA database, Workflow
service, Portal service etc.) have their own lifecycle — releasing updates every 1-2 weeks.
This creates a challenge: how do you keep a GxP-qualified system when the underlying platform
is changing continuously?

### Shared Responsibility Model:
```
Client (e.g. Roche, Novartis, Gilead)
  → Responsible for: validating processes, interfaces, identity mgmt in their environment
  → NOT responsible for: installing DVDs, running on-premise change management

SAP (as SaaS vendor for CGT/ATO)
  → Responsible for: qualifying the application and BTP infrastructure
  → Delivers: qualified software releases into production

SAP BTP (Platform as a Service)
  → Provides: HANA database, Workflow service, Portal, Event Mesh etc.
  → Continuously updated with new features, security fixes, hot fixes
```

### Cloud Service Qualification (CSQ) Approach:

Instead of reviewing each BTP service change individually (impossible — hundreds of updates),
SAP uses a **risk-based continuous verification approach**:

1. **Identify critical solution components** in the CGT/ATO application
2. **Identify which BTP services** those components depend on
3. **Define Intended Use** — what the SaaS application requires from each BTP service
4. **Conduct Risk Assessment** — GAMP5 standard — severity, detectability of possible failures
5. **Define testing strategy** — which component, which API, which cadence
6. **Continuous Verification** — automated tests run every 5 minutes / 1 hour / daily
7. **Service Qualification Platform** — monitors infrastructure compliance in real-time
8. **Reporting** — end-to-end traceability report from SaaS application to test evidence

### BTP Infrastructure Requirements for GxP:
- Data encryption at rest — YES mandatory for all electronic records under 21 CFR Part 11
- Data encryption in transit — YES mandatory
- Open system consideration (BTP is an open system) — encryption mandatory
- Backup and restore procedures at BTP service level
- ISO 27001 certificate
- SOC 2 Type 2 controls

### Emergency Updates Handling:
Security patches and emergency updates to BTP services are handled by assessing whether the
**requirement from CGT toward that BTP service is still fulfilled** — not by reviewing each
individual change. Cadence-based testing confirms service behavior continuously.

---

## 6. Qualification Documents — What GxP Requires

Regulators (clients conducting audits) expect these documents:

| Document | Purpose |
|---|---|
| **Traceability Matrix** | Maps: Epic → User Story → Requirements → Test Scripts → Test Results → Production deployment |
| **Risk Assessment** | GAMP5-based — failure scenarios, severity, detectability for each component |
| **Design Specification** | Documents the design approach |
| **Test Plan** | How testing is conducted, who, when, what scope |
| **Validation Report** | Summary report generated after all testing activities — final evidence |
| **Qualification Documents** | IQ (Installation), OQ (Operational), PQ (Performance) — infrastructure level |
| **Training Records** | Who was trained, when, on what — this session is one such record |

### Traceability Matrix — Most Important for Client Audits:
> "This is what your clients typically would want to see. Any change which goes into your
> platform — is it linked to a test case? How have you tested it? What are the activities?
> Right from epic, user story, to your requirements, to your test scripts and test results,
> and then when you move it to prod — that's called a traceability matrix."

---

## 7. Quality Agreements with Clients

**Every major Life Science client (Roche, Novartis, Gilead, Pfizer, Sanofi, Merck) requires:**
1. A **Quality Agreement** — separate from the contractual agreement
2. Self-certification of GxP compliance
3. Audit clause — client can conduct announced AND unannounced audits at any time
4. Evidence package ready on demand — documentation, audit logs, test evidence

**No external GxP certificate is required** — it is self-assessment backed by evidence.
SOC 2 Type 2 is useful but not sufficient alone — clients want to see the actual documentation.

---

## 8. Three Types of Controls Developers Must Understand

| Control Type | Examples |
|---|---|
| **Human Controls** | This training, culture, awareness, accountability |
| **Organizational Controls** | Shop surveillance, monitoring, CAPA (Corrective Action Preventive Action) |
| **Technical Controls** | Role-based access, password management, audit logs, change management, data encryption |

---

## 9. Key Rules for Developers — From This Training

1. **Follow policies and procedures — no shortcuts** even under time pressure.
   Everything is recorded. Short-circuiting a process is itself a compliance violation.

2. **If you find an incident or deviation — escalate immediately.**
   Document it. Regularize it. Do not ignore or hide it.

3. **Every change must be linked to a test case** — traceability matrix is mandatory.

4. **Audit trail must cover all regulated data changes** — who, what, when, old value, new value.

5. **Access is controlled** — only authorized users should access regulated parts of the system.
   Authorization records must be maintained.

6. **Data encryption** — at rest and in transit — is not optional for electronic records.

7. **Background jobs / system users** are excluded from eSignature requirement —
   only human user-triggered critical transactions require re-authentication.

8. **Training is mandatory and logged** — attendance at this training is itself a GxP record.

---

## 10. Regulatory Bodies and Standards Referenced

| Standard | Body | Region | Focus |
|---|---|---|---|
| 21 CFR Part 11 | FDA | USA | Electronic records and signatures |
| Annex 11 | EMA | European Union | Computerised systems (most stringent with FDA) |
| GAMP5 | ISPE | International | Risk-based approach to GxP-compliant computerised systems |
| MHRA | MHRA | UK | Data integrity guidance |
| WHO guidelines | WHO | International | Data integrity |
| SFDA | SFDA | China | Strict controls on data location and transfer |
| Brazilian Anvisa | Anvisa | Brazil | Electronic systems regulations |
| TGA | TGA | Australia | Electronic records |

> "By and large they all follow GAMP5. All these regulations come from GAMP — Good Automated
> Manufacturing Practice. It looks across the breadth and depth of wherever you are using IT
> systems for manufacturing drugs or delivering drugs across the broad spectrum of your entire
> pharma ecosystem."

---

## 11. Training Note from the Document

The Training Notes.docx contains one key note:
> "This is followed in BTP"

This refers to the Cloud Service Qualification (CSQ) framework — the approach of continuous
automated testing of BTP services is the mechanism by which SAP demonstrates GxP compliance
of the BTP infrastructure layer to clients.

---

## 12. Relationship to the ATO/eSignature Work in 2026

This 2022 training establishes the **foundational GxP requirements** that the 2026 work streams
are now implementing:

| 2022 Training Requirement | 2026 Implementation |
|---|---|
| Electronic signature for regulated changes | Reauthentication Framework + BTP eSignature SaaS |
| Audit trail for all field changes | Change Document Framework (CDHDR/CDPOS) — verified 2608 |
| Who did what, when, old/new values | CDHDR (who/when) + CDPOS (what changed) |
| ID + password re-entry is sufficient | Framework uses SAP password re-entry — compliant |
| Reason for change must be captured | Reason Code in reauthentication dialog |
| System context / background jobs excluded | Reauthentication framework skips system-user saves |
| Traceability required | Signature ID ↔ CHANGENR link in CDHDR |
