# Project checkpoint

## Current stage and next step

**Stage 6 — technical work complete.** Filtered retrieval covers Maharashtra, Tamil Nadu and Central, with required evidence links, exact source excerpts and explicit dated/scope labels. Eight notebook checks and 19 retrieval checks passed. Manual review remains deferred. Development is stopped at the Stage 6 boundary.

| Stage | Current status |
|---|---|
| 1. Environment preflight | Complete |
| 2–4. Pilot ingestion | Technical work complete; source acceptance, expected-answer cases and current-status checks deferred |
| 5. Persistent semantic search | Technical work complete: 231 chunks, explicit rebuild and reopen |
| 6. Jurisdiction-aware retrieval | Technical work complete: filtering, conflict handling and source-version context |
| 7–15 | Not started |

**Latest authorization:** the user requested completion of Stage 6. AI implementation continues with manual review deferred. The guide's recommended alias handling and clarification for conflicts is the stated working assumption after an optional question received no answer.

**Immediate next step:** Stage 7 supported answers with citations, including the team's EV-specific prompt and preservation of the returned evidence's source/version/review labels. See [Stage 6 run instructions](STAGE_6_HANDOFF.md). Stage 7 has not started.

The user's earlier decision to defer manual source review and question-writing until the full prototype is built still applies. Those tasks do not block development stages 2–10; they remain required before formal evaluation and submission. Technical checks must pass before advancing stages. All source acceptance flags remain false, current status remains unknown, and prototype evidence is labelled unverified.

Deferred review batch: verify the source text and applicable document chains; record actual reviewers/dates; independently author and verify the 24 evaluation cases; resolve current-benefit evidence gaps or keep unsupported claims explicitly unanswered. Freeze expected answers before formal evaluation. Do not invent review completion or remove these obligations from final acceptance.

## Stage 6 technical closeout — 25 September 2026

Added notebook routing and retrieval cells using Lab 4's metadata-filtered retriever. Canonical aliases are explicit; questions with conflicting or multiple recognized jurisdictions request clarification before search. Only the two indexed states and Central are selectable. Recognized unsupported jurisdictions and explicit requests outside the Central buyer pilot stop without retrieving. Word-boundary/uppercase checks avoid treating ordinary lowercase “up” as Uttar Pradesh.

Added `data/retrieval_rules.json` with 20 hash-checked page rules, core restriction pages and targeted exclusion offsets. Context expands seed pages by one adjacency hop and follows mandatory links to completion with cycle detection. Known superseded passages and bus-only annexure portions are omitted from context without editing the stored corpus. Unaffected conditions and original page citations are retained as exact slices with stable excerpt IDs and hashes. Missing/cross-jurisdiction required evidence raises an error; an exceeded budget returns no partial context.

Observed results: **eight notebook checks and 19 repeatable retrieval checks passed**. Eight live queries across all three choices had no leakage; 20 invalid/conflicting/unsupported input cases stopped before search. All 20 page rules were exercised. Required Maharashtra circular/corrigendum context, Tamil Nadu's tax-only extension and historical demand/fee deadlines, and Central's latest category rows, funding/claim restrictions and L5 closure remained available. Excluded spans were absent. Query embeddings were used only for questions, never the corpus. Observed live contexts had 5–15 pages and 11,619–28,899 characters, below the explicit 50,000-character ceiling.

Fault checks covered missing/cross-jurisdiction links, altered seed text, changed exclusion hashes/inputs/model, empty search and context overflow. A fresh Jupyter kernel passed Stage 5 reopen plus Stage 6. Earlier ingestion artifacts reproduced byte-for-byte; Stage 5's 16 persistence checks still passed. No dependency, source, chunk or main index change was required.

Outputs: [rules](data/retrieval_rules.json), [notebook checks](data/processed/search/stage6_checks.json), [retrieval checks](data/processed/search/stage6_retrieval_checks.json), [repeatable check script](checks/stage6_retrieval_checks.py) and [handoff](STAGE_6_HANDOFF.md). Reports remain tied to the tested notebook, corpus and inputs.

