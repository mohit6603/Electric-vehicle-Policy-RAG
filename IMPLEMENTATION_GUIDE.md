# EV Policy Assistant: team implementation guide

Use this alongside `REQUIREMENTS_AND_REUSE.md` and `STAGED_PLAN.md`. The steps below describe work for the team to implement and understand, with bounded AI help for explanation, review and debugging. They are not completed code or claimed test results. The proposal originally specified 8–10 states and 20–30 questions; the user has selected eight jurisdictions, including Delhi, and the resulting evaluation design contains 24 cases. The 3-slide deck, submission rules and grading weights come from the assignment. Session boundaries and pending decisions are recorded in `STAGED_PLAN.md`.

Checkpoint update, 25 September 2026: the user subsequently authorized AI implementation of technical Stage 2. Technical Stage 3 for Tamil Nadu and Stage 4 for the PM E-DRIVE buyer-incentive pilot are also complete after the user requested implementation. Stages 5–6 are also complete at the user's request, with persistent semantic search, checked reopening, jurisdiction filtering and source-version context. The shared page loader, source-specific table extraction, amendment links, splitting, exports, pilot index and filtered retrieval are complete; [PROGRESS.md](PROGRESS.md) records the observed checks. Manual source acceptance and team-written evaluation examples remain deferred. This guide describes the full project scope, including work still to be built.

## Keep the project close to the class examples

Begin with one notebook that follows the class order: setup, load data, split documents, create embeddings, index, retrieve, generate, UI, evaluation. A name such as `EV Policy Assistant.ipynb` fits the repository's notebook naming. Keep a small `app.py` only if it helps launch the finished Gradio demo. Separate index-building from the code the app runs on each startup.

Suggested supporting files are `data/policies/` for PDFs, a small source manifest, an evaluation file, `README.md`, `.env.example`, and the environment manifest. These are recommendations, not additional assignment deliverables. Retain source links and the reviewed course commit beside adapted sections. Do not copy unrelated datasets, model selectors, Pydantic grocery schemas, galleries or teaching-only code just to increase apparent reuse.

Use short functions when a task is repeated. Follow `gradio_interface` and `generate_cart` as organizational examples, adapting the latter to an EV-specific name such as `answer_question`. Use descriptive state/policy names where needed. Preserve normal attribution; concise comments should explain an actual choice or boundary.

## 1. Establish the corpus and its limits

Collect official government documents for Maharashtra, Tamil Nadu, Uttar Pradesh, Delhi (NCT), Gujarat, Telangana, Karnataka and Madhya Pradesh, plus the central scheme selected during source review. The user accepts these seven states and one union territory as the eight jurisdictions. Start by validating one state's source packet to learn the ingestion path, then complete the full agreed coverage. An early small corpus is a development milestone, not the final dataset.

Maintain these fields for each source:

| Field | Purpose |
|---|---|
| Local filename and document title | Trace an answer to the original document |
| State or `Central` | Consistent retrieval filter and UI choice |
| Policy year | Required proposal metadata; not proof of current validity |
| Official source URL and retrieval date | Provenance and freshness boundary |
| Effective/expiry dates, if the document states them | Explain time-limited benefits without guessing |
| Extraction checked; problematic pages | Avoid indexing missing, corrupted or wrongly ordered text |

Read representative incentive tables and eligibility/validity sections in the PDF and compare them to the extracted text. Check currency, percentages, per-kWh units, caps, vehicle categories, dates and footnotes. An extraction returning some characters is not sufficient evidence that a numerical table is usable.

If a PDF is scanned or unreadable, document the limitation and seek a usable official version. Do not replace an agreed jurisdiction without discussing the scope change. OCR is extra work, not an explicit assignment requirement. One bounded preparation session was approved for the Maharashtra operational circulars; its [drafts](data/ocr/maharashtra/README.md) need team verification before source acceptance. Do not invent or silently repair policy amounts.

