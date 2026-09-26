# Stage 7: supported answers with citations

**Technical Stage 7 is complete:** seven notebook checks, 13 deterministic checks and six live cases passed (four supported answers, two abstentions/withheld answers). A fresh Jupyter kernel passed the Central example. Earlier ingestion, persistence and retrieval checks remained successful.

Groq now generates document-based answers from Stage 6's labelled evidence. Each answer point cites supplied source IDs. Code resolves those IDs to original excerpts and builds official PDF-page links from checked metadata. Only sources actually cited by the answer are displayed.

## Run this stage

From the project folder, start Ollama and open `EV Policy Assistant.ipynb` in the pinned environment. Keep `GROQ_API_KEY` in the ignored `.env` file.

1. Run Stage 5's imports, index functions, inputs and open cells with `rebuild_index = False`. A fresh checkout needs the explicit Stage 5 index build first.
2. Run Stage 6's inputs, load, routing and context cells.
3. Run all Stage 7 cells. The example asks for Central e-2W rates, caps and limits; the following cell checks the result and saves its report.

The notebook function is `answer_question(selection, question)`. Choose Maharashtra, Tamil Nadu or Central. It returns `status`, `answer`, `sources`, `points`, jurisdiction, cutoff, a false current-entitlement permission, model name and usage counts. Each point retains its cited source IDs and exact original excerpts for inspection. Source records include physical PDF page, title, date, official URL, local original path, excerpt offsets/hash and version role.

Ollama embeds the question locally. Answer generation sends the question and retrieved public-policy text to Groq and consumes its API allowance. The existing 231-chunk index is reopened; answer generation does not embed the corpus. No new dependency was added.

## Classroom reuse and implementation

Lab 4 cells 150 and 153–155 supply `init_chat_model`, `ChatPromptTemplate` and `prompt | llm`. Exercise 2's Pydantic schema/parser and cell 20 `generate_cart` supply the structured-output and retrieve → format → invoke patterns. The project adds EV-specific instructions, source labels, provenance checks and rendering. The notebook keeps ordinary functions and dictionaries; no agent or separate backend is involved.

The configured model is `openai/gpt-oss-120b`, hosted by Groq, with temperature 0, medium reasoning effort, a 2,048-token output limit, 60-second request timeout and no automatic retries. JSON-object mode is combined with the classroom Pydantic parser. `include_reasoning=False` requests final answers without hidden reasoning. See [Groq reasoning parameters](https://console.groq.com/docs/reasoning) and [structured outputs](https://console.groq.com/docs/structured-outputs).

The schema permits supported points with citation IDs, or `not_established` with no points. Unknown IDs, missing citations, model-generated URLs/markup, extra fields, empty claims, malformed output and interrupted completions are withheld. Structured abstention returns no policy claims or source list. Rejected retrieval/empty context stops before Groq. Basic key/API errors have messages. A conservative guard also withholds Tamil Nadu e-cycle drafts that mention FAME/registration: repeated trials conflated the general EV clause and separate e-cycle clause. This known applicability question is left for source review. The guard can withhold a cautious or otherwise useful draft too; it is not a semantic verifier. Stage 8 wraps this chain with guarded startup and more specific failure messages.

Generation uses `answer_retrieval_k = 1`: the best matching chunk plus Stage 6's adjacency and all mandatory amendment/condition links. This fits the observed pilot allowance while retaining required evidence; recall for broader questions still needs formal evaluation. Context formatting removes extra spaces/blank lines while preserving table line breaks, without removing evidence words, required pages or amendments. Original excerpts remain unchanged for audit. Per-page version notes are retained in returned source records; the prompt uses dates/roles and the overall version note without repeating every per-page note. Source IDs are local to one answer, while stable excerpt IDs retain page identity and offsets. The model never supplies the URL, PDF page number or supporting excerpt text.

Citation validation establishes provenance, not semantic entailment. A model can cite a real page while misreading it; the technical pilot therefore checks selected facts and cited pages separately. These checks do not prove correctness for arbitrary questions.

## Verification

Run `uv run --locked python checks/stage7_answer_checks.py` for 13 deterministic citation checks, including 13 invalid response variants and preservation of all assembled prompt evidence. This opens the local index and needs Ollama, but makes **zero Groq calls**; model responses are fixtures. Add `--live` to run six actual pilot calls, paced 55 seconds apart to reduce rate-limit pressure. The live checker makes at most one retry after 55 seconds for a 429 response and records the earlier failed attempt. Other errors are not retried. Groq account limits can still cause a failed run; results are saved as observed, without substituting fixture answers.

Use `--check-saved` instead of `--live` to recheck a complete recorded batch without Groq calls; it rejects changed notebook/corpus/rules or case definitions.

Reports are saved under `data/processed/answers/`: `stage7_checks.json` for the notebook example, `stage7_citation_checks.json` for deterministic checks and `stage7_live_checks.json` for the live batch. Reports include the notebook, corpus, retrieval-rule and applicable check-script hashes. Numerical/source-page patterns are smoke checks, not an accuracy score or a replacement for inspecting claim meaning.

Pilot questions cover Maharashtra's two-wheeler cap and vehicle-count distinction, Tamil Nadu's tax-only extension, Central rates/limits and L5 closure versus claim/terminal dates, an irrelevant recipe question, and the withheld Tamil Nadu e-cycle eligibility case. The e-cycle case is an observed limitation with a conservative withholding check, not a successfully answered eligibility example. The cases are AI-authored development checks, separate from the team's 24 formal evaluation cases.

During development, a Maharashtra request exceeded Groq's token allowance and initial model-written quote strings contained ellipses/changed wording. Those drafts were withheld. The retrieval seed count was reduced to one, retaining all mandatory linked evidence; whitespace was compacted and the output schema was simplified to source IDs; code now attaches exact original evidence. This avoids relying on model-generated quotation text. A later pilot exposed a missing citation for a historical expiry and overgeneralized motor-vehicle conditions; the prompt now requires the dated source alongside the table. Prompt changes did not reliably fix the e-cycle condition conflation; the guard withholds those drafts and manual review remains pending. Review of an actual answer also caught a vehicle-count/rupee-cap swap that simple number-presence checks missed. Table line breaks are now preserved, the model uses medium reasoning, and the pilot checks bind the cap and vehicle count to their labels. These fixes require observed checks and are not a general correctness guarantee.

## Acceptance boundary

The EV prompt is an **AI-assisted draft pending team review**, not a team-authored prompt. AI assistance also covered implementation, technical cases, live checks, documentation and Git publication. The user's Stage 7 request authorizes this development work; it does not amend the assignment's AI-use rule or disclosure requirement.

Source acceptance, OCR review and current-entitlement verification remain deferred. The visible source cutoff is **23 September 2026**, with review pending. Answers describe the supplied documents and cannot establish present availability, remaining funds or personal eligibility. The six remaining jurisdictions, formal evaluation, UI, deck and submission are later work.

See [Stage 8](STAGE_8_HANDOFF.md) for the guarded entry point and failure checks. The Stage 7 reports above remain tied to their recorded notebook version.
