# Stage 10 — Telangana handoff

Telangana's **technical batch is complete**. Next is Karnataka, then Madhya Pradesh, one jurisdiction per session. Team source/OCR acceptance, current-benefit verification and formal evaluation remain deferred. The agreed cutoff remains 23 September 2026; this packet was collected on 28 September.

## Sources and reuse

Two official PDFs provide **13 pages and 32 chunks**: the 2020–2030 EV & ESS booklet (physical pages 5–16) and G.O.Ms.No.41 of 16 November 2024 (physical page 1). The [source review](data/policies/telangana/SOURCE_REVIEW.md) records scope, date precision and unresolved later-instrument/operational gaps. The original PDFs, hashes and [one-page OCR proposal](data/ocr/telangana/README.md) remain traceable and unaccepted.

Four new `stage10-telangana-*` cells reuse `load_policy_pages`, the recursive 1000/200 splitter, stable IDs, relationships and export checks. Stage 5's ingestion list gains Telangana. Stage 6 reuses existing aliases, mandatory evidence and hashed exclusions; Stage 7/8's answer and failure paths are unchanged. Gradio gains a seventh choice and a private-car tax example. No dependency, model or general answer prompt changed.

The explicit index rebuild contains **543 records**: Maharashtra 53, Tamil Nadu 78, Central 100, Uttar Pradesh 117, Delhi 132, Gujarat 31 and Telangana 32. All earlier twelve corpus JSONLs are byte-identical. Earlier ingestion receipts were refreshed for the expanded manifest. Normal startup reopens the index without corpus embeddings; a fresh checkout must build its ignored local Chroma index explicitly.

## Context and checks

Telangana/Telengana/TS resolve to the new jurisdiction. The policy-period page and later tax notification are mandatory. Seven checked spans remove old tax/fee quotas from answer context, while retaining the original audit text, retrofit rate/cap/count and state-bus encouragement. The new tax notification preserves its purchase/registration requirement, deadline, unrestricted count and bus qualifications. Manufacturing's reference to Electronics Policy 2016 and charging encouragement remain distinct from current operational benefits.

Recorded checks in `data/processed/telangana/`:

- **12 ingestion checks:** source/proposal hashes, 13 unique pages, 32 stable chunks, metadata/links, complete non-whitespace coverage, policy period, retrofit limits, charging wording, manufacturing thresholds/caps and tax/bus conditions.
- **10 integration checks:** reopen with no corpus embeddings, three aliases, five filtered semantic queries, required evidence, all 13 seeds within the context budget (2,433–9,406 characters), old-quota exclusions, OCR provenance, five model-free rejections and seven Gradio choices.
- **Six fresh-kernel checks:** ingestion, ready startup, 543 records, seven choices, current-entitlement abstention and Gradio HTTP launch.
- **13 combined live/integration checks:** two real Groq answers through Gradio HTTP, plus a comparison rejection that clears previous citations. Private-car tax cites gazette page 1 and retains 100%, purchase/registration, 31 December 2026 and unlimited count; retrofit cites policy pages 10 and 9 and retains 15%, Rs.15,000 and first 5,000. OCR derivation is shown in Sources. AI output review found the requested claims supported by these excerpts.
- Existing regressions passed: **16 persistence, 19 retrieval, 13 citation, 50 failure, 15 UI, 10 UP, nine Delhi and 11 Gujarat checks**. Stage 5/6 notebook cells passed eight each; Stage 8 negative examples passed without Groq.

An initial integration assertion incorrectly assumed there would be no excluded spans; it failed before model calls. The check now validates the seven intended old-tax exclusions and joins retained excerpts when checking retrofit text. No failed live answer was discarded. These are development checks, not the two independently authored Telangana evaluation cases or proof of general model accuracy.

## Resume and run

For ingestion, run `shared-loader`, then the four `stage10-telangana-*` code cells. Refresh all earlier ingestion receipts after changing the shared manifest, and explicitly rebuild Stage 5 only when the corpus changes. Use [Stage 9 launch instructions](STAGE_9_HANDOFF.md) for the UI, with `rebuild_index = False` on this prepared machine.

```sh
uv run --locked python checks/stage10_telangana_checks.py
uv run --locked python checks/stage10_telangana_checks.py --live
```

The default uses local Ollama query embeddings and no Groq. Live mode adds two questions, 60 seconds apart; `--live --case private_car_tax` or `--live --case retrofit` runs one. Preserve any failed report before rerunning a command that overwrites it. Source acceptance/current-entitlement flags remain false.

AI assistance covered official-source research, PDF visual comparison, OCR proposals, implementation and retrieval rules, development questions, execution/output review, documentation and authorized Git publication. Disclose the actual assistance in the assignment appendix. User-authorized Git identity is retained without an LLM coauthor trailer.
