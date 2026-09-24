# Tamil Nadu source review

Prepared on 24 September 2026 for technical Stage 3. Verification cutoff: **23 September 2026**. This is AI-assisted source preparation and extraction checking; team acceptance is deferred. Current availability of the whole benefit package and completeness of the amendment chain are not established.

## Source packet

| Source | Official reference | Physical pages used |
|---|---|---|
| Tamil Nadu Electric Vehicles Policy 2023 | [SIPCOT-hosted policy](https://sipcotweb.tn.gov.in/uploads/policy/12/TN_Electric_Vehicles_Policy_2023.pdf) | 6–27 of 28; excludes covers, blanks and contents |
| G.O. Ms. No. 674, Home (Transport-I), 29 December 2025; Notification II(2)/HO/1344(d)/2025 | [Gazette PDF](https://www.stationeryprinting.tn.gov.in/extraordinary/2025/861_Ex_II_2_2025.pdf), [2025 official gazette listing](https://www.stationeryprinting.tn.gov.in/extra_ordinary_lists.php?id=MjAyNQ%3D%3D) | 1 of 1 |

Original bytes are saved alongside this note. Paths, SHA-256 hashes, page counts, dates and URLs are recorded in [the manifest](../../source_manifest.json). The booklet supplies the year 2023 but no exact notification day was established from it; `document_date` is therefore `2023`, with year precision. The gazette is dated 29 December 2025. Website retrieval on 24 September 2026 is not backdated to the cutoff.

## Date and scope findings

The base booklet's physical page 16 gives 31 December 2025 deadlines for the described road-tax, registration-charge and permit-fee provisions and the special demand-side incentives. Physical page 17 contains the demand table and conditions. The five-year general policy period on physical page 27 must not be substituted for these individual deadlines.

The later gazette specifies exemption from **motor vehicle tax** for battery-operated vehicles, both transport and non-transport, from **1 January 2026 through 31 December 2027**, and gives the applicable vehicle-definition reference. This is direct official evidence of that notified period. It does not extend the purchase-incentive table, registration charges or permit fees. Metadata links the old road-tax section to this later page without replacing all of page 16.

The bounded search also inspected the official TNEV resource listing and sought later demand-side operational guidelines/extensions. No such extension was established in this session; that is a research gap, not proof that none exists. Current funding, individual eligibility, claims availability, later amendments and the booklet's precise original notification date remain to be verified. All source acceptance and current-entitlement permission flags remain false. The known tax dates are retained separately so the evidence is not lost.

## Extraction checks

The PDFs have readable text layers; no OCR was added. Rendered policy pages **16, 17, 19, 20 and 27** and the full one-page tax notification were inspected. This was targeted AI comparison, not a complete human review of all 23 ingested pages.

Plain extraction on page 17 serializes table columns separately. Layout extraction retains the five rows; pages 19–20 also need it to distinguish charging categories, amounts and station counts. The manifest opts these three pages into layout extraction. The shared loader normalizes whitespace padding while keeping row order, paragraph breaks and physical-page citations. Other pages keep plain extraction, as Maharashtra does.

Checks compare the following source content to actual chunks:

- Demand table: the private e-cycle row and four commercial categories retain battery units, caps and annual counts. The e-cycle government-programme restriction, FAME II/local manufacture-sale-registration condition, DBT application text and footnote power/speed limits remain accessible on the same original page.
- Demand validity: page 17 links to page 16's printed deadline and keeps extension status `not_established`.
- Charging tables: public fast/slow charging retain their separate caps/counts; private fast charging retains the first-50 condition and 25% equipment/machinery subsidy. The land-cost exclusion and renewable-energy condition remain on page 19.
- Battery swapping: page 20 preserves the first-200 condition, 25% rate and Rs. 2 lakh cap, with a link to page 19's shared conditions.
- Tax notification: transport/non-transport scope, start/end dates and the vehicle-definition explanation remain together in one chunk.

The class's 1000/200 splitter initially separated the public/private charging headings from some supporting text. Stage 3 now prioritizes the `5.2.1` and `5.2.2` section boundaries before the usual recursive separators. The complete checked public and private blocks each fit inside one chunk. Maharashtra keeps its existing splitter settings and artifacts.

Some extracted headings lose spaces, and occasional ligature/word spacing remains imperfect. The printed demand-table header lacks a closing parenthesis after `Rs/KWh`; the private charger table repeats the public-station column label. These are preserved, not silently corrected. Conditions-page links require later retrieval to fetch the relevant page evidence; metadata alone does not implement that behavior.

## Deferred team work

Review the full selected source text and applicable document chain, record actual reviewers/dates, and independently write the two Tamil Nadu evaluation cases before formal evaluation. Check later status evidence through the agreed cutoff. Rebuild affected page/chunk artifacts after any source correction. The technical checks are not expected-answer evaluation cases or a current-entitlement approval.
