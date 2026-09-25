# Electric Vehicle Policy RAG

An EV policy assistant planned for the Generative AI mini-project at Jio Institute. It will answer questions from official policy documents, with jurisdiction filtering and document/page citations.

**Status:** Technical Stage 4 is complete. Maharashtra has 53 draft chunks, Tamil Nadu 78 and Central PM E-DRIVE 100. The central pilot covers two-/three-wheeler buyer incentives with dated amendments. Manual source acceptance and remaining current-entitlement checks are deferred. See [Stage 4 run instructions](STAGE_4_HANDOFF.md) and [progress](PROGRESS.md).

## Project documents

- [Staged plan](STAGED_PLAN.md): 30–45-minute work sessions, acceptance checks and current decisions.
- [Implementation guide](IMPLEMENTATION_GUIDE.md): technical workflow and validation guidance.
- [Requirements and reuse map](REQUIREMENTS_AND_REUSE.md): assignment requirements and exact classroom-code references.

## Agreed scope

Coverage: Maharashtra, Tamil Nadu, Uttar Pradesh, Delhi (NCT), Gujarat, Telangana, Karnataka and Madhya Pradesh, plus the selected central PM E-DRIVE buyer-incentive pilot (two-/three-wheelers). Answers will address one jurisdiction per query. Comparisons are deferred.

The agreed verification cutoff is **23 September 2026**, and Maharashtra is the first pilot. This is the target date for source verification, not a claim that current benefits have already been verified. The corpus will include applicable official documents and amendments.

Planned stack: Python 3.12, LangChain, local Ollama embeddings (`nomic-embed-text`), persisted Chroma, Groq (`openai/gpt-oss-120b`) and Gradio.

## Run the setup checks

1. Install [uv](https://docs.astral.sh/uv/) and [Ollama](https://ollama.com/) if they are not already available.
2. From the project folder, run `uv sync --locked`. This creates `.venv` with Python 3.12 and the pinned classroom libraries.
3. Start Ollama if needed (`ollama serve`) and make sure `nomic-embed-text` is available (`ollama pull nomic-embed-text`).
4. Create a local `.env` using `.env.example` and set `GROQ_API_KEY` there. The key file is ignored by Git; do not put the key in the notebook.
5. Run `uv run --locked jupyter lab "EV Policy Assistant.ipynb"`, select the project Python kernel, and run the cells in order.

The notebook checks imports, one local embedding and one small Groq request. An absent key stops the Groq cell; it does not count as a successful check. Clear notebook outputs before committing. `uv pip check --python .venv/bin/python` checks package compatibility.

## Run Stage 2 only

Open `EV Policy Assistant.ipynb` from the project folder, run **Shared page loader**, then every cell under **Stage 2: Maharashtra ingestion and chunk checks**, in order. These cells need only the installed Python dependencies; they do not use the API key, Groq or Ollama. The prepared OCR text is already saved in the repository.

Expected output: **18 page records, 16 draft pages, 53 chunks, 12 passed checks**. The notebook writes `pages.jsonl`, `chunks.jsonl` and `stage2_checks.json` under `data/processed/maharashtra/`. Rerunning replaces these derived files. The chunks are unverified development data; no index or answer generation is implemented yet. The [handoff](STAGE_2_HANDOFF.md) explains the amendment exclusions and remaining review work.

## Run Stage 3 only

Run **Shared page loader**, then every cell under **Stage 3: Tamil Nadu ingestion**, in order. No Stage 1/2 execution, API key or model service is needed; the committed Maharashtra artifacts are used for the jurisdiction-isolation check. Expected output: **23 pages, 78 chunks, 12 passed checks**. Outputs are saved under `data/processed/tamil_nadu/`. See [the Stage 3 handoff](STAGE_3_HANDOFF.md) for source scope and deferred acceptance.

## Run Stage 4 only

Run **Shared page loader**, then every cell under **Stage 4: Central PM E-DRIVE buyer incentives**. No API key, Groq, Ollama or earlier-stage execution is needed. Expected output: **53 audit pages, 35 draft pages, 100 chunks and 13 passed checks**. Outputs are saved under `data/processed/central/`. The [handoff](STAGE_4_HANDOFF.md) records scope, required update links and deferred acceptance.

## Reference and assistance

Implementation will adapt applicable examples from the [course repository](https://github.com/aagarwal4/generative-ai-pgp-ji-2026/tree/33c2faa22450cde16ead9071f7ce7ecc78ca592a). The reuse map records the relevant notebooks and cells.

AI assistance so far has covered requirements review, repository inspection, planning, Git setup, dependency configuration, adaptation of the classroom setup cells, official-source research, provenance records, OCR preparation and proposed text corrections. The user subsequently authorized AI implementation of technical Stages 2–4: the shared page loader, source-specific extraction, metadata relationships, splitting, checks and exports. This supersedes the earlier helper-only instruction for those stages; it does not change the assignment's AI-use rule. The team must disclose the actual assistance in the presentation appendix. Manual source verification and independently authored evaluation cases remain the team's work; no policy-answer evaluation results have been generated.
