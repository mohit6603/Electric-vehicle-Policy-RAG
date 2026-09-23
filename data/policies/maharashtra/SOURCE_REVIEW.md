# Maharashtra source checkpoint

Reviewed: 23 September 2026. Agreed verification cutoff: **23 September 2026**.

Stage S is **incomplete**. Four official PDFs are saved unchanged, with provenance, page counts and hashes in [the source manifest](../../source_manifest.json). They are research inputs, not an accepted ingestion set. The notebook still contains setup checks only.

Follow-up on the same date: the user accepted one OCR preparation session for the June and July circulars. [Five page-matched drafts](../../ocr/maharashtra/README.md) are now prepared, with observed errors recorded and team verification pending. Original extraction results below remain the audit record; OCR drafts have not been accepted in their place.

## Official sources found

The [Motor Vehicles Department EV listing](https://transport.maharashtra.gov.in/Site/Common/ViewPdfList.aspx?Doctype=d0bc9262-60e0-4dcd-afa2-324484089ba1) links the policy and both operational circulars. The [Transport Department document listing](https://transports.maharashtra.gov.in/en/documents/) links the corrigendum through the government S3WAAS document host. Listing/upload dates differ from the dates printed in the PDFs; the manifest uses the latter.

All page references below are physical PDF pages, starting at 1. The observations are AI-assisted research notes requiring team verification, not student-written evaluation answers or certified translations.

| Document | Pages | Role and extraction result |
|---|---:|---|
| [Policy, 23 May 2025](maharashtra_ev_policy_2025-05-23.pdf) | 25 | Base policy. English pages 16–25 are an extraction candidate. Table 2 on page 18 and conditions on page 19 were visually compared with extracted text; row values remain readable before splitting. Marathi pages have character-mapping problems. |
| [Circular 41/2025, 19 June 2025](maharashtra_ev_operational_guidelines_2025-06-19.pdf) | 4 | Operational conditions for demand incentives. All four pages were visually inspected. The text layer returns characters but garbles Marathi; it is unsuitable for indexing as extracted. |
| [Circular 53/2025, 28 July 2025](maharashtra_ev_operational_guidelines_2025-07-28.pdf) | 1 | Clarifies the June circular. Visually inspected; no text extracted. Requires a checked transcription or OCR. |
| [Corrigendum, 29 August 2025](maharashtra_ev_corrigendum_2025-08-29.pdf) | 3 | Amends the toll-reimbursement clause. Pages 1–2 were visually inspected. Marathi text extracts with character errors and needs checking before ingestion. |

## How the documents fit together

The base policy describes a 1 April 2025–31 March 2030 policy period on page 16. Its demand-incentive table on page 18 contains percentages, per-vehicle maximums and vehicle-count limits; page 19 adds conditions. These are separate fields, and the vehicle-count limit must not become a rupee cap during extraction. An intact table before splitting does not establish intact chunks later. [Official policy](https://transport.maharashtra.gov.in/Site/Upload/GR/EV%20Policy%202025%20dated%2023-05-2025.pdf).

The June circular's page 2 addresses registration from 23 May 2025, OEM responsibility, invoicing, claim deadlines and first-come allocation within limits. Page 3 describes verification/payment steps and fleet-operator documentation. Its final provisions retain the policy's precedence in case of conflict. Do not infer demand-incentive eligibility from 1 April solely from the overall policy period. The team must verify the Marathi conditions against the source before using them. [Official June circular](https://transport.maharashtra.gov.in/Site/Upload/GR/Operational%20Guidelines%20Circular%20dated%2019062025.pdf).

The July circular clarifies treatment of vehicles registered between 23 May and 19 June 2025, OEM/dealer responsibility and evidence of incentives passed to customers. It also addresses submission of pre-portal claims within the first 30 days after the portal became operational. The actual portal launch date has not been established here. Keep this circular with June's rules when reviewing historic claims. [Official July circular](https://transport.maharashtra.gov.in/Site/Upload/GR/Operational%20Guidelines%20Circular%20dated%2028072025.pdf).

The August corrigendum replaces the reimbursement wording in section 4.2(1): the Transport Department reimburses the concerned department/authority rather than naming the Public Works Department alone. It is a toll-related change; it does not establish additional purchase-subsidy availability. [Official corrigendum](https://cdnbbsr.s3waas.gov.in/s3d446e76a7b26f214b3f29f4441e6eb87/uploads/2025/09/202509221584431889.pdf).

## Current-status evidence and its limits

The Motor Vehicles Department listing's HTML includes a link labelled `MHEV Policy Portal Link` pointing to [mhevpolicy.in](https://mhevpolicy.in/). This establishes a government inbound link; the portal's own title alone would not establish provenance. The source listings reviewed did not establish that the collected amendment chain is exhaustive through the cutoff.

Two unauthenticated public responses used by the portal were saved in [status_evidence.json](status_evidence.json):

- Registration totals carry an `asOnDate` of 21 September 2026. Registrations are not approved or paid incentive claims.
- Vehicle-type counts were returned on 23 September 2026. Their response timestamps and category counts do not establish a signed benefit-status notice, available funding, or an individual buyer's eligibility. One category count even exceeds the base policy's stated vehicle limit; subtracting these counts from policy limits would be an unverified calculation.

The announcements request returned HTTP 401 and was not retried with credentials. No private portal data was accessed. These observations establish that public portal data was available when checked, but **do not verify that every listed benefit remained claimable on 23 September 2026**. A website review date or a successful HTTP response is also insufficient for that claim.

No current-entitlement claim is approved for the application from this checkpoint. Later answers must distinguish a policy provision from verified availability and abstain where the latter is unresolved. These review notes and public JSON responses are audit evidence, not replacements for the official PDF corpus.

## Next bounded session

1. Have the team verify the five OCR drafts against the original circular pages, record corrections and reviewer/date, and separately review the corrigendum's extracted text. Keep the original PDFs as citation targets. Do not index the garbled text layer or unchecked OCR.
2. Continue the official amendment/status check through the cutoff. Establish which vehicle categories and benefits can be supported as current, and retain explicit unknowns where official evidence is unavailable. Claim-process questions may need the portal launch notice and referenced supporting notifications.
3. Have the team check the document chain and extracted evidence. Only then accept the relevant sources for Stage 2, where the team implements page metadata and splitting using the existing classroom reuse map.

The initial source session created no OCR, ingestion, embeddings, index, policy answers or evaluation cases. The subsequent approved session prepared OCR drafts only; current-status verification remains open independently of text preparation.
