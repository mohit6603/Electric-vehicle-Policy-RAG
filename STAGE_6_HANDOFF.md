# Stage 6: jurisdiction-aware retrieval

**Technical Stage 6 is complete.** The saved 231-chunk index is searched with an explicit `state` filter. Retrieved chunks lead to exact source-page excerpts, required amendments/conditions and dated scope notes. Eight notebook checks and 19 retrieval checks passed. No answer generation or UI is added here.

## Run this stage

Open `EV Policy Assistant.ipynb` from the project root in the pinned environment with Ollama running.

1. Run Stage 5's imports, index functions, inputs and open cells. Leave `rebuild_index = False`; the existing local index needs no rebuild for Stage 6. On a fresh checkout, complete the explicit Stage 5 build first.
2. Run all Stage 6 cells in order. No earlier ingestion cells or Groq key are needed.
3. Change `selected_jurisdiction` and `retrieval_question` in the search cell to inspect another query. The default Tamil Nadu query prints page references and evidence roles, then passes eight notebook checks.

The public notebook function is `retrieve_policy(selection, question, k=4, max_context_chars=50000)`. Its result contains a status/message, canonical jurisdiction, `context_docs`, diagnostic `seed_chunk_ids`, omitted-span records, the verification cutoff and the false current-entitlement permission. Only `status='retrieved'` supplies context. Stage 7 consumes the context and its date/version/review labels, not fetch raw seed text by ID. A successful retrieval is not proof that the evidence answers the question.

## Input behavior

The guide's recommended rule was implemented after the optional preference question received no answer: accept documented aliases, clarify selection/question conflicts, and require separate queries for multiple jurisdictions. This is a stated working assumption, not explicit user selection.

- A question without a jurisdiction uses the selected jurisdiction; an explicit matching name is allowed.
- Conflicting names, multiple states, or state-plus-Central questions request clarification before search. Empty questions and missing/unsupported selections also stop before search.
- Current choices are **Maharashtra, Tamil Nadu and Central**. Delhi and the other planned states remain unsupported until their ingestion stage.
- Aliases include `Tamilnadu`, `New Delhi`, `Gujrat`, `Telengana` and PM E-DRIVE spellings. `MH`, `TN`, `UP`, `MP`, `GJ`, `TS`, `KA` and `DL` are recognized as uppercase abbreviations in questions; selection aliases are case-insensitive. Ordinary lowercase “up” is not a state mention.
- The Central pilot rejects explicit FAME/EMPS, car, bus, truck, ambulance and charging-infrastructure requests. Its scope remains PM E-DRIVE two-/three-wheeler buyer incentives and eligibility.

The complete alias list is in [retrieval_rules.json](data/retrieval_rules.json). These are English name/word checks, not a location-recognition model: city-only queries, unlisted misspellings, other-language names, negation and quoted place names are not interpreted semantically. Explicit recognized names trigger the conservative clarification rule. Relevance/answerability checks and broader failure handling remain Stage 8 work.

## Evidence and version handling

The implementation reuses Lab 4 cells 127/129 with `filter={'state': jurisdiction}` and `.invoke(question)`. The [official Chroma integration](https://docs.langchain.com/oss/python/integrations/vectorstores/chroma) documents metadata-filtered search. This stage adds a small explicit rule file for the prepared pilot sources; it is not an automatic policy-consolidation system.

Every query includes its jurisdiction's core dated restrictions, then the matched pages and one hop of their recorded adjacent pages. Mandatory update, conditions, policy-period and replacement links are followed to completion with cycle detection. Adjacent pages do not recursively pull in the whole source. An absent, excluded or cross-jurisdiction mandatory page is an error. Context exceeding the character budget returns no context rather than silently dropping required evidence.

Twenty page rules record source-text hashes and exact character offsets for known exclusions. Superseded Maharashtra section 4.2(1), Tamil Nadu's earlier road-tax paragraph, Central's older period/outlay/rate summaries and March's replaced e2w provisions are omitted only from assembled context. The unaffected conditions and March e-rickshaw row remain. Specialist bus-only portions are also excluded from the Central buyer context. PDFs, OCR proposals, page/chunk files and the saved vector index are unchanged.

Each excerpt retains the original document/URL/physical page and metadata, plus `evidence_id`, `excerpt_start`, `excerpt_end`, `excerpt_sha256`, `context_role`, `version_note` and retrieval reasons. `text_sha256` continues to identify the complete original page; `excerpt_sha256` identifies the returned slice. Every excerpt is an exact contiguous source-text slice; separate slices from one page have separate evidence IDs. No rewritten policy text is inserted into the excerpts.

Tamil Nadu's printed demand/fee deadline remains explicitly historical; its later motor-vehicle-tax notification does not extend those provisions. Central context retains the newest saved amendment, fund limitation, separate claim deadline and L5 closure. Maharashtra includes June/July operational conditions and the August replacement. These rules are AI-prepared, pending team review; all source acceptance and current-entitlement permission flags remain false.

## Checks and next stage

Run `uv run --locked python checks/stage6_retrieval_checks.py`. The 19 checks cover eight live queries across all three choices, 20 rejected input cases, exact excerpt/source metadata, all 20 page rules, missing/cross-jurisdiction dependencies, modified hits/inputs/model, empty search and budget overflow. Each live query embeds only the question; the corpus is not re-embedded. Observed contexts contain 5–15 pages and 11,619–28,899 characters; these are technical observations, not answer-quality scores.

Reports: [notebook checks](data/processed/search/stage6_checks.json) and [retrieval checks](data/processed/search/stage6_retrieval_checks.json). A fresh Jupyter kernel passed the Stage 5 reopen plus Stage 6 sequence. Earlier ingestion outputs remained byte-identical and Stage 5 persistence checks still passed.

AI assistance covered implementation, the pilot-specific evidence rules, technical cases, actual local retrieval runs, documentation and Git publication. These technical questions do not replace the team's independently authored formal evaluation set. Manual source/rule review and current-benefit verification remain deferred.

Stage 7 now builds on this retrieval result. See [the Stage 7 handoff](STAGE_7_HANDOFF.md) for its AI-assisted prompt draft, source-ID checks and original PDF-page links. Team prompt/source review remains pending.
