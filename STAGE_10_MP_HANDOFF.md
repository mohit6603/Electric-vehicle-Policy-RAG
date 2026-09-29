# Stage 10 — Madhya Pradesh

Technical completion: 29 September 2026. This closes the eight requested jurisdictions plus Central. The saved index now contains **804 chunks** and the UI has **nine choices**.

## Implemented

Two original official PDFs, 60 selected physical pages and 156 chunks use the existing shared loader, classroom 1000/200 recursive splitter and persisted Chroma path. Sixteen labelled OCR/table/flow proposals have original/proposed hashes; four booklet tables use layout extraction. Mandatory evidence links retain policy period, vehicle conditions, charging cost/approval/uptime terms and RWA exceptions. No new dependency or model was added. The earlier sixteen corpus JSONL files remain byte-identical.

The final booklet is distinct from the excluded draft. Full PDFs, source dates, physical pages, page-scope exclusions and unresolved notification/operational gaps are recorded in [the source review](data/policies/madhya_pradesh/SOURCE_REVIEW.md). All source acceptance/current-entitlement flags remain false. The target cutoff remains 23 September; collection on 29 September is not retrospective certification.

## Observed checks

- 15 ingestion checks passed: provenance, 60 unique pages, chunk coverage/metadata, policy period and key charging/RWA conditions.
- 10 integration checks passed: startup without corpus embeddings, MP aliases, five filtered queries, mandatory conditions, all 60 page seeds within the context limit, negative guards and nine UI choices. Context sizes ranged from 2,518 to 37,642 characters.
- 13 combined integration/live checks passed through actual local Gradio HTTP and Groq: small charging rate/basis/cap/count; RWA working-day deadline/safety/written refusal conditions; subsequent rejected comparison cleared citations. Actual answers and excerpts are retained in `data/processed/madhya_pradesh/stage10_live_checks.json`.
- Six fresh-kernel checks passed, including MP ingestion, saved index, nine choices, entitlement abstention and local HTTP launch. Stage 5/6 notebook checks passed eight each; Stage 8 negative example guards passed.
- Existing suites passed: 16 persistence, 19 retrieval, 14 citation, 50 failure, 15 UI, 10 UP, nine Delhi, 11 Gujarat, 10 Telangana and 11 Karnataka checks.

The initial ingestion check caught the existing OCR string `pommon` in the common-load clause. The proposal was corrected against the rendered original, with its hash refreshed before indexing. Ollama was initially stopped; starting the installed local service resolved the rebuild prerequisite. No failed model answer was hidden or counted as passed.

Run `uv run --locked python checks/stage10_mp_checks.py` for integration checks; add `--live` for two billable/usage-consuming Groq calls, or `--live --case small_charging` / `--live --case rwa_noc` for one. These are AI-authored development cases, not the independent evaluation set.

## Next required work

Stage 10 technical development is finished. Consolidate actual team source/OCR/prompt review and independent expected answers before formal Stages 11–12. `evaluation/team_cases.json` provides empty slots and `evaluate.py` provides the gated, resumable runner; no formal evaluation is claimed. The application can be launched with `uv run --locked python run.py` from the project root; a fresh checkout first needs an explicit `run.py --build-index`.

AI assistance: source research, selected visual/OCR readings, ingestion/retrieval rules, development questions and output review, testing, documentation and Git publication. Git uses the authorized human identity; this does not replace the assignment's AI-use disclosure.