AI assistance: implementation, pilot-specific source-version/exclusion rules, technical checks, actual local searches, documentation and Git publication. The rules and sources are still pending team acceptance. Alias matching is an explicit English-name baseline, not general place/intent recognition. Relevance/answerability, generated answers, citation rendering, UI and formal evaluation remain later work. Current-entitlement permission remains false.

## Stage 5 technical closeout — 25 September 2026

Added notebook cells reusing the course's Ollama embedding, persisted Chroma, document insertion and retriever patterns. The index loads all saved pilot chunks with stable IDs, retains their full metadata, and stores a corpus/model receipt only after the build validates. Normal open checks that receipt and every saved record without embedding the corpus. Missing, incomplete or changed indexes require an explicit rebuild; re-running startup never silently ingests data.

Observed results: **231 records (53 Maharashtra, 78 Tamil Nadu, 100 Central), 768-dimensional finite nonzero vectors, eight passed notebook checks**. The unfiltered e-voucher smoke query retrieved Central operational-guideline pages 16, 14 and 15. These are technical search observations, not policy-answer evaluation or evidence of current eligibility.

The committed `checks/stage5_index_checks.py` passed **16 persistence/integrity checks**. A separate Python process reopened all 231 records with document embedding forbidden: zero embedding calls before search, zero corpus embeddings afterward, and one query embedding. Rebuild/change/corruption tests use six real chunks in isolated temporary stores; interruption testing stops after a 32-record batch. Rebuilds remove stale entries, preserve changed metadata and do not duplicate IDs. Invalid inputs leave the old index intact; a failed build cannot leave a valid completion receipt and recovers by rebuilding.

A fresh Jupyter kernel passed Stage 5 with `rebuild_index = False`. All six earlier page/chunk files remain byte-identical after rerunning Stages 2–4. Reports contain current notebook hashes; the canonical notebook has no saved outputs. Dependencies, source records and PDFs are unchanged.

Outputs: ignored local `data/chroma/` database/build receipt; [notebook checks](data/processed/search/stage5_checks.json), [persistence checks](data/processed/search/stage5_persistence_checks.json), [repeatable check script](checks/stage5_index_checks.py) and [handoff](STAGE_5_HANDOFF.md). The database is recreated from committed chunks on a fresh checkout, using a deliberate build.

AI assistance: implementation, persistence/integrity tests, actual local embedding/search runs, documentation and Git publication. All source acceptance/current-entitlement flags remain false. No jurisdiction filter, amendment-aware context assembly, generated answer, formal evaluation or UI was added. Those stages and the consolidated human review remain pending.

## Stage 4 technical closeout — 25 September 2026

Selected PM E-DRIVE's two-/three-wheeler buyer-incentive scope, with the original notification, operational guidelines, applicable amendments and dated closure/claim notices. Ten PDFs downloaded from official production-portal links on 24 September retain original bytes and dates. The bounded source review records the unconfirmed scope assumption, source exclusions, later-update requirements and current-entitlement gaps. No state-plus-central benefit stacking is implied.

Added Stage 4 cells that reuse the shared loader and course splitter. A small loader extension trims four mixed-language pages at recorded English headings and retains raw-text hashes. Five OCR proposals supply missing text/amounts from the newest amendment and scanned letters, with original-page citations and false acceptance flags. Historical/specialist pages remain in the audit; dated exceptions are not current claims windows.

Observed results: **53 unique audit pages, 35 draft pages, 100 chunks, 13 passed notebook checks**. Critical checks preserve the latest e2w table/caps/years and 15% limitation, the e-rickshaw table, L5 closure, fund limitation, distinct claim deadline and buyer/e-voucher requirements. Required amendment/conditions references resolve. Nine invalid-input tests reject source/hash/page/OCR/marker problems. The original six state-source records and four state JSONL files are unchanged.

Fresh Jupyter kernels passed Stage 4 independently and Stages 2–4 together, without API keys or model services. All six JSONL artifacts reproduced byte-for-byte, report notebook hashes match, and saved notebook outputs remain empty.

Outputs: [page audit](data/processed/central/pages.jsonl), [draft chunks](data/processed/central/chunks.jsonl), [check report](data/processed/central/stage4_checks.json), [source review](data/policies/central/SOURCE_REVIEW.md) and [OCR provenance](data/ocr/central/review.json). Earlier check reports are refreshed for the current notebook/manifest. No model calls, embeddings, index, generated answers or evaluation cases were added.