A dated policy supports questions about that document but does not by itself establish current benefits. The user has chosen current-benefit verification through **23 September 2026**, starting with **Maharashtra**: check official amendments, extensions, replacement documents and status through that cutoff. Keep each applicable document chain traceable, record unresolved status, and avoid claiming live policy coverage beyond the cutoff.

## 2. Load documents with trustworthy page metadata

Reuse L4's `UnstructuredPDFLoader` pattern and E2's `Document(..., metadata=...)` pattern. Make sure the splitter receives the policy documents, not the lab's previously loaded website `docs`.

The lab's `by_title` configuration creates section-oriented elements. Inspect whether an element crosses physical pages before treating a single `page_number` as a precise citation. A page-preserving configuration or loader is an explainable adaptation when exact page citations matter.

One alternative, **not demonstrated in the course notebooks**, is `PyPDFLoader` with page-wise extraction. LangChain's [official API reference](https://reference.langchain.com/python/langchain-community/document_loaders/pdf/PyPDFLoader) documents `mode="page"`. If the team chooses it, verify the installed classroom version's behavior, check its page metadata, and be prepared to explain the additional syntax. It is not a substitute for checking table quality or an automatic OCR solution.

Before splitting, attach the canonical state, policy year, document title, official source URL and page information. Use a consistent display convention such as physical PDF page 1, and preserve printed page labels separately if useful. Do not assume different loaders use the same field name or page-number base.

Check: inspect several documents manually, including two different states. Locate their text on the stated source pages. Then inspect split chunks and confirm the metadata survived.

## 3. Build and reopen the Chroma index

Reuse L4 cell 77's recursive splitting and cell 38's embedding setup, then L5 cell 17's persisted Chroma initialization. The class's 1000-character chunks with 200-character overlap are an initial setting, not a verified optimum for policy tables.

Keep the collection name, persist path and embedding model consistent between ingestion and the application. Add all accepted policy chunks rather than the lab's first-ten shortcut. An app launch should open an existing index; indexing should be a deliberate separate step.

Decide what a repeated ingestion does. A simple documented rebuild of this project's own index can be sufficient during development. Alternatively, assign reproducible chunk IDs and deliberately replace affected documents. Either approach must account for stale chunks when documents change. Do not retain fresh-UUID insertion on every application launch.

Check: record indexed document/chunk counts, restart the app, and confirm no corpus re-embedding occurs. Repeat the team's chosen ingestion process and inspect for duplicates or stale documents. This is still local persistence; the app needs Ollama for new query embeddings and Groq for generated answers.

## 4. Make jurisdiction selection explicit

Adapt L4 cell 127's metadata filter from `source` to the canonical state field. Start with a state dropdown whose choices come from the accepted corpus. Include a `Central` choice so the promised central scheme is reachable.

Decide and document these cases before building the UI:

| Input situation | Suggested baseline behavior |
|---|---|
| A state is selected; the question names no state | Use the selected state |
| The question names the selected state | Retrieve only that state's chunks |
| Selected state differs from a state explicitly named in the question | Ask the user to align the selection and question |
| No supported state is selected, or the question names an unsupported state | Request a supported choice; do not fall back to an unfiltered search |
| Central scheme is selected | Retrieve central documents only |
| Two states are compared | Explain the single-state scope unless the optional comparison route is implemented |

These are proposed product decisions, not existing repo functionality. Simple explicit state-name checks may be enough for the baseline; document supported aliases and limitations. Do not describe a dropdown alone as automatic state detection.

For a combined central-plus-state question, ask for separate queries. The user chose one state or Central per query for the first version. Do not assume the benefits can be added together.

Check: inspect retrieved metadata before calling the LLM. A Maharashtra query must not return Karnataka evidence. A UI mismatch must not silently override the filter. If experimenting with hybrid retrieval later, every retrieval branch needs the same jurisdiction restriction.

