# Delhi (NCT) source review

Technical packet prepared on 27 September 2026 for the agreed **23 September 2026 cutoff**. All sources remain candidates: no team reviewer, acceptance, exhaustive amendment audit or current-entitlement verification is claimed.

## Official packet

| Document | Document date / official listing | Ingested physical PDF pages |
|---|---|---|
| [Delhi Electric Vehicle Policy 2026](https://transport.delhi.gov.in/sites/default/files/Transport/circulars-orders/delhi_ev_policy_2026-30_0.pdf) | 30 June 2026 notification; listed 1 July; expressly effective 1 July 2026 | English 12–18 of 18; Hindi 1–11 not duplicated |
| [Centralized Operating Guidelines](https://transport.delhi.gov.in/sites/default/files/Transport/circulars-orders/operating_guidelines.pdf) | Signed 2 July 2026; listed 8 July | All 44 English pages, including blank application/checklist forms |

Listings: [policy](https://transport.delhi.gov.in/transport/delhi-ev-policy-2026-0), [guidelines](https://transport.delhi.gov.in/transport/centralized-operating-guidelines-delhi-ev-policy), [notifications](https://transport.delhi.gov.in/notifications). Original bytes, SHA-256, dates and physical page numbers are recorded in `data/source_manifest.json`. The two sources produce 51 page records and 132 chunks. No OCR or unofficial translation is needed.

The final policy is the governing packet for this pilot. The April 2026 consultation draft and older 2020 policy/extension material are not indexed. The notifications page's 14 September gazette download was empty; the matching [official eGazette PDF](https://egazette.gov.in/WriteReadData/2026/276193.pdf) was obtained separately. It designates redressal authorities under CMVR Rule 167(5); it is not added as an EV benefit amendment. Its hash and exclusion are recorded in the research log. This bounded check is not proof that no other relevant instrument exists.

## Extraction and version details

Pypdf layout extraction is used for the seven English policy pages and selected guideline tables/checklists. Collapsing layout padding preserves row order and line breaks; other guideline pages use direct searchable text. Original PDF bytes are unchanged. AI visual spot checks covered policy pages 12–14 and 18, plus guideline pages 1, 7–9, 11, 15–16 and 18. This is not an independent human review of all pages or certification of the bilingual text.

Checks retain these distinctions:

- Policy page 13: electric two-wheeler ex-showroom ceiling ₹2.25 lakh. Registration Year 1 from notification: ₹10,000/kWh capped at ₹30,000; Year 2: ₹6,600/kWh capped at ₹20,000; Year 3: ₹3,300/kWh capped at ₹10,000. Plug-in and swapping models are covered. L5M rates are a separate table and its battery/permit conditions continue on page 14.
- Page 14: the N1 table distinguishes GVW above 1.75 tonnes from up to 1.75 tonnes. Car scrapping assistance is ₹1,00,000, limited separately to the first 1,00,000 eligible applicants, with an ex-showroom ceiling of ₹30 lakh. Delhi registration, BS-IV-or-below old car, authorised CoD, six-month new-purchase window and scrapped-vehicle ownership conditions must remain visible. This is a scrapping benefit, not a universal car purchase subsidy.
- Page 14: the general lifetime road-tax / registration-time fee clause is subject to the car clauses. Cars up to ₹30 lakh have the stated exemption through 31 March 2030; cars above that ceiling have none under those clauses. Do not turn the general clause into an unconditional all-car exemption.
- Policy page 15 plus guideline pages 10–11: the private N2 no-entry exemption has a 1,000-vehicle limit and three-month entry window from policy notification, whichever closes first; its duration is ten years from registration. Public institutional-use exclusions and any Apex Committee exception remain relevant. Remaining places are not verified.
- Policy page 13 and guideline page 7: purchase applications within 30 days of **RC generation**. Guideline Annex XII pages 42–43 instead say vehicle registration. Preserve and flag that wording discrepancy; guideline page 2 says the policy prevails. The 60-day disbursal period runs from application submission, subject to verification, rather than guaranteeing a payment date.
- Policy notification is dated 30 June but expressly takes effect 1 July. Yearly tables, the NOC restriction and other clauses use notification-based anchors; policy validity ends 31 March 2030 unless modified. Do not silently substitute an anchor or extend the shorter windows through the overall end date.
- Guideline page 4 has separate deemed-model-approval routes and validity dates. Annex II technical tables span pages 14–19; do not apply committee-assessment criteria universally without those exceptions. Pages 34–44 are application/checklist forms, not proof that an applicant or model has approval.

Retrieval retains required policy commencement/validity and guideline-priority pages. Page links add purchase/scrapping conditions, the N2 continuation, technical tables and the relevant multi-page forms. All 51 pages are tested as possible semantic seeds; source URLs cite original physical PDF pages.

## Deferred acceptance

An actual team reviewer must check extraction/table boundaries, date-anchor discrepancies, model approval/listing, any applicable later amendments or implementation orders, live portal operation and remaining allocation. Separate charging SoPs, tax/fee implementation instruments and the referenced 2023 aggregator scheme have not been assembled into a complete verified chain. The corpus can explain supplied provisions; it cannot certify current benefits or individual eligibility at the cutoff.

The two model questions are AI development checks, not independently authored evaluation cases. The team must independently write and verify its two Delhi cases during the deferred review batch. All acceptance/current-entitlement flags remain false. AI assistance covered source research, extraction checks, implementation, development questions, verification and documentation; disclose it in the assignment appendix.