AI assistance: scheme/source research, official downloads, targeted visual/text comparison, OCR/proposed transcription, notebook implementation/checks, technical verification, documentation and Git operations. Four central team-written expected-answer cases, genuine OCR/source acceptance and unresolved funding/eligibility checks remain pending. Technical completion does not certify current entitlement or full coverage of specialist PM E-DRIVE segments.

## Stage 3 technical closeout — 24 September 2026

Added Tamil Nadu's 2023 policy booklet and the 29 December 2025 motor-vehicle-tax notification from official government hosts. The manifest selects policy physical pages 6–27 and notification page 1. Source dates, hashes, review scope and unresolved status checks are recorded in [the source review](data/policies/tamil_nadu/SOURCE_REVIEW.md) and research log. The tax order's 2026–2027 period is kept separate from the purchase-incentive/fee-waiver deadlines; no blanket current-entitlement claim is enabled.

Moved the existing loader/imports into a shared notebook cell. Maharashtra still uses the same extraction path. Tamil Nadu selects layout extraction on three table pages and normalizes whitespace without rewriting values. Its recursive splitter uses 1000/200 with two extra section separators to preserve public/private charging blocks. Conditions, policy-period and tax-update page links survive splitting.

Observed technical results: **23 Tamil Nadu pages, 78 chunks, 12 passed notebook checks**. Five demand rows, their units/caps/counts and linked conditions/deadline are preserved; charging/swapping tables and the later tax clause retain their scope. Six invalid-input tests reject bad hashes/counts, duplicate or out-of-range pages, empty selection and duplicate sources. Both jurisdictions retain distinct IDs/state values. Maharashtra's JSONL files and original four manifest source records are unchanged.

Fresh Jupyter kernels passed both Stage 3 alone and Stages 2–3 together without Stage 1 services or keys. All four JSONL files reproduced byte-for-byte; both report notebook hashes match the saved notebook. Canonical notebook outputs remain empty.

Outputs: [pages](data/processed/tamil_nadu/pages.jsonl), [chunks](data/processed/tamil_nadu/chunks.jsonl), [check report](data/processed/tamil_nadu/stage3_checks.json). Stage 2's check report was refreshed for the shared notebook revision. No new dependency, model call, embedding/index, generated answer, UI or evaluation case was introduced.

AI assistance: official-source research/downloads, targeted PDF visual/text comparison, source records, loader adaptation, Stage 3 cells/checks/exports, execution and failure checks, documentation and Git operations. Independent source research was attempted but its agent stopped at a usage limit; the main session completed the PDF inspection and validation. Manual review, complete amendment verification and two team-authored Tamil Nadu cases remain deferred. This completes technical Stage 3, not final source acceptance.

## Stage 2 technical closeout — 24 September 2026

Replaced the separate worked examples with one complete notebook path using the confirmed course patterns: page loading/inspection from Lab 4, `Document` metadata from Exercise 2, and the recursive splitter at 1000 characters with 200 overlap. Added explicit PDF/proposal hash checks, original physical-page citations, optional document relationships and stable chunk IDs. No dependencies or Stage 1 code cells changed.

The loader reads ten English policy pages and the eight explicitly mapped OCR proposals. All 18 records remain in `pages.jsonl`; the August old-wording and distribution-only pages are excluded from `chunks.jsonl`. Base page 19 keeps unaffected provisions and a section-specific link to the August replacement. Table conditions and page continuations are linked without combining their citations.

Observed results:

| Check | Result |
|---|---|
| Complete Stage 2 in a fresh Jupyter kernel | Passed without Stage 1, API keys or model services |
| Unique page records | 18: base policy 10, June 4, July 1, August 3 |
| Pages included in draft chunks | 16; two August audit-only pages excluded |
| Draft chunks | 53: base policy 32, June 15, July 3, August 3 |
| Notebook technical checks | All 12 passed; saved in `stage2_checks.json` |
| Critical evidence | Table 2's ten rows/units and linked conditions, Table 3 and its cost exclusion, June clause 6 continuation, August replacement preserved |
| Provenance and status | Original PDF citations, relationship targets, source/proposal hashes and unverified flags retained through splitting |
| Loader failure cases | All 14 passed: missing/duplicate pages, invalid page numbers, mismatched source/role/hashes, duplicate sources/candidates and wrong PDF page count |
| Repeatability | A separate fresh run reproduced both JSONL files byte-for-byte |

