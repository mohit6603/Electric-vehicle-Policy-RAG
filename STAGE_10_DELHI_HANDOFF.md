# Stage 10 — Delhi (NCT) handoff

Delhi's **technical batch is complete**. Gujarat is next, followed by Telangana, Karnataka and Madhya Pradesh. Source/team acceptance and current-entitlement verification remain pending under the agreed deferred-review workflow. The source cutoff stays 23 September 2026.

## Sources and implementation

The final policy notified on 30 June 2026 (effective 1 July) and operating guidelines dated 2 July replace the initial assumption that this batch would use 2020 policy extensions. The April draft is excluded. See the [source review](data/policies/delhi/SOURCE_REVIEW.md) for dates, conditions and outstanding verification.

Two original PDFs yield **51 candidate pages and 132 chunks**: seven English policy pages and 44 guideline pages. No OCR is needed. The full saved index now contains **480 chunks**: Maharashtra 53, Tamil Nadu 78, Central 100, Uttar Pradesh 117 and Delhi 132.

Four `stage10-delhi-*` code cells reuse the shared loader, 1000-character/200-overlap splitter and export/check pattern. Stage 5's `ingestion_stages` adds Delhi; existing routing enables Delhi, New Delhi, Delhi (NCT), NCT of Delhi and DL. Required page links retain subsidy/tax/scrapping conditions, N2 limits, model-approval exceptions and table/form continuations. Gradio automatically lists the fifth jurisdiction and has a Delhi example. No library, generation backend or separate app structure changed.

The previous eight corpus JSONL files reproduced byte-for-byte. Their ingestion receipts were refreshed for the changed shared manifest. The local Chroma index was explicitly rebuilt once and subsequently reopened without corpus embeddings. It remains ignored by Git and must be built on a fresh checkout.

## Run

Follow [Stage 9's definition-cell sequence](STAGE_9_HANDOFF.md) to launch the UI. It now offers five jurisdictions. Keep `rebuild_index = False` for the existing index. Avoid Run All when only launching Gradio: setup/example cells make extra model calls.

To reproduce Delhi ingestion, run `shared-loader` and the four `stage10-delhi-*` code cells. If changing the shared manifest, also rerun Stages 2–4 and the UP ingestion cells to refresh their receipts. A changed corpus requires an explicit Stage 5 rebuild, followed by returning its rebuild switch to `False`.

```sh
uv run --locked python checks/stage10_delhi_checks.py
uv run --locked python checks/stage10_delhi_checks.py --live
```

The default uses local Ollama retrieval without Groq. `--live` adds two development questions through local Gradio HTTP, paced 60 seconds apart. A targeted retry is available with `--live --case car_scrapping` or `--live --case two_wheeler`. Account limits can still cause failures; preserve the failed report before rerunning a command that writes the same filename.

## Recorded verification

- **13 ingestion checks**: page/chunk hashes, complete text coverage, metadata/links, subsidy bands, caps, dates, scrapping/tax conditions and deadline wording.
- **Nine integration checks**: reopen without corpus embeddings/rebuild, aliases, five semantic queries, conditions/continuations, no old/draft sources, every one of the 51 pages within the context budget, rejection guards and Gradio choices.
- **Six fresh-kernel checks**: Delhi ingestion, ready restart, 480 records, five choices, current-entitlement abstention and local Gradio HTTP launch; no Groq call.
- Stage 5/6 notebook checks also passed (eight each); updated Stage 8 example guards passed without Groq. Eleven final artifact/schema/credential checks passed.
- Regression suites passed: **16 persistence, 19 retrieval, 13 citation, 50 offline failure, 15 UI and 10 UP integration checks**.
- Actual Gradio/Groq two-wheeler answer retained all three rate/cap bands, the price ceiling and the policy-page citation. The first car-scrapping answer retained the amount, applicant limit, price ceiling, old-car requirement and deadline, but omitted ownership. The test expected that detail without explicitly asking it. That failed observation remains in `stage10_live_checks.json`; it is not counted as a pass. A targeted retry with ownership explicitly requested passed all checks, including the source pages. A subsequent mismatch cleared the previous citations. The successful retry is in `stage10_live_car_scrapping.json`.

Reports under `data/processed/delhi/` contain the tested notebook/script/rule hashes and actual answers. These limited development checks do not prove general semantic accuracy, complete policy verification or independently authored evaluation. Earlier live reports retain their original observations.

## Deferred acceptance

The team still needs to compare sources/extraction, resolve the notification/effective-date and registration/RC-generation wording issues, check later instruments and operational availability, and independently author the two Delhi evaluation cases. No actual reviewer/date is invented. All acceptance/current-entitlement flags remain false; no live quota, approved model, payment or personal eligibility is promised.

AI assistance covered research, original-source downloads, selected visual comparisons, notebook/configuration/check code, development questions, actual verification, documentation and Git publication. Disclose this in the assignment appendix. Git attribution uses the user's authorized identity.
