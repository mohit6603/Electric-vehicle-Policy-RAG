# Stage 8: abstention and failure behavior

**Technical status: complete — 26 September 2026.** Passed 50 offline failure checks, six live cases and six fresh-kernel notebook checks. Stage 6's 19 retrieval checks and Stage 7's 13 citation checks also passed. Manual acceptance and formal evaluation remain pending.

Stage 8 adds `ask_policy(selection, question)` as the guarded notebook entry point. It reuses the existing source loader, saved index, jurisdiction rules and cited-answer chain. `start_policy_assistant()` checks prerequisites without generating an answer, and `reset_policy_assistant()` clears cached readiness after repairs.

## Run this stage

Open `EV Policy Assistant.ipynb` in the pinned Python environment from the project folder. For the guarded path, run these **definition cells**, in order:

1. `stage5-imports`, `stage5-index-functions`.
2. `stage6-inputs`, `stage6-routing`, `stage6-context`.
3. `stage7-schema`, `stage7-prompt`, `stage7-citations`, `stage7-answer`.
4. All Stage 8 cells.

Skip `stage5-inputs`, `stage5-open`, `stage6-load` and earlier examples when checking missing services: they are the earlier direct execution path. Stage 6's loader is now a reusable `load_retrieval_inputs()` function; its new `stage6-load` cell executes it for normal Stage 6/7 runs. Source validation rules and the corpus are unchanged.

The Stage 8 example checks blank/unsupported/conflicting/current-entitlement questions, then makes one actual Central answer call and saves its notebook checks. Ollama, the saved Stage 5 index and `GROQ_API_KEY` in the ignored `.env` are required for that supported answer. Missing prerequisites return messages; the check cell fails rather than claiming completion.

## Behavior and recovery

Every reply has the same fields: `status`, `answer`, `sources`, `points`, `jurisdiction`, `verification_cutoff`, `current_entitlement_answers_allowed`, `model`, `usage`, `reason`, `retryable` and `diagnostics`. A cold failure before source loading can have a null cutoff. All current-entitlement permissions remain false. Errors, clarifications and abstentions contain no policy points or source list from an earlier answer.

| Situation | Result and next action |
|---|---|
| Empty/non-text/punctuation-only input, over 2,000 characters or a recognized vague follow-up | Clarification before embeddings/Groq; enter a specific vehicle/benefit question |
| Missing/unsupported jurisdiction, mismatch, multiple jurisdictions or unsupported Central segment | Existing Stage 6 routing response; align the selection/question or split the request |
| Explicit present-availability, remaining-funds or personal-eligibility request | `not_established`; ask what dated documents state. Current entitlement is unverified |
| Empty search, excessive required context or invalid citations/completion | No partial policy answer; narrow/retry or inspect the evidence as the message indicates |
| Irrelevant/insufficient retrieved evidence | The evidence-only prompt must abstain; no unvalidated similarity threshold is used |
| Missing or changed source/check/rule files | `data_error`; restore files or rerun affected ingestion, then reset |
| Missing, corrupt, inaccessible, changed or stale index | `index_error`; check the folder or explicitly rebuild Stage 5, then retry |
| Ollama unavailable, missing model, query timeout or model error | A distinct embedding status; start/check Ollama or install `nomic-embed-text`, then retry |
| Missing Groq key or invalid configuration | `configuration_error`; check local `.env` and model configuration |
| Groq 401/403, 429, 413, timeout, connection/server error or other rejection | Distinct authentication/rate/size/timeout/service/error status with the corresponding action |
| Unexpected exception | `internal_error`; reset/retry and inspect the separate diagnostic |

Input rejection precedes model work. Groq key presence is checked before opening the index for an answer. Startup never rebuilds or embeds the corpus. Warm requests check index files, receipt identity and all stored text/metadata; existing retrieval checks validate source hashes and the embedding-model identity. Failed setup cannot fall back to a previously opened store. Recoverable requests work after the prerequisite is fixed; changed source packets should be reset and explicitly rebuilt when needed.

Local query embeddings have a 30-second timeout; the Groq timeout remains 60 seconds with automatic retries disabled. `retryable` indicates a transient failure, not an automatic retry or guaranteed recovery. Rate limits depend on the account. Oversized requests are reported without silently dropping mandatory evidence.

Diagnostics contain only phase, exception type and optional HTTP status/cause type. They are separate from the answer and never contain raw exception messages, credentials, response bodies or prompts. `last_diagnostic` is replaced on each request. No user-query logging is added.

## Checks and limits

Run `uv run --locked python checks/stage8_failure_checks.py` for 50 offline checks. These use the real source files, isolated index fixtures and injected SDK exceptions/model replies. They make **zero Ollama and zero Groq calls** and verify unchanged corpus files, no automatic rebuild, redacted errors, consistent replies and recovery without stale answers.

Add `--live` for a real refused local endpoint/recovery check and six actual Groq questions: the four supported Stage 7 topics plus an insurance premium absent from the policy and an irrelevant recipe request containing EV-policy words. The runner pauses 55 seconds before each call, allows one additional wait/retry for a rate limit, records observations and fails if a case does not meet its checks. It never stops the user's Ollama service. Only numeric provider limit fields are retained if a live call fails.

Reports are under `data/processed/answers/`: `stage8_failure_checks.json`, `stage8_live_checks.json` and `stage8_checks.json`. Each identifies the notebook/corpus/rules used; script-based reports also identify the script. Previous stage reports remain observations of their recorded versions, not newly claimed results for the current prompt.

The live batch retained four supported answers and abstained on both unsupported questions. Its last recipe case initially hit Groq's account allowance twice; only that failed case was retried on 26 September after allowance recovered, and both earlier replies remain in the report. A real refused local endpoint returned `embedding_unavailable`; resetting to the normal endpoint reopened all 231 records. The fresh-kernel run then produced the checked Central answer. A final notebook edit only corrected Stage 7's stale boundary description; the live report records both hashes and the check that every executable cell remained identical.

The prompt was shortened during Stage 8 after live size-limit errors; the actual policy excerpts, mandatory links, table line breaks and citation validation were retained. Provider limits can still return an actionable error. Source-ID validation establishes provenance, not semantic entailment or universal answer accuracy.

The new input checks are bounded English patterns, not a general intent/date/location classifier. They can conservatively reject a question containing a present-time word and do not interpret every paraphrase. Other unsupported facts still depend on model abstention. The existing Tamil Nadu e-cycle registration/FAME guard remains conservative and pending source review. No new jurisdiction, source acceptance or current-entitlement verification is claimed.

## Reuse and next stage

Stage 8 wraps the existing Stage 5 open/check functions, Stage 6 loader/router/retriever and Stage 7 `answer_question`; its local `try`/`except` branches extend Exercise 2's error-handling pattern. `httpx` and `ollama` exception types are from already installed dependencies; no new package, custom exception hierarchy or backend is added.

AI assistance covered implementation, compacting the prompt, failure-case design, observed local/Groq checks, documentation and Git publication. These are development checks, not the team's independently authored 24-case evaluation. Manual source/OCR/prompt review and the assignment's AI-use/disclosure obligations remain unchanged.

Stage 9 now provides the notebook Gradio pilot; see [its handoff](STAGE_9_HANDOFF.md) for the definition-cell launch sequence and UI checks. The Stage 8 reports above retain their recorded test versions.