Outputs: [page audit](data/processed/maharashtra/pages.jsonl), [draft chunks](data/processed/maharashtra/chunks.jsonl), [technical check report](data/processed/maharashtra/stage2_checks.json). The report records evidence chunk IDs, artifact hashes and the notebook hash at export. Reruns replace only these derived outputs. No embeddings, index, generated policy answers, UI or evaluation cases were added.

Technical Stage 2 is complete; final team acceptance is deferred. The OCR loader deliberately uses proposals and cannot promote them to accepted text merely by changing a reviewer flag. Later retrieval must follow evidence links, and future team corrections require regenerated chunks and repeated checks. Current-benefit availability through the agreed cutoff remains unverified.

AI assistance: implementation of the Stage 2 loader, metadata relationships, splitting, assertions and exports; independent chunk/loader review; execution checks; documentation and Git operations. The team did not author or verify these results as human review. The sections below preserve earlier checkpoints; their incomplete-work descriptions are historical and superseded by this closeout.

## Stage 2 continuation — OCR worked example

Added a separate example for the August corrigendum's physical page 2. It reads the explicitly mapped proposed text, checks the original-PDF and proposal hashes, and keeps the original PDF/URL as the citation target. The text file/hash are recorded separately. Metadata preserves the replacement role, amended source/section and all pending-review/current-status restrictions; it does not inherit the base policy's title, date or page-19 link.

Observed checks: all Stage 2 cells run in a fresh namespace without model calls or key access. The OCR proposal contains 1,881 characters (1,880 stripped), matches its recorded hash and source/page mapping, and retains the replacement text markers. The original ten policy records remain unchanged. Notebook schema/syntax pass, earlier cells are unchanged, outputs are clear. A read-only independent check confirmed original PDF length and both hashes.

This adds one worked OCR example, not the eight-page OCR pipeline. The team still needs to handle optional June/July/August relationship fields, assemble 18 unique records, distinguish old/replacement/distribution roles, link cross-page evidence and implement/check splitting. Manual review remains deferred. AI assistance: bounded example, provenance checks, independent review and extension guidance; no generated policy answers or evaluation cases.

## Stage 2 continuation — English page records

Extended the bounded loading example to physical pages 16–25, using the manifest's candidate list and Exercise 2's list/`Document` pattern. Each page receives an independent metadata dictionary. Removed page-specific fields from the shared template; only page 18 carries its conditions link to page 19. The earlier page-18 example is not added a second time.

Observed checks: all Stage 2 cells execute in a fresh namespace without Stage 1 services or key access. Ten unique, nonempty records match their original PDF pages; source path/URL and review/status flags are preserved. Metadata dictionaries are independent, page 18 matches the earlier example, notebook syntax/schema pass and saved outputs are empty. Earlier notebook cells, PDFs and dependencies are unchanged. Character counts are diagnostic; extraction whitespace differs slightly from the earlier manifest measurements.

This is the English-page checkpoint only. Eight OCR page records, document relationships, chunking and table/continuation checks remain. Manual review stays deferred. AI assistance: bounded example extension, independent review and execution checks; no evaluation examples or generated policy answers.

## Stage 2 start — one-page worked example

Added an AI-assisted example loading the original policy's physical page 18 with `pypdf.PdfReader`, then applying Exercise 2 cell 9's `Document` metadata pattern. Lab 4's load/inspect sequence is reused; the page-preserving reader is an explicitly disclosed addition. It retains the original PDF/URL, page 18, a conditions-page link to page 19, document identity/date, cutoff and all unverified/acceptance restrictions.

Observed checks: notebook schema and code syntax pass; both new code cells run in a fresh namespace without the Stage 1 model setup; the page returns 1,728 characters and the incentive-table heading/units checks pass. Stage 1 code and dependencies are unchanged. Saved notebook outputs are empty. This is one runnable example, not completion of the 18-record loader or proof that table chunks are correct.

