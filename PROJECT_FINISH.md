# Project finish checkpoint

**Application implementation complete; assignment acceptance/submission pending.** Technical Stages 1–10 cover the eight agreed jurisdictions plus Central, 804 persisted chunks, jurisdiction-aware retrieval, cited Groq answers, abstention/error handling and the Gradio interface. Original sources and course-code attribution are in the repository. Keys and the machine-local index are excluded from Git.

The [30 September professor audit](PROFESSOR_AUDIT.md) now records fresh-environment reproduction, 196 passing automated checks, 117 ingestion assertions and a targeted Central-answer repair. Team acceptance and submission are still pending. The user reports the deadline as **1 October 2026**, with time not supplied; the live-demo date is unknown. A broader professor AI-use exception is user-reported, but its wording/scope has not yet been provided for verification.

## Run

From this project folder, with Ollama running and `GROQ_API_KEY` in the ignored `.env`:

```sh
uv run --locked python run.py
```

Open http://127.0.0.1:7860. Stop with Ctrl+C. `--check` verifies startup without Groq; `--port 7861` changes the local port. Normal startup never builds embeddings. A fresh checkout needs `uv sync --locked`, `ollama pull nomic-embed-text`, local `.env` setup, then `uv run --locked python run.py --build-index` once. The launcher executes the existing notebook definitions; there is no second backend implementation.

## Required remaining work, in order

1. **Team acceptance:** compare candidate/OCR text against original PDFs, resolve applicable instrument/status gaps and review the prompt. Record actual reviewers/dates; update acceptance records only for checks actually completed. Current-benefit availability is still unverified and the app refuses current entitlement claims.
2. **Stages 11–12:** independently fill the 24 expected-answer cases in `evaluation/team_cases.json`, then freeze and run the two batches as described in `evaluation/README.md`. Grade retrieval, answers and citations separately. Development spot checks do not establish formal accuracy.
3. **Stage 13 final acceptance:** after evaluation/repairs, verify the intended submission revision. Anonymous repository access, a new virtual environment, explicit index build and restart were checked in the professor audit on this Mac. A separate clean-machine reproduction is not claimed; rerun affected checks after subsequent changes.
4. **Stage 14:** the team authors exactly three slides: business impact; stack/GenAI architecture; appendix with truthful actual AI assistance. The assignment limits AI to code assistance, so no AI-authored presentation is represented as a compliant final deck.
5. **Stage 15:** rehearse the eight-minute team presentation/live demo and prepare for 3–4 minutes of Q&A. Package the three-slide deck and repository link in the final ZIP, verify the announced deadline, and have every member upload it to Digiicampus. Preserve the submitted GitHub revision after the deadline.

Repository link: https://github.com/mohit6603/Electric-vehicle-Policy-RAG

The four-member group exception is user-confirmed. Technical 80% / presentation 20% is the stated grading split. Git attribution remains Mohit Patle; the appendix still needs to disclose the actual AI assistance recorded in `PROGRESS.md` and `REQUIREMENTS_AND_REUSE.md`. No upload, rehearsal, independent review, evaluation result or instructor approval beyond the user's confirmation has been invented.
