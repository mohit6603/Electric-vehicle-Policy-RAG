# Project checkpoint

## Current stage and next step

**Next working stage: 2 — Maharashtra extraction tests.** No Stage 2 application code has been written. Stage S's technical preparation batch is finished; full source acceptance and current-benefit verification remain open. This is not an unconditional Stage S pass.

| Stage | Current status |
|---|---|
| 1. Environment preflight | Complete |
| S. Maharashtra sources | Preparation/AI comparison finished; team acceptance and current-status verification pending |
| 2. First-state ingestion | Ready for candidate-text tests only; acceptance criteria still apply |
| 3–15 | Not started |

**Latest decision:** defer the user's manual source review and question-writing until the full prototype is built. Those tasks no longer block development stages 2–10; they remain required before formal evaluation and submission. Technical checks must still pass before advancing stages. Keep source acceptance flags false, preserve unknown current status, and label prototype evidence as unverified.

**Immediate next step:** the team provides its Stage 2 loading/metadata/splitting code in the notebook, as it confirmed under the helper-only scope. Assistance then reviews, debugs and runs the technical checks from [STAGE_2_HANDOFF.md](STAGE_2_HANDOFF.md). Do not ask for manual source sign-off first. No Stage 2 implementation has been supplied yet.

Deferred review batch: verify the source text and applicable document chains; record actual reviewers/dates; independently author and verify the 24 evaluation cases; resolve current-benefit evidence gaps or keep unsupported claims explicitly unanswered. Freeze expected answers before formal evaluation. Do not invent review completion or remove these obligations from final acceptance.

AI assistance in this update: recorded the user's revised ordering only; no application code, policy verification or evaluation results were added.

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
