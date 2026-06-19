# GxP / CGTO / eSignature — Codebase Overview

## Project Overview

- **Name:** GxP-CGTO-eSignature_Requirement
- **Type:** SAP S/4HANA — GxP Compliance + CGTO/ATO Industry Integration for Purchase Orders
- **Domain:** Life Science compliance (GxP), Advanced Therapy Orchestration (ATO), eSignature

## Two Distinct Work Streams

| Work Stream | Topic | Target |
|---|---|---|
| 1 | eSignature integration in ME21N/ME22N | 2702 |
| 3 | CGTO/ATO industry field extension to EKKO/EKPO | 2702 |

## Tech Stack

- SAP S/4HANA ABAP (ME21N/ME22N, EKKO/EKPO, Change Document)
- BTP eSignature SaaS service
- BTP Event Mesh (async events S4↔ATO)
- Integration Suite iFlow (event schema mapping)
- Industry Object Extension pattern (CGTO fields)
- OData API extension (PurchaseOrder entity + CGTO extension)

## Key Objects

| Object | Type | Description |
|---|---|---|
| EKKO | Table | PO Header — target of CGTO extension |
| EKPO | Table | PO Item — target of CGTO extension |
| ME21N | Web GUI | Create PO — primary eSignature integration target |
| ME22N | Web GUI | Change PO — eSignature on changes |
| Change Document | Framework | Prerequisite for eSignature — verified 2608 |
| Industry Object Extension | Pattern | CGTO field addition (NOT direct EKKO/EKPO append) |
| Event Mesh | BTP Service | S4↔ATO event channel |
| iFlow | Integration Suite | Schema mapping middleware |

## Critical Decisions

- NEVER append CGTO fields directly to EKKO/EKPO — use Industry Object Extension
- ME21N is phase 1 for eSignature — Manage PO App (BOF) is deferred
- eSignature requires Change Document to work first (dependency)
- North Star Architecture governance required for public cloud extensions