## 5. Generate answers with evidence the user can check

Reuse E2 cell 20's sequence: retrieve, format context, build the input dictionary, invoke a prompt/LLM chain, return the result. Reuse L4 cell 150's Groq initialization. For the baseline, one model is enough.

Final acceptance requires the team to review and own the EV prompt. Stage 7 currently supplies a disclosed AI-assisted draft at the user's request; this does not satisfy a claim of team authorship. It should constrain answers to the supplied evidence, retain eligibility/vehicle/date conditions, identify the jurisdiction, and state when the available material does not answer the question. L4's hub prompt illustrates abstention, but does not implement this project's citations or policy rules.

Unlike E2's text-only join, format the relevant document metadata with each evidence passage. Keep citations traceable to the retrieved documents, and check that a claimed source actually supports the answer. A list of retrieved documents alone is not proof of grounding.

Handle an empty result before asking the model to answer. Also test cases where documents are returned but are irrelevant: top-k retrieval can return something for an unsupported question. A similarity threshold is a tuning option, not a guarantee of answerability; the class's threshold should not be copied as a validated EV value.

Aim for a short answer with sources attached. Preserve necessary conditions even when they make the answer longer than one sentence. Saying "not established by these documents" is different from asserting that no benefit exists.

Check: compare an amount, its unit, its cap and its eligibility conditions against the source PDF. Ask an unsupported question and inspect whether the model abstains. Verify actual cited pages rather than trusting the model's citation text.

Stage 7 implements this flow in notebook cells `stage7-schema` through `stage7-checks`. The model emits supplied source IDs; code attaches exact excerpts and physical PDF-page links. See [Stage 7 handoff](STAGE_7_HANDOFF.md) for run instructions, observed checks and provenance-versus-semantic-support limits.

## 6. Add the Gradio interface and basic failure handling

Adapt E2 cells 23–24's `gr.Interface` first; its Blocks alternative in cells 26–28 is available if useful. Keep the callback small: state and question in, answer and sources out. Use the same return shape for normal answers, clarifications and errors.

Handle the failures students can demonstrate and explain: empty question, unavailable index, unavailable Ollama model/service, missing Groq key and failed model request. Keep developer diagnostics separate from the answer. A missing index should produce an actionable message instead of triggering an unnoticed full rebuild.

Use `.env` for the Groq key and an example file with placeholders. Check what Git will include before publishing. Source PDFs and metadata must be available or reproducibly obtainable by a reviewer, with setup/run instructions that match the actual implementation. Do not claim offline answer generation: the proposed Groq model is remote.

Stage 8 now supplies `ask_policy`, `start_policy_assistant` and `reset_policy_assistant` in the notebook. The source loader has a separate definition/execution step so setup failures can return a checked result. See [Stage 8 handoff](STAGE_8_HANDOFF.md) for statuses, recovery and the distinction between injected failures and actual live observations. Stage 9 now adapts Exercise 2’s `gr.Interface` in the notebook, with a small `gradio_interface` callback, loaded jurisdiction choices and two Markdown outputs. See [Stage 9 handoff](STAGE_9_HANDOFF.md) for launch and observed UI checks.

## 7. Write and run the promised evaluation

Have the team write two questions per included jurisdiction, four central questions, and four unsupported or ambiguous questions. For the confirmed eight jurisdictions this produces **24 questions**, within the promised 20–30, including 20 questions answerable from the verified documents. Include numeric incentives, eligibility, validity dates, amendment handling and at least one table-based case across the set.

Use these evaluation fields; leave observed results empty until a run has occurred:

| Before running: students fill from the PDF | After running: students record observations |
|---|---|
| Question ID and text | Retrieved document/page references |
| Selected jurisdiction and test type | Generated answer and displayed citations |
| Expected answer or expected abstention/clarification | Retrieval correct? |
| Supporting document, page and short evidence passage for answerable cases | Answer accurate and conditions preserved? |
| Relevant vehicle category and date | Citations support the answer? |
| Human verification of the expected answer | Pass/fail, failure explanation and run date |

