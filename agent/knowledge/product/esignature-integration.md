# eSignature Integration — Product Details

---

## 1. eSignature Service on BTP

The eSignature reusable service is already available as a SaaS on BTP.
It does NOT need to be built — it needs to be **integrated into LOB applications**.

Integration means:
- LOB app (ME21N) triggers the signature dialog at the right point in the process
- Signature is linked to the change document of the business object
- Audit trail is stored and accessible for GxP inspections

---

## 2. Integration Points in ME21N

```
ME21N Save Flow:
  1. User fills PO and clicks Save
  2. EKKO/EKPO written (standard)
  3. Change Document created (standard — verified 2608)
  4. [NEW] eSignature trigger point after Change Document
  5. Signature dialog shown to user
  6. User authenticates + signs
  7. Signature stored, linked to Change Document
  8. GxP-compliant PO save complete
```

### Configuration Options
- Which fields trigger signature requirement (configurable per field)
- Authentication method (SAP user password, PIN, external IdP)
- Signature reason (mandatory/optional text from signer)

---

## 3. Change Document Enablement — What Was Done in 2608

The eSignature team provided a list of PO-relevant fields to verify change tracking.
The PO team tested that change documents are correctly created for these fields.

**Result:** Change Document works correctly for Purchase Order in 2608.
No development was needed — just verification and testing.

---

## 4. What Still Needs to Be Done for 2702

### eSignature (Work Stream 1)
- Add eSignature trigger point in ME21N save flow
- Connect to BTP eSignature SaaS via communication arrangement
- Configure which PO fields require signature
- Test end-to-end: save PO → change doc → signature captured

### CGTO/ATO (Work Stream 3)
- Industry Object Extension nodes on EKKO/EKPO
- OData extension to expose CGTO fields via PurchaseOrder API
- Outbound event publishing on PO change (S4→Event Mesh)
- Inbound event handling for PO creation from ATO (BTP→S4 via OData)

---

## 5. Communication Arrangement for eSignature BTP Service

When implemented, a Communication Arrangement will be needed:
- System Alias pointing to BTP eSignature tenant
- Authentication setup (OAuth / service key)
- Test connectivity before enabling in productive system

This follows the same pattern as SAP_COM_0267 for other BTP integrations.
