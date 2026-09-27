# Stage 10 — Uttar Pradesh handoff

This batch adds **Uttar Pradesh only**. Delhi (NCT), Gujarat, Telangana, Karnataka and Madhya Pradesh remain separate Stage 10 batches. The source cutoff is still 23 September 2026. This is technical prototype completion; source acceptance, current entitlement and the team's independent evaluation are pending.

## Added evidence and code

Six official PDFs produce **39 page records and 117 chunks**. The corpus now has **348 chunks**: Maharashtra 53, Tamil Nadu 78, Central 100 and Uttar Pradesh 117. See [source review](data/policies/uttar_pradesh/SOURCE_REVIEW.md) for document dates, source-chain gaps and selected-page scope. Ten Hindi pages have hash-linked AI English readings, explicitly labelled as unofficial and awaiting review. Original PDF bytes and physical-page citations are retained.

Four `stage10-up-*` code cells reuse the shared loader and the classroom 1000-character/200-overlap splitter. Stage 5 and Stage 6 share the simple `ingestion_stages` list. Existing aliases enable `UP` once its chunks are loaded; ordinary lowercase “up” still does not select the state. Gradio loads the fourth choice automatically and adds one UP example. The source renderer/callback preserve translation provenance.

UP retrieval keeps the revised purchase-subsidy pages, conditions and both 2025 tax/fee orders available. Hash-checked exclusions remove the superseded fiscal paragraph (including text hidden by a visual mask over the old 3W row) and the old one-year period. The 2024 cancelled 3W purchase provision stays distinct from the later pure-EV tax/fee exemptions. The fleet ownership minimum stays distinct from the subsidised-vehicle maximum. Original page records remain unchanged for audit.

No dependency changed. The three earlier jurisdictions' six JSONL files reproduced byte-for-byte; their ingestion receipts were refreshed because the shared manifest changed. The Chroma index was explicitly rebuilt once, then reopened without corpus embeddings. The database remains ignored and is recreated on a fresh checkout.

## Run and verify

For normal use, follow [Stage 9's definition-cell launch sequence](STAGE_9_HANDOFF.md). It now offers four jurisdictions. Keep `rebuild_index = False` when using the existing index. Do not use Run All if you only want to launch the UI: early setup/example cells make extra model calls.

For ingestion, run `shared-loader` and the four `stage10-up-*` cells. If the shared source manifest changes, rerun Stages 2–4 before the index stage so their receipts match. For a new/changed corpus, run Stage 5 with `rebuild_index = True` once, then return it to `False`. All sources and prepared text are committed; no runtime OCR is needed.

```sh
uv run --locked python checks/stage10_up_checks.py
uv run --locked python checks/stage10_up_checks.py --live
```

The default check uses local Ollama retrieval, with no Groq calls. `--live` adds three Groq questions through Gradio HTTP, spaced 60 seconds apart. Account limits can still interrupt a run; reports retain failures. To retry one case without spending on earlier successes:

```sh
uv run --locked python checks/stage10_up_checks.py --live --case cancelled_3w
```

Recorded verification:

- 13 UP ingestion checks; all 39 pages assemble with applicable version rules, and five semantic queries stay within UP and the context budget.
- 10 integration checks: counts, aliases, amendments/exclusions, five rejected queries with no model calls or stale citations, and four Gradio choices.
- Six fresh-kernel checks: UP ingestion, restart, 348 records, four choices, current-entitlement abstention and local Gradio launch.
- Existing checks: 16 index-persistence, 19 retrieval, 13 citation, 50 offline failure and 15 Gradio checks passed. Stage 5 and Stage 6 notebook check cells also passed, eight each.
- Actual live observations and any retry are saved under `data/processed/uttar_pradesh/`. The initial live check caught a missing translation label in the separate UI source list; the callback was corrected. The next run passed purchase and tax/fee cases, then hit a Groq rate limit on the 3W case. Those attempts remain recorded, not recast as successes. A targeted retry then passed the 3W cancellation case with the amendment-page citation; its subsequent mismatch request cleared the previous sources. All three live cases therefore passed across the recorded attempts, not in one uninterrupted run.

Reports include hashes for the versions actually tested. Earlier stage histories and old live reports retain their original observations; they are not new evaluations of UP. Notebook outputs are empty, `.env` is ignored and no secrets or local database are committed.

## Deferred acceptance

The two UP development questions/answers do not count as independently written team evaluation cases. A reviewer must compare the original pages with the AI readings, check the remaining amendment/status gaps, record actual reviewer/date and independently write the two UP cases. All `team_verified`, `accepted_for_ingestion` and current-entitlement flags remain false. The UI cannot promise available money, approval, payment or personal eligibility. Manufacturing/charging text describes the base policy; separate operational orders and current applicability remain unverified.

AI assistance covered research, official downloads, visual comparison/English readings, notebook and check code, development prompts, actual local/Groq tests, documentation and Git publication. This must be disclosed in the assignment appendix. Commit attribution uses the user's authorized Git identity.
