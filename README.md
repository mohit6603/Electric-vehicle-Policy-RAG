# Electric Vehicle Policy RAG

An EV policy assistant planned for the Generative AI mini-project at Jio Institute. It will answer questions from official policy documents, with jurisdiction filtering and document/page citations.

**Status:** Stage 1 is complete. Maharashtra source preparation now includes four official PDFs and eight OCR proposals with page-level review records. Manual team review is deferred until the prototype is built, before formal evaluation/submission; current-benefit verification remains open. [Stage 2 extraction testing](STAGE_2_HANDOFF.md) now loads ten English policy pages and demonstrates loading one OCR proposal with source/amendment metadata. Full OCR integration and splitting remain pending. See [progress](PROGRESS.md) and the [source review](data/policies/maharashtra/SOURCE_REVIEW.md).

## Project documents

- [Staged plan](STAGED_PLAN.md): 30–45-minute work sessions, acceptance checks and current decisions.
- [Implementation guide](IMPLEMENTATION_GUIDE.md): technical workflow and validation guidance.
- [Requirements and reuse map](REQUIREMENTS_AND_REUSE.md): assignment requirements and exact classroom-code references.

## Agreed scope

Coverage: Maharashtra, Tamil Nadu, Uttar Pradesh, Delhi (NCT), Gujarat, Telangana, Karnataka and Madhya Pradesh, plus a central scheme to be selected during source review. Answers will address one jurisdiction per query. Comparisons are deferred.

The agreed verification cutoff is **23 September 2026**, and Maharashtra is the first pilot. This is the target date for source verification, not a claim that current benefits have already been verified. The corpus will include applicable official documents and amendments.

Planned stack: Python 3.12, LangChain, local Ollama embeddings (`nomic-embed-text`), persisted Chroma, Groq (`openai/gpt-oss-120b`) and Gradio.

## Run the setup checks

1. Install [uv](https://docs.astral.sh/uv/) and [Ollama](https://ollama.com/) if they are not already available.
2. From the project folder, run `uv sync --locked`. This creates `.venv` with Python 3.12 and the pinned classroom libraries.
3. Start Ollama if needed (`ollama serve`) and make sure `nomic-embed-text` is available (`ollama pull nomic-embed-text`).
4. Create a local `.env` using `.env.example` and set `GROQ_API_KEY` there. The key file is ignored by Git; do not put the key in the notebook.
5. Run `uv run --locked jupyter lab "EV Policy Assistant.ipynb"`, select the project Python kernel, and run the cells in order.

The notebook checks imports, one local embedding and one small Groq request. An absent key stops the Groq cell; it does not count as a successful check. Clear notebook outputs before committing. `uv pip check --python .venv/bin/python` checks package compatibility.

PDF loader imports are available, but extraction and any extra OCR dependencies will be checked during ingestion. No policy index or Gradio application is created in Stage 1.

## Reference and assistance

Implementation will adapt applicable examples from the [course repository](https://github.com/aagarwal4/generative-ai-pgp-ji-2026/tree/33c2faa22450cde16ead9071f7ce7ecc78ca592a). The reuse map records the relevant notebooks and cells.

AI assistance so far has covered requirements review, repository inspection, planning, Git setup, dependency configuration, adaptation of the classroom setup cells, official-source research, provenance records and OCR preparation, full-page comparisons and proposed text corrections. A bounded Stage 2 page-loading worked example has also been added and executed. Actual setup outcomes and unresolved source gaps are recorded. The team still needs to verify the policy evidence and implement the EV pipeline; no policy evaluation results have been generated. Assistance remains within the agreed helper-only scope, and its actual use will be disclosed in the presentation appendix.
