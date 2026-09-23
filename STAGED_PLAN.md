# EV Policy Assistant: proposed stages

Status: stage-wise work approved by the user on 23 September 2026; Stage 1 environment preflight started. Source of scope: IMPLEMENTATION_GUIDE.md, with REQUIREMENTS_AND_REUSE.md for exact classroom references and assignment constraints. The four-person group is approved as reported by the user. AI assistance remains helper-only: the team implements and verifies the work; assistance supports explanation, review and debugging. See `PROGRESS.md` for actual checks and the next checkpoint.

Confirmed choices: target 30–45-minute sessions; one state or Central per query; defer comparisons. Coverage: Maharashtra, Tamil Nadu, Uttar Pradesh, Delhi (NCT), Gujarat, Telangana, Karnataka and Madhya Pradesh. The user explicitly accepts seven states plus Delhi as the eight jurisdictions; this is a clarified scope adjustment to the proposal's literal state count, not an independently verified instructor exception. Verify benefits current through a fixed date still to be agreed. Select the central scheme and its documents during central-source review.

## Session sizing

Each numbered row targets one 30–45-minute session; stage 10 repeats for one additional jurisdiction at a time. Because current benefits must now be verified, source research is a separate repeatable session before a jurisdiction's ingestion session. Downloads, dependency failures, source research and model-service availability can require a separate narrowly scoped continuation; elapsed time does not predict account usage reliably. Pilot jurisdictions are to be selected from the agreed list based on readable official PDFs, not assumed here.

Work on one agreed stage or batch at a time. Do not automatically continue to the next stage. If an external prerequisite fails or the stage grows, preserve the evidence and open a narrowly defined repair session. A saved checkpoint can be incomplete; it must not be labelled done until its checks pass.

## Source verification: a separate repeatable stage

Run one **Source verification session (S)** for each pilot state, central scheme, and later added jurisdiction, before its ingestion session. This separation keeps current-policy research from consuming the implementation session. For central, first select the buyer-relevant scheme(s) for the agreed cutoff.

Covers: official policy and relevant amendments, extensions, replacement documents and official status evidence through the cutoff; effective/expiry dates; provenance; extraction feasibility. Done means a saved source packet explains the applicable document chain and status with official references, flags unresolved points explicitly, and supplies readable evidence for ingestion. A dated policy PDF by itself is not sufficient verification of current benefits. Where status cannot be verified, preserve the limitation and ensure later answers do not assert active entitlement. An unresolved required source check stays incomplete rather than being labelled verified.

Dependencies: agreed cutoff, jurisdiction and scheme scope; no application code required. Output: source packet and evidence/status record. Research the first state's packet after stage 1, the second and central packets before stages 3 and 4, then one remaining packet before each stage-10 session. If one packet exceeds the session, stop at a saved research checkpoint with the exact unresolved document/status question; do not start ingestion on an unverified claim.

## Proposed implementation order

| Stage | Covers and standalone output | Done means | Dependencies |
|---|---|---|---|
| 1. Environment preflight | Python 3.12/classroom dependency baseline, notebook startup, Ollama embedding and Groq connection smoke checks | Required imports succeed; a small embedding and model invocation work; setup steps and secret configuration are recorded without exposing keys | Available local services and credentials; approved session plan |
| 2. First-state ingestion | First verified source packet, source manifest, extraction, metadata and recursive splitting | A checked incentive table retains its amount/units/conditions; inspected chunks retain state, policy year, document and correct page; required amendments remain traceable; two human-verified question/answer examples are saved | 1 and S for the first pilot state |
| 3. Second-state ingestion | Process a second state's verified source packet through the same path | Source records, checked tables and page metadata work for the second state; two further human-verified questions are saved | 2 and S for the second pilot state |
| 4. Central-source ingestion | Process the verified documents for the scheme selected during central-source review | Central evidence is labelled separately; source/date scope is recorded; four human-verified central questions are saved | 2 and S for central; can run before 3 |
| 5. Persistent semantic search | Embed the pilot chunks, ingest all of them into Chroma, search from a notebook, reopen the index | Saved counts match accepted chunks; restart avoids corpus re-embedding; agreed rebuild/update process introduces neither duplicates nor stale chunks | 3 and 4; rebuild versus incremental-update choice resolved |
| 6. Jurisdiction-aware retrieval | State-filtered retrieval, separate central selection, applicable source versions and agreed handling of selection/question conflicts | Retrieved metadata shows no leakage across both pilot states and central; amendments needed for the answer remain available; superseded evidence is not treated as current; unsupported or conflicting inputs follow the agreed clarification behavior | 5; state-name handling agreed |
| 7. Supported answers with citations | Groq generation from labelled retrieved evidence, concise answer and traceable sources | Pilot examples preserve amounts, units, caps and conditions; answers expose the verified cutoff/status; displayed state/document/page references support the answer | 6; students author the EV-specific prompt |
| 8. Abstention and failure behavior | Empty or irrelevant evidence, unsupported questions, ambiguous input and service/index/key failures | Observed negative cases return an appropriate clarification, abstention or actionable error; prior supported examples still work | 7 |
| 9. Gradio pilot | State/Central dropdown, question input, answer and sources through a small callback | Supported, unsupported and mismatch cases work through the UI; startup opens the saved index without rebuilding it; outputs keep a consistent shape on errors | 8; notebook launch versus optional app.py decision |
| 10. Add one remaining jurisdiction (repeat) | One additional verified source packet through ingestion, indexing and UI spot checks | That jurisdiction has working coverage, complete source records and two human-verified questions; repeat for the six remaining jurisdictions | 9 and S completed for that jurisdiction |
| 11. Evaluation preparation and first batch | Audit the complete team-written expected-answer set, freeze it, and run approximately half of the cases | Expected answers are independently verified before execution; first-batch retrieval, answer and citation results are saved separately with triaged failures | All stage-10 repetitions complete |
| 12. Second evaluation batch and findings | Run the remaining cases on the same recorded app/corpus version; compile results | Every case has real observations; report counts/denominators and classify failures; identify bounded repair work before release | 11 |
| 13. Reproducible repository | Setup/run instructions, source availability, environment record, course attribution, assistance log and reviewer access to the intended GitHub revision | A fresh start reproduces a supported answer and an abstention; setup matches the project; the intended reviewer can access the code and sources; keys are excluded | 12; required-behavior failures fixed and affected cases rechecked |
| 14. Required three-slide deck | Exactly three slides: business impact; stack and architecture flow; appendix including actual AI usage | Correct count/order; architecture reflects the implemented app; any reported results are observed; disclosure accurately describes assistance | 13 |
| 15. Rehearsal and submission package | Timed live demo, Q&A preparation, final ZIP with deck and GitHub link | Rehearsal fits eight minutes with separate 3–4-minute Q&A preparation; link and ZIP contents verified; all-member upload checklist and post-deadline repository freeze recorded | 14; final submission/demo schedule from course announcements |

