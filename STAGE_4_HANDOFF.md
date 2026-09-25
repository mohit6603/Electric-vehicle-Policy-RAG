# Stage 4: Central PM E-DRIVE ingestion

**Technical Stage 4 is complete:** ten official documents, 53 audit pages, 35 draft pages and 100 chunks. The selected pilot covers two-/three-wheeler buyer incentives, eligibility and e-vouchers through the agreed 23 September 2026 cutoff. This was the assistant's stated recommended scope after the optional breadth question remained unanswered; detailed truck, ambulance, bus and charging rules are not covered by this pilot.

## Run this stage

Open `EV Policy Assistant.ipynb` from the project folder using the existing locked environment.

1. Run **Shared page loader**.
2. Run all **Stage 4: Central PM E-DRIVE buyer incentives** cells in order.
3. Confirm **53 audit pages, 35 draft pages, 100 chunks and 13 passed technical checks**.

No API key, Groq, Ollama or Stage 1–3 execution is required. The committed state artifacts supply isolation checks. Rerunning replaces Central's derived outputs only. Save notebook changes before running and clear outputs before committing; the report hashes the notebook file on disk at export.

## Sources and reuse

The [source review](data/policies/central/SOURCE_REVIEW.md), [research log](data/policies/central/research_log.json) and [manifest](data/source_manifest.json) identify every original PDF, date, URL, hash, physical-page selection and historical exclusion. [OCR records](data/ocr/central/review.json) map five raw/proposed page pairs to their PDF originals; none is human-verified.

The implementation reuses `load_policy_pages`, `Document` metadata and the class recursive splitter with 1000 characters and 200 overlap. Numbered-section/table separators retain the checked incentive blocks. A small shared-loader addition starts four mixed-language pages at a recorded English heading; raw extraction hashes are retained. Earlier state page/chunk artifacts remain unchanged.

| Output | Contents |
|---|---|
| [pages.jsonl](data/processed/central/pages.jsonl) | All 53 selected pages, including historical and audit-only records |
| [chunks.jsonl](data/processed/central/chunks.jsonl) | 100 draft chunks from the 35 selected answer-context pages |
| [stage4_checks.json](data/processed/central/stage4_checks.json) | Observed counts, splitter settings, critical evidence chunk IDs and hashes |

Central is stored as `state=Central`, with `scheme=PM E-DRIVE` and the explicit buyer scope. Required update links identify the March/August 2026 amendments. The March page's earlier e2w provision is flagged as superseded; the e-rickshaw row remains available. Current table pages link to base eligibility. Stage 6 must actually resolve these links and enforce scope when assembling answer context.

## Checks and remaining work

Thirteen notebook checks cover page/source completeness, audit exclusions, provenance, scalar metadata, preserved text, valid relationships, both current table blocks and their limits, fund/claim deadlines, L5 closure, buyer/e-voucher rules and distinct Central/state IDs. Nine invalid-input tests reject bad source/hash/page/OCR/marker data.

These are ingestion checks. They do not verify unexhausted funding, an individual buyer's eligibility, a complete legal consolidation or model-answer quality. All acceptance/entitlement permission flags remain false. Four team-authored central expected-answer cases, genuine source/OCR review and the remaining status checks are still deferred.

Stage 4 ends here. Stage 5 persistent semantic search is now implemented separately; see [its handoff](STAGE_5_HANDOFF.md). No embeddings, index, UI or generated policy answers belong to this checkpoint.