Remaining technical work: complete loading and metadata for all 18 records, preserve amendment relationships and distribution-only roles, split and inspect tables/conditions/continuations, and record actual results. No embeddings, index, generated policy answers or evaluation examples were added. AI assistance in this step: bounded worked example, execution checks and review guidance. Team acceptance remains deferred.

## Stage S preparation closeout — 24 September 2026

Completed the remaining preparation as one batch:

- Compared base-policy English pages 16–25 with extracted text; recorded table fields, source inconsistencies and page continuations.
- Completed proposed corrections for all five circular pages and prepared/compared all three corrigendum pages. Eight raw/proposed pairs are mapped to source PDFs and hashes. [Text review](data/ocr/maharashtra/TEXT_REVIEW.md) explains changes and uncertainties.
- Recorded the toll amendment's old/replacement page roles and the July circular's relationship to June. Original PDFs, earlier raw OCR, setup notebook and dependencies are unchanged.
- Finished a bounded follow-up official-source search and saved [research findings](data/policies/maharashtra/research_log.json). The existing public portal snapshot is dated 23 September; follow-up research is dated 24 September. No backdated observation or current-entitlement verification was inferred.

Remaining requirements: actual team text review; confirmation of applicable later amendments/current availability; portal launch/deadline evidence if answering historic claim deadlines. A reported later claim-window extension was not verified from an official circular. No current-entitlement claim is allowed. Unknown status and all false team/ingestion-acceptance flags are retained in the manifest.

Validation: original PDF hashes/page counts, earlier raw OCR hashes, all eight proposal hashes/page mappings, JSON consistency, local document links, notebook unchanged/outputs empty, secret exclusion and the focused Git diff checked before publication. No model calls or application tests were needed for source/data documentation changes.

AI assistance: OCR, visual/text comparison, proposed corrections, official-source research, provenance/status records, Stage 2 handoff and Git operations. No EV pipeline, student-written evaluation questions, human-review claims or policy-answer results were produced.

The sections below are earlier checkpoints. Their pending steps and next-page instructions describe the state at that time; the current checkpoint above supersedes their work ordering.

## Stage S subtask: June circular page 1 comparison

Status: **proposed corrections prepared; human verification pending**. Compared the full rendered page at 300 DPI with the OCR draft. Saved a separate proposed transcription and [change notes](data/ocr/maharashtra/2025-06-19/page-1-review.md); original PDF and raw OCR remain unchanged. Header/date/reference corrections and an eligibility-word correction are proposed. The non-policy file-path footer is explicitly omitted from the proposed text.

Corrected an earlier AI review note: the scan appears to print the rules year `१९५९`, so the proposed transcription retains it. The previous definite instruction to replace it with `१९८९` was withdrawn; the analogous page-2 instruction is now an unresolved comparison item. Legal-reference clarification remains separate from transcription.

Proposal provenance and hashes are recorded in `review.json`. No human reviewer, review date or accepted text was invented; all acceptance flags remain false. Original-file hashes, proposal metadata, local links and the focused diff were checked. Stage S step 3 remains active, and no later-stage work was started.

AI assistance: visual source comparison, proposed transcription corrections, correction log and Git checkpoint. The team must still verify the complete page, including minor glyphs and contact text.

## Stage S subtask: Maharashtra circular OCR preparation

Date: 23 September 2026. Status: **preparation complete; team verification pending**. The user accepted the recommended bounded OCR session after the source checkpoint. Stage S remains incomplete and Stage 2 has not started.

Prepared [five page-matched drafts and a review checklist](data/ocr/maharashtra/README.md) for the June and July circulars. [Review records](data/ocr/maharashtra/review.json) preserve source/draft hashes, engine/model settings, observed errors and empty reviewer fields. The original PDFs are unchanged; all ingestion-acceptance and team-verification flags remain false.

Observed checks:

- Local Tesseract 5.5.3 was available. Downloaded the official Marathi model at a recorded commit into ignored `tmp/`; used the installed English model. No Python dependencies changed.
- Rendered all five pages at 300 DPI and ran `mar+eng` OCR. Every page produced nonempty text with its own source/page mapping.
- Compared draft text with the scans. Header dates, handwritten numbers, the rules year and signatory text contain errors; these are recorded for correction. June page 3 used a second segmentation setting to keep clause numbers beside their paragraphs. This was an AI spot check, not full human verification.
- Original-PDF and draft hashes, page coverage, JSON records, acceptance flags and local document links were checked before publication. The setup notebook was not changed.