Stages 11 and 12 each produce saved, inspectable results for their case batch. Use two questions per accepted jurisdiction, four central questions and four negative/ambiguous cases: **24 cases** across the confirmed eight jurisdictions, within the guide's 24–28 design. Include amendment/expiry handling among the applicable cases. Defects discovered during either batch receive separate bounded repair sessions rather than an unlimited fix loop. Keep results tied to the tested version; if a fix affects both batches, rerun affected cases before reporting combined results. Evaluation completion is not a claim of perfect accuracy; publish honest counts, explain remaining limitations, and resolve required-behavior failures before calling the release ready.

Writing source-backed questions happens during source acceptance, before model output can influence the expected answers. Formal evaluation remains later, after full coverage and the UI are verified. A small pilot does not satisfy final corpus coverage.

## Conditional extensions

Two-state comparison routing is deferred, as requested. If selected later, insert two additional sessions after stage 12 and before stage 13: independently filtered comparison retrieval/generation; then UI integration and regression evaluation. The first must demonstrate correctly attributed evidence for both states; the second must preserve abstention when either side lacks evidence and rerun affected baseline cases.

Combined central-plus-state answers are outside the first version under the confirmed one-state-or-Central scope. These questions should request separate queries. Current-benefit verification is explicitly included in the repeated S sessions. OCR is not included; a need for OCR or a source packet too large for a single ingestion session requires an explicit scope/batch adjustment.

## Pending source-verification decision

1. The exact cutoff date for verification of current benefits. Proposed for discussion: 22 September 2026. A different date may be selected; no date is agreed yet.
The user has approved starting stage-wise work. The central scheme selection is explicitly deferred to its S session.

Resolve later at the relevant checkpoint: page-preserving loader choice using stage 2 extraction evidence; explicit rebuild versus incremental index updates before stage 5; notebook-only launch versus a small app.py before stage 9. Extra OCR or materially different scope must be discussed before expanding a stage.

## Checkpoint for every session

Save a short progress note with the stage/batch, completed work, files touched, exact checks and observed outcomes, any unresolved issue, next action, and updated AI-assistance record. Keep agreed decisions in this plan and actual completion in the progress note. Begin the next session from those files instead of re-auditing the whole reference repository.

Suggested continuation message: "Continue stage [number/batch] from the saved checkpoint. Keep the helper-only scope, verify its done criteria, and stop before starting another stage."

## Git history and attribution

Repository: [mohit6603/Electric-vehicle-Policy-RAG](https://github.com/mohit6603/Electric-vehicle-Policy-RAG). The user authorizes committing and pushing completed project work on their behalf. The workspace is connected through `origin`; the initial publication contains planning documents only.

- Use the user's Git identity for both author and committer. Repository-local configuration is `Mohit Patle` with `142034520+mohit6603@users.noreply.github.com`, based on the authenticated GitHub account `mohit6603` (ID `142034520`). Verify attribution on the pushed commit.
- Do not add LLM/bot authors, AI `Co-authored-by` trailers, or generated-by signatures to commit messages.
- Make focused commits at verified checkpoints, with short messages describing the actual change, such as `docs: record staged implementation plan` or `feat: preserve policy page metadata during ingestion`. Split unrelated changes; avoid empty or filler commits.
- Inspect the diff and relevant checks before each commit. Include the checkpoint update and preserve accurate validation results. Exclude secrets, temporary reference checkouts, caches and unintended generated files.
- Start from the user's new project repository. Reuse applicable course code with source attribution in project documentation; do not merge the reference repository's Git history into the new project.
- Verify author/committer metadata and the pushed commit after publication. GitHub associates commits with accounts using the commit email, so the email must belong to the user's account. Other existing or future human/bot commits can affect the contributor display; inspect the supplied repository before promising its final list.
- Keep the assignment's truthful AI-usage disclosure and course-code attribution. Git commit identity does not replace either disclosure.
- Preserve a clean forward history and the submitted revision after the deadline. Rewriting published history or altering an existing author's attribution is outside this standing authorization.

## Submission obligations outside coding sessions

The idea submission is a separate all-member upload of the existing PDF, due 22 September 2026 EOD according to the supplied instructions. Its upload status was not verified and must not wait for the implementation stages. Final submission and demo dates are TBD in those instructions; confirm subsequent announcements. Each of the four approved members must submit individually. Preserve the submitted GitHub revision after the deadline. These human actions cannot be marked complete from a code or document check alone.
