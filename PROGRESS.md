# Project checkpoint

## Stage S: Maharashtra source review

Date: 23 September 2026. Status: **incomplete; research checkpoint saved**. The user agreed Maharashtra as the first pilot and 23 September 2026 as the verification cutoff. Stage 2 ingestion has not started.

Saved four official PDFs (33 physical pages total), a [source manifest](data/source_manifest.json), [review notes](data/policies/maharashtra/SOURCE_REVIEW.md), and [public status evidence](data/policies/maharashtra/status_evidence.json). The packet includes the 23 May policy, 19 June and 28 July operational circulars, and 29 August corrigendum. Document dates were distinguished from website upload dates.

Observed checks:

- All four files open with `pypdf`; page counts and SHA-256 hashes are recorded. Main-policy pages 18–19, all five circular pages, and corrigendum pages 1–2 were rendered and visually inspected.
- The English incentive table is readable before splitting. June's text layer garbles Marathi; July returns no text; the corrigendum also needs Marathi character checks. No source is yet marked accepted for ingestion.
- The official transport listing links to the MHEV portal. Saved public responses have dated registration totals and vehicle-type counts, but do not establish current funding, approved/paid claims or individual entitlement. The announcements request returned HTTP 401; no authentication was attempted.
- The known documents' relationships are recorded. Completeness of the amendment chain and current availability through the cutoff remain unresolved. No current-entitlement claim is approved from this packet.

Next action: resolve the pending choice of an added OCR preparation session with team verification, or team-provided checked transcriptions. Continue the bounded official status/amendment check as a separate source-stage continuation. Once source acceptance checks pass, begin the team's Stage 2 ingestion work using the existing reuse map. Do not interpret the saved checkpoint as source-stage completion.

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
