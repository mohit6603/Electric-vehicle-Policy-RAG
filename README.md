# EV Policy Assistant

Ask a question about an EV policy and get an answer with the original document and page number. The app uses government PDFs, searches within the selected jurisdiction and shows the evidence beside the answer.

**The app is built. Team review, formal evaluation and final submission are still pending.** It covers Maharashtra, Tamil Nadu, Uttar Pradesh, Delhi (NCT), Gujarat, Telangana, Karnataka and Madhya Pradesh, plus the Central PM E-DRIVE two-/three-wheeler pilot. Ask about one jurisdiction at a time; comparisons and combined Central-plus-state answers are outside this version.

The dataset has **34 PDFs, 308 selected pages and 804 chunks**. The source-verification target is **23 September 2026**, but current benefits and personal eligibility have not been verified. The app states this limitation and refuses current-entitlement claims.

## Run locally

Install [uv](https://docs.astral.sh/uv/) and [Ollama](https://ollama.com/). Keep Ollama running; if needed, run `ollama serve` in another terminal. For a fresh checkout, use the commands below. If you already have the project, skip the first two lines and work from its folder.

```sh
git clone https://github.com/mohit6603/Electric-vehicle-Policy-RAG.git
cd Electric-vehicle-Policy-RAG
uv sync --locked
ollama pull nomic-embed-text
```

On first setup, copy `.env.example` to `.env` and add your key:

```dotenv
GROQ_API_KEY=your_groq_api_key
```

Keep `.env` private. It is excluded from Git, along with `.venv`, temporary files and the local index. Questions and retrieved policy excerpts are sent to Groq; embeddings run locally.

Build the index once, then start the app:

```sh
uv run --locked python run.py --build-index
uv run --locked python run.py
```

Open **http://127.0.0.1:7860**. For later runs, use only the second command. Normal startup reuses the saved index. Rebuild explicitly after changing the corpus or embedding model. Stop with `Ctrl+C`; use `--port 7861` if port 7860 is busy.

`uv run --locked python run.py --check` checks startup without calling Groq. A missing index needs a build; a missing key needs `.env`; connection errors usually mean Ollama is stopped. Wait before retrying a Groq rate-limit error.

## How it works

**PDFs → page text and metadata → chunks → local embeddings → saved Chroma index → jurisdiction-filtered search → Groq answer → page citations in Gradio.**

The stack is Python 3.12, LangChain, Chroma, Ollama `nomic-embed-text`, Groq `openai/gpt-oss-120b` and Gradio. Dependencies are pinned in [pyproject.toml](pyproject.toml) and [uv.lock](uv.lock).

| File or folder | Purpose |
|---|---|
| [EV Policy Assistant.ipynb](EV%20Policy%20Assistant.ipynb) | Main implementation, organised by stage |
| [run.py](run.py) | Launches the notebook's implementation; also checks or rebuilds the index |
| [data/policies](data/policies) | Original government PDFs |
| [data/source_manifest.json](data/source_manifest.json) | Source URLs, dates, hashes, page selections and review status |
| [data/ocr](data/ocr) | Raw text, AI-assisted readings and page review records |
| [data/processed](data/processed) | Page/chunk JSONL files and stage results |
| [data/retrieval_rules.json](data/retrieval_rules.json) | Amendment links, exclusions and evidence rules |
| [checks](checks) / [evaluation](evaluation) | Development checks / independent team evaluation |

## Stage progress

“Done” below means the technical work passed its checks. It does not mean the source text or benefits have been accepted by the team. Work through pending stages in order, one 30–45-minute session at a time; save the next unfinished step here.

| Stage | Work and result | Status / depends on |
|---|---|---|
| S | Collect original sources, dates, amendments and OCR where needed | Preparation done; team acceptance pending before 11 |
| 1 | Set up Python, dependencies, Ollama and Groq | Done |
| 2 | Ingest Maharashtra and preserve tables, conditions and page metadata | Done; 1 + source preparation |
| 3 | Ingest Tamil Nadu through the shared loader | Done; 2 |
| 4 | Select and ingest Central PM E-DRIVE buyer-incentive documents | Done; 2 |
| 5 | Build, save and reopen semantic search without duplicate chunks | Done; 3–4 |
| 6 | Filter by jurisdiction and include required amendments | Done; 5 |
| 7 | Generate supported answers with document/page citations | Done; 6 |
| 8 | Handle unsupported questions, unclear inputs and service failures | Done; 7 |
| 9 | Add the Gradio picker, question box, answers and sources | Done; 8 |
| 10 | Add UP, Delhi, Gujarat, Telangana, Karnataka and MP individually | All six done; 9 + each source packet |
| 11 | Complete team review, write/freeze 24 cases and run batch 1 | **Next**; 10 + actual team inputs |
| 12 | Run batch 2, grade results and fix observed failures | Pending; 11 |
| 13 | Confirm reproducibility and access at the final revision | Setup audited; final acceptance follows 12 |
| 14 | Prepare exactly three presentation slides | Pending; 13 |
| 15 | Rehearse, make the ZIP and submit from every member's account | Pending; 14 |

For notebook work, open `uv run --locked jupyter lab "EV Policy Assistant.ipynb"`. Run **Shared page loader**, then the chosen Stage 2, 3, 4 or 10 ingestion section in order. These sections do not need Groq or Ollama; saved OCR text is already included. They replace derived page/chunk files and stage receipts. Refresh all ingestion receipts after manifest changes, then rebuild the index if corpus data changed. Use `run.py` for normal launch rather than running every notebook cell.

## Source review

All 34 sources remain unaccepted, and no current-benefit permission has been granted. Original PDFs stay the citation targets; AI-assisted OCR, translations and table readings remain labelled. Readable text and valid citations do not establish correct interpretation or current availability. Sources collected after the target date do not prove availability at that cutoff.

| Jurisdiction | Pages / chunks | Main points still needing review |
|---|---:|---|
| Maharashtra | 18 / 53 | Policy and registration start dates differ. Check Marathi circulars and cross-page conditions. August page 2 replaces toll reimbursement wording, not purchase support; pages 1/3 are history/distribution only. Portal launch, claim windows and remaining funds are unverified. |
| Tamil Nadu | 23 / 78 | The later motor-vehicle-tax extension does not extend purchase incentives, registration charges or permit fees. E-cycle registration/FAME interpretation remains withheld. |
| Central | 53 / 100 | Keep each year/period with its own rate and cap. Scheme end, claim deadline and funding limit differ; retain the L5 closure. Detailed non-buyer segments and operational availability remain outside the checked scope. |
| Uttar Pradesh | 39 / 117 | Hindi-to-English readings are unofficial; old masked 3W text is superseded. Keep purchase provisions separate from pure-EV tax/fee exemptions. Parent amendments, hybrid/aggregator rules and operational status need review. |
| Delhi | 51 / 132 | Use the final 2026 policy and guidelines, not drafts. Check notification/commencement dates, RC-generation versus registration wording, ownership/scrapping conditions, car exceptions and later instruments. |
| Gujarat | 10 / 31 | The purchase policy is historical. Later tax extensions do not renew purchase benefits. Battery-limit questions are withheld because the table's column reference is inconsistent. |
| Telangana | 13 / 32 | Later tax/fee rules replace old quotas; this is not a cash subsidy. Separate retrofit conditions remain. Bus qualifications, manufacturing-policy dependencies and the full later Act need review. |
| Karnataka | 41 / 105 | Act commencement is unverified. Printed zone totals 199/32/9 differ from counted rows 198/33/9; MSME/industrial-policy dependencies remain open. Do not invent a charging-subsidy cost basis. |
| Madhya Pradesh | 60 / 156 | The draft is excluded; original gazette/transport instruments remain missing. Check amendments and charging conditions. RWA provisions distinguish seven working days, seven days and a 30-day grievance threshold. |

Detailed earlier source notes and OCR corrections are preserved in the [documentation before consolidation](https://github.com/mohit6603/Electric-vehicle-Policy-RAG/tree/f73e596a068c247eb74239e5b6d51388b0712471). In particular, Maharashtra's printed rules-year and bus-category inconsistencies must be checked against the originals, not silently corrected. Keep raw OCR files unchanged when preparing reviewed text.

The saved AI-assisted readings cover eight Maharashtra pages, five Central pages, ten UP pages, one Telangana page, nine Karnataka tables and sixteen MP pages. UP readings and MP page 1 include unofficial English translations. Original-page mappings, file hashes and preparation settings stay in each OCR folder's `review.json`; a matching hash does not prove the reading is accurate.

## Checks and evaluation

The 30 September technical audit passed **196 automated checks and 117 ingestion assertions**. All 18 corpus JSONL files reproduced unchanged. A fresh environment on the same Mac installed successfully, rebuilt 804 chunks and reopened them. This was not a second-machine test or a formal accuracy score.

The audit fixed a Central rate-period error and a loader bug that discarded completed review status. Two corrected Central answers matched their cited page; refusal and citation-clearing checks passed. [Saved audit reports](checks/professor_audit) retain the original failure and actual retests. Their hashes describe the audited revision before this documentation cleanup.

To rerun development checks with Ollama available:

```sh
for check in checks/*_checks.py; do
  uv run --locked python "$check" || break
done
```

These checks do not call Groq unless a supported script is given `--live`. They do not replace the team's promised **20–30 self-written questions**. The agreed [24-case template](evaluation/team_cases.json) is still empty: two per jurisdiction, four Central and four negative/ambiguous cases.

Before formal evaluation:

1. Compare source/OCR text and the prompt with the original evidence. Record actual `reviewer`, `reviewed_on` (`YYYY-MM-DD`), `team_verified` and `accepted_for_ingestion` values in the manifest and relevant OCR `review.json` pages. Legacy Maharashtra pages need the acceptance field added when accepted. A source cannot be accepted while its selected OCR pages remain unaccepted.
2. Keep raw text intact. The loader reads `proposed_text` and checks `proposed_sha256`; if using a corrected file, update that path/hash pair too—`corrected_text` alone does not change ingestion. Regenerate affected outputs and explicitly rebuild the index. Text acceptance does not verify current benefits.
3. Write questions, expected answers and physical-page references independently, before looking at model output. Include amendments and expiry conditions. In `evaluation/team_cases.json`, fill the actual `authored_by`, `verified_by` and `verified_on` for each case, plus the top-level `source_review` record (`completed`, `reviewer`, `reviewed_on`). Then freeze the cases and run both batches:

```sh
uv run --locked python evaluate.py --freeze
uv run --locked python evaluate.py --batch 1
uv run --locked python evaluate.py --batch 2
```

The runner records versions and real responses, resumes unfinished batches and spaces requests by 60 seconds. The team grades retrieval, answers and citations separately. Keep failed runs and report honest counts; service errors are not successful abstentions. **No formal evaluation cases have run.**

## Course code and AI assistance

This project adapts the [course repository at commit 33c2faa](https://github.com/aagarwal4/generative-ai-pgp-ji-2026/tree/33c2faa22450cde16ead9071f7ce7ecc78ca592a). Cell numbers count all cells, starting at 1.

| Classroom example | Reused here |
|---|---|
| `class-labs/4. Retrieval Augmented Generation (RAG).ipynb`, cells 65–66, 77 | PDF-loading workflow and recursive splitting: 1,000 characters with 200 overlap; `pypdf` adds physical-page preservation |
| Same notebook, cells 37–38, 127/129, 150, 153–155 | Ollama embeddings, filtered retrieval, Groq setup and prompt-chain pattern |
| `class-labs/5. Advanced RAG with LangChain.ipynb`, cell 17 | Persisted Chroma collection |
| `class-exercises/exercise-2/exercise2_solution.ipynb`, cells 9, 20, 23–24 | Document metadata, retrieve/format/generate flow and Gradio callback/interface |

EV source collection, OCR handling, amendment rules, citation checks, failure handling, explicit rebuilding and evaluation tooling extend those examples. The team needs to understand and explain these additions.

AI assisted with planning, source research, OCR/readings, implementation, debugging, development questions and output checks, documentation and Git work. This includes generated code and must be disclosed accurately in slide 3. The professor's written rule permits code-helper use only and states a **30% flat penalty for detected AI-generated code**. Broader permission is user-reported; its wording has not been supplied for verification. Git authorship does not replace that disclosure or approval.

## Final submission

The project is a custom-dataset RAG application; agents are optional. The four-person group exception is user-confirmed: Mohit Patle (27PGAI0102), Pushkar Brahmankar (27PGAI0100), Vaishnavi B (27PGAI0120) and Sehal Chodankar (27PGAI0116). The agreed coverage is seven states plus Delhi, a change from the proposal's literal 8–10 states. Answers use concise cited points rather than a strict one-line format.

- **Idea PDF:** names/IDs, problem and rationale, approach and stack were checked. Every member's upload, due 22 September 2026 EOD, remains unverified.
- **Exactly three slides:** 1. business impact; 2. technical stack and GenAI architecture flow; 3. appendix including actual AI assistance.
- **Demo:** rehearse an eight-minute presentation/live demo and prepare for about 3–4 minutes of Q&A. Grading is technical **80%**, presentation/narrative **20%**.
- **Final ZIP:** include the three-slide presentation and [project GitHub link](https://github.com/mohit6603/Electric-vehicle-Policy-RAG). Every member must upload it to Digiicampus and retain a receipt.
- **Deadline:** the user reports **1 October 2026**; exact time and demo date remain unconfirmed. Late uploads by any member or GitHub edits after the deadline can penalise the whole group, including a possible zero. Preserve the submitted commit after the deadline.

The deck, formal evaluation, rehearsal, ZIP and upload confirmations are still pending. The professor does not mandate 24 cases, a minimum accuracy, hosting, a video or a separate report; the evaluation target comes from our proposal and plan.