Next action: the team checks each full page and saves corrections with reviewer/date, following the OCR checklist. A separate source-stage continuation still needs to review the August corrigendum text and establish the applicable amendment/status evidence through the cutoff. Do not begin ingestion from unchecked drafts.

AI assistance in this session: local OCR setup/execution, page mapping, visual spot checks, error records, review guidance and Git operations. No EV application code, policy answers or evaluation ground truth was produced.

## Stage S: Maharashtra source review

Date: 23 September 2026. Status: **incomplete; research checkpoint saved**. The user agreed Maharashtra as the first pilot and 23 September 2026 as the verification cutoff. Stage 2 ingestion has not started.

Saved four official PDFs (33 physical pages total), a [source manifest](data/source_manifest.json), [review notes](data/policies/maharashtra/SOURCE_REVIEW.md), and [public status evidence](data/policies/maharashtra/status_evidence.json). The packet includes the 23 May policy, 19 June and 28 July operational circulars, and 29 August corrigendum. Document dates were distinguished from website upload dates.

Observed checks:

- All four files open with `pypdf`; page counts and SHA-256 hashes are recorded. Main-policy pages 18–19, all five circular pages, and corrigendum pages 1–2 were rendered and visually inspected.
- The English incentive table is readable before splitting. June's text layer garbles Marathi; July returns no text; the corrigendum also needs Marathi character checks. No source is yet marked accepted for ingestion.
- The official transport listing links to the MHEV portal. Saved public responses have dated registration totals and vehicle-type counts, but do not establish current funding, approved/paid claims or individual entitlement. The announcements request returned HTTP 401; no authentication was attempted.
- The known documents' relationships are recorded. Completeness of the amendment chain and current availability through the cutoff remain unresolved. No current-entitlement claim is approved from this packet.

At this checkpoint, text preparation was pending. The later OCR session above records the user's accepted approach and its results. Official status/amendment review remains open. Once source acceptance checks pass, begin the team's Stage 2 ingestion work using the existing reuse map. Do not interpret the saved checkpoint as source-stage completion.

AI assistance in this stage: official-source discovery, original-document downloads, visual and text-extraction review, provenance/status records, planning updates and Git operations. These are research notes awaiting team verification, not human-verified evaluation answers. No application code, OCR, index or policy evaluations were added.

## Stage 1: environment preflight

Date: 23 September 2026. Status: **complete**. The full setup notebook passed, including an authenticated Groq request. Stopped at this stage before source verification and ingestion.

Completed setup:

- Created a Python 3.12 environment with pinned classroom dependencies and `uv.lock`. The project lock was seeded from the course lock and resolved for this smaller dependency set.
- Added a setup-only notebook adapting the course imports, dotenv, Ollama embeddings and Groq initialization. Exact source cells are listed in the notebook.
- Added `.env.example`, secret-file ignore rules and setup instructions. Notebook outputs remain empty in Git.

Observed checks:

| Check | Result |
|---|---|
| Interpreter | Python 3.12.14 |
| Notebook schema and code syntax | Passed |
| Direct dependency versions | Matched project pins |
| Installed package compatibility | Passed `uv pip check` |
| Real Jupyter kernel and setup imports | Passed |
| Local `nomic-embed-text` query embedding | Passed: 768 finite values |
| Groq `openai/gpt-oss-120b` request | Passed in the notebook: returned `OK` |
| Policy loading, indexing and answer evaluation | Not started; later stages |

The user configured the key in the local `.env` file. It remains excluded from Git, and the committed notebook has no saved outputs or credentials. The successful run required no application-code changes.

At this checkpoint, the next action was to agree the cutoff and first pilot, then begin source verification. Those choices and the later source-stage work are recorded above. Central scheme selection remains part of central-source review.

AI assistance in this stage: environment configuration, setup-cell adaptation, setup checks, documentation and Git operations. The team still owns the policy corpus, EV-specific implementation, prompt and human-verified evaluation questions.