For unsupported questions, explain what the corpus does not establish; do not fabricate a supporting page. For ambiguous inputs, the expected behavior may be clarification rather than a policy answer.

Keep retrieval and answer correctness separate. If the right passage was not retrieved, changing only the generation prompt may not solve the problem. If retrieval succeeded but a number was misread, inspect table extraction and the answer instructions. If a citation has the wrong page, inspect metadata and page numbering.

Report observed counts with denominators. No minimum score is stated by the assignment. Keep an honest record of failures and limitations; a tuned prompt is not evidence of a successful evaluation by itself.

## 8. Treat comparisons as an optional extension

Only after the baseline and its evaluation work, consider L6's `State`, `retrieve`, `generate` and graph edges, plus L8's conditional-edge example. The proposed two-state router is not already implemented in either notebook.

Keep each state's evidence and answer separate, then show them side by side. If one side lacks evidence, say so. Test the optional path separately and explain its extra syntax in the demo. An assistant handling one jurisdiction per query across the full promised corpus satisfies the non-agentic project scope.

## 9. Prepare the required submission and demo

The supplied idea PDF contains the required idea categories. The user confirmed approval for its four-person roster. Every member still needs their own Digiicampus upload by **22 September 2026, EOD**; this task has not verified any uploads.

For the final submission, use exactly these three slides:

| Slide | Required subject | Evidence to use from the team's work |
|---|---|---|
| 1 | Business impact | Buyer problem, intended users and benefit; distinguish expected impact from measured results |
| 2 | Technical stack and GenAI architecture flow | Actual implemented ingestion/retrieval/generation flow and selected class libraries |
| 3 | Appendix, including AI-use disclosure | Actual AI assistance, source/reuse attribution, observed evaluation and material limitations as space permits |

Slide 3 must contain AI disclosure; the other suggested appendix material is not explicitly mandated. Keep a truthful assistance log now. AI assistance has included reading the PDFs, inspecting the reference code, mapping requirements, preparing guidance, configuring dependencies, adapting the classroom setup cells, running the environment checks, researching official Maharashtra sources, and preparing OCR drafts with provenance and visual spot checks. At the user's later request, AI also implemented technical Stages 2–9, including ingestion, persistence, retrieval rules, a draft EV prompt, structured answer generation, citation resolution, guarded failure behavior and the Gradio pilot, and ran actual development checks. Formal team evaluation has not run. Update that record as work continues; do not claim work was manually authored or tested when it was not.

Recommended 8-minute rehearsal: 1 minute for the buyer problem, 2 for the architecture, 4 for the live demo, and 1 for observed evaluation/limitations and appendix. Prepare for a separate 3–4 minutes of questions. This timing split is advice; only the 8-minute total and approximate Q&A duration are specified.

In the live demo, show a supported numerical answer, open its source page, demonstrate state filtering, show an unsupported question, and exercise the central option. Be able to explain why chunking, metadata filtering, persistence and abstention are needed, and which classroom code was adapted. Prepare the app beforehand without presenting unrun examples as results.

Before submitting: verify the GitHub URL works for the intended reviewer, setup instructions match a clean run, the deck has exactly three slides in the required order, and the ZIP contains the deck and repository link. All four members must upload individually. Final submission and live-demo dates remain TBD in the PDF; use the course's later announcements. Preserve the submitted GitHub revision and do not edit after the deadline.

## First ingestion checkpoint

After the staged plan's environment checks and first source-verification session, implement the first state's load → metadata → recursive split path. Inspect the extracted incentive table and the page metadata before adding embeddings; include applicable amendment documents in its source packet. That produces a small, concrete piece of student code that can be reviewed against L4 cells 65–77 and E2 cell 9 before the team extends it to the full corpus.
