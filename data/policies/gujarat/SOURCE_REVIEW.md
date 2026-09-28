# Gujarat source review

Collected and checked with AI assistance on 28 September 2026. The verification target remains **23 September 2026**. This is a technical source packet, not team acceptance or confirmation of current benefits. All acceptance/current-entitlement flags remain false; actual reviewers and review dates are pending.

## Official packet

| Source | Selected physical pages | Relationship and limits |
|---|---|---|
| [Gujarat State Electric Vehicle Policy 2021](https://www.powermin.gov.in/static/uploads/2025/07/3c383a891d96404e4b137b9e1ceb9ff9.pdf) — resolution dated 23 June 2021 | 3–7 of 7 | Original government policy hosted by the Ministry of Power. Four years from 1 July 2021; the end of 30 June 2025 is derived from that clause. No purchase/charging renewal established. |
| [Motor vehicle tax notification GH/PT/2025/13](https://egazette.gujarat.gov.in/ViewPdf2.aspx?docid=202504210834101619.pdf&cdbid=04b1daad51e67cccdfe90fc07bb46679&contentType=application/pdf) — 17 April 2025 | 1–3 of 3 | Amendments to PT/2017/6/MVD/2017/699/KH of 31 March 2017, including the EV category table. The original deadline is replaced by the next source. |
| [Motor vehicle tax notification GH/PT/2026/06](https://egazette.gujarat.gov.in/ViewPdf2.aspx?docid=20260404080501091.pdf&cdbid=eea3958b560b3b4ebb6101a297608df8&contentType=application/pdf) — 30 March 2026, gazetted 2 April | 4–5 of 6 (printed 47–48) | Replaces 31 March 2026 with 31 March 2027 in the clause above the tax table after the same parent's Schedule and Explanations. The 2025 table and 2026 continuation must be read together. |

Original PDF bytes, SHA-256, document dates, retrieval dates and page counts are in `data/source_manifest.json`. The latter two PDFs came from the public Gujarat eGazette search. The full 2017 parent was not obtained; the 2025 notification supplies the operative EV qualification/table. Do not imply complete verification of the parent's vehicle classifications or every later amendment.

## Text and page checks

All ten candidate pages were rendered and visually compared with extraction. Policy pages 3–6 use the shared layout path, collapsing spacing while retaining line order; its table rows preserve segment, battery capacity, rate and ex-factory ceiling. Some embedded spacing splits words. Page 7 retains minor pre-existing OCR errors in headings/signature; the interpretation provision is readable, but no team has accepted a corrected transcription.

Plain extraction is necessary for the 2025 tax PDF: layout extraction returns empty/near-empty text. Plain extraction preserves the row-wise category/rate/rebate/effective-rate order. No new OCR, dependencies or loader branch was needed. The 2026 gazette's physical pages 4–5 also contain education and land-revenue text. Full extracted pages remain in the audit/chunk files; hash-checked Stage 6 exclusions keep that unrelated text out of generated-answer context. The policy page 7 distribution list is similarly excluded from context. Original PDFs and physical-page citations remain intact.

## Provisions and traps

- Policy page 3 gives four years from 1 July 2021. Page 4 targets the first two lakh EVs: 1,10,000 two-wheelers, 70,000 three-wheelers and 20,000 four-wheelers. Treat these provisions as historical; a motor vehicle tax extension does not renew them.
- Page 5 Table 2 prints Rs 10,000 per kWh for all three segments; battery capacities 2/5/15 kWh and maximum ex-factory prices Rs 1.5/5/15 lakhs respectively. Clause 8(iv) limits the subsidy amount by battery capacity; it does not expressly disqualify a vehicle with a larger battery. The clause refers to column (2), but battery capacity is in column (3). Retain and flag that discrepancy instead of silently rewriting the instrument or claiming battery capacity is actually in column (2). Lump-sum caps are not explicitly printed in the table; the answer path must not invent calculations.
- Page 5 scope refers to vehicles that have taken the FAME II subsidy. Demand support is over and above central support, while a beneficiary may claim only one State scheme. This is historical text; it does not establish continuing FAME II availability.
- Page 6's charging provision states 25% of equipment/machinery cost, limited to Rs 10 lakh per station for the first 250 commercial public EV charging stations. Its distinct condition excludes entities that have availed other Government of India promotional subsidies. Subsequent procedure and charging standards are referenced, not comprehensively collected. Existing-connection charging excludes agriculture connections; the referenced GERC order does not establish a current numeric tariff here. The industrial-policy cross-reference likewise supplies no complete manufacturing incentive schedule.
- Tax page 1 requires the specified categories to be powered exclusively by an electric motor whose traction energy comes exclusively from an installed battery. Do not extend this to hybrids or every vehicle merely labelled electric in the older policy definition. Its initial general 6% omnibus amendment is followed by the specific EV table override.
- Tax page 2 private vehicles and several passenger categories list 6% existing, 5% rebate and 1% effective, all of vehicle cost. Agricultural/other specified tractors instead show 3/2/1%. Auto rickshaws licensed for at most three passengers show **2.5/1.5/1%**; the greater-than-three, at-most-six row shows 6/5/1%. A blanket 5% rebate is wrong.
- Tax page 3 includes two maxi-cab rows at 6/5/1%, the other-than-designated-omnibus row at 2/1/1%, educational private-service vehicles at 3.5/2.5/1%, and goods vehicles at 6/5/1%. Preserve category boundaries and the cost basis.
- The 2025 original prints “31st Match, 2026”; the 2026 notification calls it “31st March, 2026” and substitutes “31st March, 2027”. Both PDFs are retained. This is a motor vehicle tax deadline, not a registration-fee waiver, renewed cash subsidy, proof of remaining funds or approval for an individual vehicle.

## Observed answer limitation

Live development answers repeatedly interpreted the subsidy battery limit as vehicle eligibility, repeated the inconsistent column reference or cited the wrong period page. Those failed outputs are retained. Gujarat purchase-subsidy battery-limit questions now abstain before model calls, and generated claims using the known 2/5/15 kWh limits are conservatively withheld. This guard is bounded pattern matching, not a general semantic verifier. It does not resolve the source ambiguity; the team must review it before enabling that interpretation. Historical rate/price/period answers remain available, with an explicit historical label supplied by the renderer. The separate tax provisions remain available with their required update chain.

## Research limits and deferred review

The official 2026–27 budget announcement corroborates an additional year of tax relief, but the gazette amendment is used as answer evidence. Third-party copies/reports were discovery leads only. Neighbouring gazette notifications on general omnibus rates, road safety membership, scrapped-vehicle arrears and diplomatic vehicles were not indexed. Public transport listing errors and a failed alternate policy download are recorded in the research log; failure to obtain another instrument is not evidence that none exists.

Still required: genuine team comparison/acceptance; complete later-amendment and parent-schedule review through the cutoff; verification of operational applications, remaining allocations and applicable model/vehicle eligibility; any separate GEDA/student scheme if scope is expanded; and two independently written Gujarat evaluation questions with frozen expected answers and source pages. No reviewer/date or human-authored case has been invented. Development questions and model-output checks are AI-assisted technical observations, not formal evaluation.

AI assistance: source discovery/downloads, extraction and visual comparison, this research record, ingestion/retrieval configuration, checks and Git publication. Disclose the actual assistance in the assignment appendix.
