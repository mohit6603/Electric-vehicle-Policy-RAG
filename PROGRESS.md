# Project checkpoint

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

Next action: agree the policy cutoff date and choose the first pilot state from the eight confirmed jurisdictions, then begin its source-verification session (S). Central scheme selection remains part of central-source review. No source verification or Stage 2 ingestion has started.

AI assistance in this stage: environment configuration, setup-cell adaptation, setup checks, documentation and Git operations. The team still owns the policy corpus, EV-specific implementation, prompt and human-verified evaluation questions.
