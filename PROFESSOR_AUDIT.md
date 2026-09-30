# Professor requirement audit — 30 September 2026

**Technical audit completed with two repairs. Final submission is not ready.** The application runs from a fresh environment and its automated checks pass. Team review, independent evaluation, the presentation and uploads are still outstanding. Passing development checks cannot guarantee marks or establish general answer accuracy.

The authority is the attached **Assignment3_MiniProject_Instructions (1).pdf**, both pages. The proposal and staged guide add project commitments; they are distinguished below. The user reports the final deadline as **1 October 2026**. Its time and the live-demo date have not been supplied. Preserve the submitted GitHub revision after the actual deadline.

## Professor's requirements

| Requirement and PDF location | Result | Evidence or remaining action |
|---|---|---|
| Group of three; §1, p1 | User-reported exception | The proposal lists four members. User confirms professor approval for four. |
| RAG with a custom dataset and problem; §3, p1 | Implemented | EV problem statement; 34 official source PDFs; 308 selected page records; 804 chunks; filtered retrieval, grounded generation and UI. Dataset acceptance is still pending. |
| Agents optional; §3, p1 | Satisfied without agents | Single-jurisdiction workflow. Comparisons were explicitly deferred. |
| Idea PDF includes names/IDs, problem and rationale, approach, stack; §4, p1 | Content passed | All four categories are present in the supplied idea PDF. |
| Every member uploads the idea PDF by 22 September EOD; §4, p1 | Unverified | Obtain each member's actual Digiicampus receipt; no upload or timely-submission claim is made. |
| Project GitHub link; §5, p1 | Passed access/setup audit | [Public repository](https://github.com/mohit6603/Electric-vehicle-Policy-RAG). Anonymous download, fresh environment, explicit index build and restart checked. |
| Exactly three slides; §5, pp1–2 | Missing | Slide 1 business impact; slide 2 technical stack and GenAI architecture flow; slide 3 appendix including actual AI use. No final slide file is present. |
| Every member submits final ZIP; §5, p2 | Missing/unverified | ZIP must contain the repository link and three-slide presentation. ZIP and individual upload receipts are absent. |
| Eight-minute presentation/live demo, about 3–4 minutes Q&A; §6, p2 | App tested; rehearsal pending | Local browser and actual model responses checked. Team timing, explanation and live-demo date are not verified. |
| Mainly classroom stack/syntax; explain additions; §7, p2 | Reuse established; oral explanation pending | [Exact course-code map](REQUIREMENTS_AND_REUSE.md). Python/LangChain/Ollama/Chroma/Groq/Gradio match the class patterns. Team must explain page/hash checks, review metadata, evidence links, JSON parsing, error handling and the launcher/evaluation scripts. |
| AI only as code helper; 30% flat penalty for detected AI-generated code; §8, p2 | Exception reported, wording unverified | User says professor approved broader AI implementation and will provide the wording. It has not been supplied, so the permitted scope cannot be checked. User implementation permission and Git authorship do not establish an instructor exception. |
| Brief AI disclosure in appendix; §8, p2 | Missing with slide 3 | Disclose the actual research/OCR assistance, implementation, debugging, development questions/output review, documentation and Git assistance recorded in progress. Do not describe the work as only minor autocomplete. |
| Demo main grading; technical 80%, presentation/narrative 20%; §9, p2 | Recorded | No score forecast; technical checks do not cover the team's presentation or understanding. |
| Late upload by any member or GitHub changes after deadline can penalize whole group, including zero; final note, p2 | Team action pending | Confirm the announced time, submit for every member, save receipts and the submitted commit, then stop repository changes after the deadline. |

The professor PDF does **not** prescribe 24 cases, a minimum accuracy, hosting, agents, a video, a test framework or an additional report. Those must not be presented as separate grading rules.

## Proposal and agreed-plan commitments

| Commitment | Status |
|---|---|
| Original proposal: 8–10 states plus Central | User agreed seven states plus Delhi (NCT), and Central. All nine choices are implemented. This is a documented scope change; professor acceptance of that wording has not been verified. |
| Benefits verified through the agreed 23 September 2026 cutoff | Not complete. All 34 source acceptance flags and current-entitlement permissions remain false. Official-source status gaps are recorded in each jurisdiction's source review. Later collection dates do not certify availability at the cutoff. |
| State/year/page metadata, persistent index, filtered retrieval, sources and abstention | Implemented and development-tested. A valid page citation alone does not prove an answer interprets that page correctly. |
| Proposal: 20–30 questions written by the team; guide: 24 cases | Not complete: all 24 question slots are empty. The freeze command correctly refuses incomplete review; zero formal cases have run. [Team workflow](evaluation/README.md). |
| Proposal's one-line answers | UI returns up to six concise cited points to retain conditions and periods. This differs from the literal one-line phrasing; present the actual behavior. |

## Checks and repairs

Evidence is saved in [checks/professor_audit](checks/professor_audit). These are AI-assisted development observations, not independent team evaluation.

- Downloaded public commit `4b85eedd788b20e83b702ebc92a93dbe5d7d4167` anonymously; all 285 tracked files matched. Installed the locked dependencies in a new virtual environment (220 compatible packages), built the 804-record index using the existing local Ollama service, and reopened it. This is a fresh environment on the same Mac, not a second-machine test.
- On that published version, the 184 existing checks passed. The browser then exposed a real factual error: the generic Central e-2W example applied the earlier rate/cap too broadly. The failed response is retained in `browser_before.json`.
- Updated the prompt to keep each table period with its rate/cap. Two actual repaired browser responses were compared with physical page 3 of the supplied 10 August 2026 Central amendment: the generic query distinguished FY 2024–25 from 1 April 2025–31 March 2028; the explicit-period query selected the latter column. Both cited that page. This targeted repair is not proof that every policy answer is correct.
- In six repaired browser submissions, both supported answers, unrelated-question abstention, current-entitlement refusal, jurisdiction mismatch and blank-input handling behaved as expected. Nonanswers cleared sources; Clear reset inputs/outputs; all nine choices were visible. Startup made no corpus/query embeddings; the submissions made three query embeddings and zero corpus embeddings.
- Fixed ingestion so actual recorded source/OCR reviews can survive loading and splitting. Previously hard-coded pending flags/assertions prevented the accepted-review path. Reviewer names, valid non-future dates, Boolean flags and source/page consistency are checked. Legacy pending OCR records without an acceptance flag remain unaccepted. AI-origin text remains labelled as such after review.
- All **196 automated checks** passed after the patches: persistence 16, retrieval 19, citations 14, failures 50, UI 15, UP 10, Delhi 9, Gujarat 11, Telangana 10, Karnataka 11, MP 10, evaluation gates 9, review transitions 12. Synthetic review records stay in memory and do not accept the real corpus.
- All **117 ingestion assertions** passed on the real pending-review files. All 18 page/chunk JSONL files reproduced byte-for-byte; ingestion receipts were refreshed. No corpus rebuild was needed for these code-only repairs.
- Notebook schema and all 68 code-cell syntaxes passed; saved outputs are empty. All 34 original PDF hashes match. Common credential-pattern scanning found no matching tokens/private keys in tracked files; `.env`, virtual environment and local index are excluded. This is bounded scanning, not an exhaustive security audit. Existing commits use the authorized Mohit Patle identity without LLM coauthor trailers.

The patched checks ran in the fresh export with the changed notebook/check files overlaid. Reports record their file hashes and scope; they must not be read as tests of an unchanged earlier commit.

## Finish in this order

1. Supply the professor's actual AI-approval wording and confirm the deadline time/demo date from the announcement. Keep the four-member approval evidence with the team.
2. Complete actual source/OCR and prompt review, resolve the recorded policy-status gaps for the intended claims, then author the independent cases from the original PDFs. Record real names/dates. Re-ingest, explicitly rebuild if artifacts change, freeze, run and grade the two evaluation batches.
3. Prepare the three-slide deck, including truthful disclosure and measured results only. Check its exact slide count and contents.
4. Rehearse the eight-minute demo and Q&A on the final revision, including startup, a supported question and a refusal. Recheck setup after any substantive changes.
5. Put the deck and repository-link file in the ZIP, inspect the ZIP contents, upload from every member's account before the actual deadline, and retain receipts and the final commit. No upload has been performed by this audit.

This file is a review record, not the team's final presentation or a claim of professor approval.
