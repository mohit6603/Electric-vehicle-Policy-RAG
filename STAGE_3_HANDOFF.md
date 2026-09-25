# Stage 3: Tamil Nadu ingestion

**Technical Stage 3 is complete:** two official PDFs, 23 selected physical pages and 78 draft chunks. The notebook reuses Stage 2's loader, source metadata and course recursive splitter. Manual source acceptance and two team-written evaluation cases remain deferred.

## Run this stage

From the project folder, use the existing locked environment and open `EV Policy Assistant.ipynb` with `uv run --locked jupyter lab "EV Policy Assistant.ipynb"`.

1. Run the **Shared page loader** cell.
2. Run all **Stage 3: Tamil Nadu ingestion** cells in order.
3. Confirm **23 pages, 78 draft chunks and 12 passed technical checks**.

No API key, Groq, Ollama or Stage 1/2 execution is required. The committed Maharashtra chunk file supplies the second-jurisdiction comparison; this is an ingestion check, not filtered retrieval. Rerunning replaces only Tamil Nadu's derived outputs. Clear notebook outputs before committing; the report records the notebook file hash at export.

## Inputs and outputs

The [source review](data/policies/tamil_nadu/SOURCE_REVIEW.md) and [manifest](data/source_manifest.json) describe the original PDFs, dates and evidence gaps. The 2023 policy contributes physical pages 6–27; the December 2025 tax notification contributes physical page 1. Printed policy page numbers differ by five and are not used as PDF citations.

| Output | Contents |
|---|---|
| [pages.jsonl](data/processed/tamil_nadu/pages.jsonl) | 23 page records with original source/page citations and review/status metadata |
| [chunks.jsonl](data/processed/tamil_nadu/chunks.jsonl) | 78 chunks with stable IDs, start offsets and inherited evidence links |
| [stage3_checks.json](data/processed/tamil_nadu/stage3_checks.json) | Observed counts, splitter settings, check names, critical chunk IDs and hashes |

## Reuse and source-specific additions

`load_policy_pages` moved from the Stage 2 input cell to **Shared page loader**. Both jurisdictions use the same validation and `Document` construction. Tamil Nadu's manifest selects `pypdf` layout extraction on pages 17, 19 and 20 to preserve table rows. Whitespace padding is normalized; amounts and original PDFs are unchanged. No new dependency or OCR was added.

The class's 1000-character / 200-overlap recursive splitter is retained. Two section separators (`5.2.1` and `5.2.2`) keep Tamil Nadu's public/private charging headings, subsidy text and tables together. The demand table fits in one chunk; its conditions and printed expiry are linked to their source pages. Adjacent-page links retain possible continuations. Later retrieval must resolve these links when assembling evidence.

The motor-vehicle-tax notification has its own document identity, effective dates and benefit scope. The base policy page links to it for the road-tax provision only. The printed purchase-incentive deadline remains 31 December 2025 with extension status not established. No other benefit is silently extended.

## Checks and stopping point

All 12 notebook checks pass: page coverage, hashes/citations, physical numbering, preserved metadata/status, valid links, complete non-whitespace coverage, five demand rows and conditions, distinct demand/tax dates, public/private charging tables, swapping cap/count, tax-order scope/dates and distinct jurisdiction IDs. Six invalid-input tests exercise the shared loader for Tamil Nadu. Maharashtra's original 18 pages and 53 chunks remain byte-identical.

These results establish technical ingestion. They do not establish a fully verified policy corpus, model-answer accuracy or live entitlement. Team source review, amendment completeness/current-status gaps and the two independently authored Tamil Nadu cases remain pending. No embeddings, Chroma index, answers or UI belong to this stage.

Stage 4 now covers the PM E-DRIVE central buyer-incentive pilot; see [its handoff](STAGE_4_HANDOFF.md). Next is Stage 5 persistent semantic search.
