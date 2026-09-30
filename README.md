# EV Policy Assistant

Ask about an EV policy and get an answer with the original document and page number. The app searches government PDFs for one selected jurisdiction at a time.

Coverage includes Maharashtra, Tamil Nadu, Uttar Pradesh, Delhi, Gujarat, Telangana, Karnataka, Madhya Pradesh and Central PM E-DRIVE buyer incentives. The dataset contains **34 PDFs and 804 text chunks**.


## Tech stack

Python 3.12, LangChain, Chroma, Ollama (`nomic-embed-text`), Groq (`openai/gpt-oss-120b`) and Gradio.


## Setup

Install [uv](https://docs.astral.sh/uv/) and [Ollama](https://ollama.com/). Keep Ollama running, then run:


```sh
git clone https://github.com/mohit6603/Electric-vehicle-Policy-RAG.git
cd Electric-vehicle-Policy-RAG
uv sync
ollama pull nomic-embed-text
cp .env.example .env
```

Add your Groq API key to `.env`:

```dotenv
GROQ_API_KEY=your_key_here
```

Build the index once and start the app:

```sh
uv run python run.py --build-index
uv run python run.py
```

Open **http://127.0.0.1:7860**. For later runs, use only `uv run python run.py`. Rebuild the index after changing source data or the embedding model. Keep `.env` private. Questions and retrieved excerpts are sent to Groq; embeddings run locally.


## Project files

* [EV Policy Assistant.ipynb](EV%20Policy%20Assistant.ipynb): main implementation.
* [run.py](run.py): app launcher and index builder.
* [data](data): original PDFs, source records, OCR text and processed chunks.
* [checks](checks): development checks and saved results.
* [evaluation](evaluation): case template used by [evaluate.py](evaluate.py).


## Stage progress

1. Environment setup: complete.
2. Maharashtra ingestion: complete.
3. Tamil Nadu ingestion: complete.
4. Central scheme ingestion: complete.
5. Persistent semantic search: complete.
6. Jurisdiction filtering: complete.
7. Answers with page citations: complete.
8. Abstention and error handling: complete.
9. Gradio interface: complete.
10. Remaining jurisdictions: complete.


## Source review

The app describes the supplied documents. Current benefit availability and personal eligibility are unverified. All sources still need team review, including OCR readings and amendments. Comparisons and combined state/Central answers are outside this version.

Source dates, URLs, hashes and review status are in [source_manifest.json](data/source_manifest.json). The verification target is 23 September 2026; it is not a claim that benefits were verified through that date. Detailed earlier source notes remain in [Git history](https://github.com/mohit6603/Electric-vehicle-Policy-RAG/tree/f73e596a068c247eb74239e5b6d51388b0712471).


## Validation

The technical audit passed **196 automated checks and 117 ingestion assertions**. These are development results, not an accuracy score. The [24-case evaluation template](evaluation/team_cases.json) is still empty; formal evaluation awaits source review and independently checked expected answers.
