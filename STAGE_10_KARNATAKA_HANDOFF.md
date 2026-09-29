# Stage 10 — Karnataka handoff

Karnataka's **technical batch is complete**, closed on 29 September 2026. Next is **Madhya Pradesh**, one jurisdiction per session. Team source acceptance, current-benefit verification and formal evaluation remain deferred. The target cutoff is 23 September; this packet was collected on 28 September.

## Sources and reuse

Three official PDFs provide **41 pages and 105 chunks**: Clean Mobility Policy 2025–2030 (33 pages/84 chunks), final Act 29 of 2026 (seven pages/17 chunks), and G.S.R.525(E)'s registration-fee provision (one page/four chunks). The [source review](data/policies/karnataka/SOURCE_REVIEW.md) and [research log](data/policies/karnataka/research_log.json) record URLs, dates, hashes, selection and unresolved dependencies.

Four `stage10-karnataka-*` cells reuse the shared page loader, recursive 1000/200 splitting, metadata relationships and JSONL exports. The loader now accepts an explicit subset of proposal pages, preserving earlier full-document behavior. Nine [labelled AI table readings](data/ocr/karnataka/README.md) are mixed with plain/layout extraction. No OCR engine or dependency was added. Original PDF pages remain citation targets and all reviewer/acceptance fields remain empty/false.

The explicit index rebuild contains **648 records**: Maharashtra 53, Tamil Nadu 78, Central 100, Uttar Pradesh 117, Delhi 132, Gujarat 31, Telangana 32 and Karnataka 105. Earlier fourteen corpus JSONLs remain byte-identical. Ingestion receipts were refreshed for the expanded manifest/final notebook. Startup reopens without corpus embeddings; a fresh checkout must explicitly build its ignored Chroma index. Gradio now has eight choices and a Karnataka charging example.

## Context and limits

Karnataka/KA select only this packet. Period, definitions, approval conditions and table continuations are linked. Eight checked exclusion spans remove the old policy tax paragraph, the historical 2017 period and unrelated Act schedules from answer context while retaining audit text. The tax packet includes cost/age/refund tables and the separately limited registration-fee provision.

The Act's **separate commencement notification has not been verified or collected**. Tax answers describe the printed Act with an explicit commencement caveat; they do not establish currently payable tax. DPAL's certificate verification failed during public-source download; the research log records the transport limitation and independent Transport listing.

The policy appendix prints zone totals **199/32/9**; AI readings of the 240 taluks yield **198/33/9**. This remains unresolved, without silently altering assignments. Full Industrial Policy/MSME enabling instruments and later-instrument/operational verification remain pending. Current entitlement still abstains, and comparisons remain outside scope.

## Checks and observed corrections

Reports are saved in `data/processed/karnataka/`:

- **15 ingestion checks:** PDF/proposal hashes, 41 unique pages, stable chunks, complete non-whitespace coverage, metadata/links, period, category/zone/charging terms, tax/refund distinctions and limited fees.
- **11 integration checks:** reopen without corpus embeddings, two aliases, six filtered semantic queries, all 41 page seeds within the context budget (8,773–27,867 characters), version exclusions, proposal coverage rejection, model-free negative cases and eight UI choices.
- **Six fresh-kernel checks:** ingestion, ready startup, 648 records, eight choices, current-entitlement abstention and local Gradio HTTP launch.
- **Two supported HTTP development answers:** the final tax run passed 13 combined integration/live checks, including a comparison rejection that clears earlier sources. The actual charging response was locally rechecked after correcting numeric/word patterns, without another API call; its original run and notebook hash are retained. Charging retains 25%, Rs.10 lakh/station, 500 stations and no slow-charger incentive. Tax preserves all three cost slabs/rates and explicitly records unverified commencement, with original Act citations.
- Existing regressions: **16 persistence, 19 retrieval, 14 citation, 50 failure, 15 UI, 10 UP, nine Delhi, 11 Gujarat and 10 Telangana checks**. Stage 5/6 notebook checks passed eight each; negative Stage 8 examples passed without Groq.

The first live run withheld the tax answer as `citation_error`. A retained diagnostic showed that mathematical `>` was rejected by the existing markup guard. The prompt asks for comparisons in words. Because model output still sometimes used symbols, the validator now converts numeric comparisons (including inclusive bounds) to words before rejecting remaining markup; a new regression checks all four operators and existing markup-rejection cases still pass. A subsequent numeric-check pass still contained an unsupported “project cost” gloss in charging and an irrelevant policy-period citation in the tax point. AI semantic review required revision. The prompt now forbids invented calculation bases and unrelated citation labels; the Karnataka note requires the commencement caveat. Live checks now require the tax/commencement pages, restrict charging citations to its table and any actual period point, and reject the observed charging gloss. Assertions also rejected correct spelled-out numbers and “25 percent”; the check now accepts equivalent numeric/word forms. A later response cited the historical 2017 period as the new policy term; that historical span is now excluded from answer context. The new exclusion initially had an incorrect hash field, caught by preflight before any model call and corrected. Earlier failure, diagnostic and pre-review results are retained, not relabelled as final successes.

These are AI development checks and output inspection, not the two independently authored Karnataka evaluation questions or proof of general model accuracy. Manual review and the formal 24-case evaluation remain pending.

## Resume and run

Run `shared-loader`, then the four `stage10-karnataka-*` code cells for ingestion. After shared manifest/notebook changes, refresh earlier ingestion receipts. Explicitly rebuild Stage 5 only when the corpus/model changes; leave `rebuild_index = False` on this prepared machine. Use [Stage 9 launch instructions](STAGE_9_HANDOFF.md) for Gradio.

```sh
uv run --locked python checks/stage10_karnataka_checks.py
uv run --locked python checks/stage10_karnataka_checks.py --live
```

Default checks use local query embeddings and no Groq. Live mode adds two questions, 60 seconds apart; `--live --case fast_charging` or `--live --case car_tax` runs one. Preserve existing reports before rerunning a command that overwrites them.

AI assistance covered research, PDF visual/table comparison, proposed readings, implementation, retrieval rules and prompt refinements, development questions/checks/output review, documentation and authorized Git publication. Disclose the actual use in the assignment appendix. User-authorized Git identity is retained without an LLM coauthor trailer.
