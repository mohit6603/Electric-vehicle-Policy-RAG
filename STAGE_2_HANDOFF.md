# Stage 2: first-state extraction and splitting

**Technical Stage 2 is complete.** Maharashtra's four source PDFs produce 18 page records and 53 draft chunks from 16 pages. Twelve checks pass in a fresh Jupyter kernel. The user authorized AI implementation of this stage with disclosure; manual source review and two team-written evaluation examples remain deferred. Current-benefit verification is still open.

## Run this stage

1. From the project folder, install the locked environment with `uv sync --locked` if needed.
2. Open `EV Policy Assistant.ipynb` using `uv run --locked jupyter lab "EV Policy Assistant.ipynb"` and select the project Python kernel.
3. Run **Shared page loader**, then every cell under **Stage 2: Maharashtra ingestion and chunk checks**, in order. Stage 1 cells, API keys, Groq and Ollama are not needed for this stage.
4. Confirm **18 loaded pages, 16 draft pages, 53 draft chunks and 12 passed checks**. Clear notebook outputs before committing.

The export cell writes three files under `data/processed/maharashtra/`:

| File | Contents |
|---|---|
| [pages.jsonl](data/processed/maharashtra/pages.jsonl) | All 18 page texts with original PDF citations, physical page numbers, provenance, relationships and review/status fields |
| [chunks.jsonl](data/processed/maharashtra/chunks.jsonl) | 53 draft chunks with inherited metadata, start offsets and stable chunk IDs |
| [stage2_checks.json](data/processed/maharashtra/stage2_checks.json) | Observed counts, passed checks, critical evidence chunk IDs and artifact/notebook hashes at export |

Rerunning replaces these derived files. It leaves the original PDFs, OCR proposals and source-review records unchanged. Save notebook edits before running; the report hashes the notebook file on disk at export. If source checks fail, fix the mismatch before rerunning the stage; do not treat an older report as a result for changed inputs.

## Reuse confirmed before implementation

The [reuse map](REQUIREMENTS_AND_REUSE.md) pins the course reference to commit `33c2faa22450cde16ead9071f7ce7ecc78ca592a`. Cell numbers include markdown cells.

| Work | Course code | Implemented adaptation |
|---|---|---|
| Load and inspect PDF text | Lab 4, cells 65–66, `UnstructuredPDFLoader` / `loader.load()` | `pypdf.PdfReader` preserves physical pages for the English policy; explicitly mapped OCR proposals supply the circulars and corrigendum. The page reader, sidecars and hash checks are additions. |
| Attach metadata | Exercise 2 solution, cell 9, `Document(page_content=page_text, metadata=metadata)` | Source identity, state, year, PDF/page citation, dates, review/status fields and document relationships are attached before splitting. |
| Split | Lab 4 cell 77; Lab 5 cell 25, `RecursiveCharacterTextSplitter` / `split_documents(docs)` | Policy documents are split at 1000 characters with 200 overlap and start indices. Critical table blocks pass with the default boundaries. |

The implementation stays in small notebook cells with lists, dictionaries and short functions. No new dependency or application framework was added.

## Source and amendment handling

- The [manifest](data/source_manifest.json) supplies original PDF paths, dates, official URLs, page counts and hashes. Physical pages 16–25 of the base policy retain those numbers.
- The [OCR review records](data/ocr/maharashtra/review.json) explicitly select eight proposed text files. The loader checks complete page coverage, source/proposal hashes and roles; it does not glob all text files or combine raw and proposed OCR.
- June supplements the base policy; July clarifies June. The August corrigendum amends section 4.2(1). Its page 1 old wording and page 3 distribution list remain in the page audit but are excluded from draft chunks; page 2 supplies the replacement.
- Base policy page 19 retains unaffected provisions and a link to the replacement page. Related page IDs preserve table conditions and continuations. The IDs are JSON strings to keep metadata scalar for the later vector store; retrieval must resolve them in Stage 6.
- All OCR text stays labelled `ai_proposal`, with `team_verified: false` and `accepted_for_ingestion: false`. Current availability remains `not_verified`; current-entitlement answers are not allowed. Citations target original PDFs, with OCR text paths recorded separately.

## What the checks establish

The notebook checks unique source/page coverage, nonempty text, hashes, valid relationship targets, original PDF citations, metadata retention and complete non-whitespace text coverage after splitting. It checks that Table 2 retains all ten rows with headings/units and its linked conditions, Table 3 retains its rows/units/cost exclusion, June clause 6 keeps its page 2–3 continuation, and the August replacement remains separate from audit-only wording.

Independent review also exercised 14 invalid-input cases and reproduced both JSONL outputs byte-for-byte. These are extraction/chunking results, not policy-answer evaluation results or proof that benefits are currently available. The [text review](data/ocr/maharashtra/TEXT_REVIEW.md) retains source inconsistencies and OCR uncertainties.

## Deferred acceptance and next stage

The team still needs to verify the source text/document chain, record actual reviewers and dates, and independently write the two Maharashtra evaluation cases. Those tasks belong to the consolidated team-review batch before formal evaluation/submission. Current-benefit verification through **23 September 2026** remains unresolved separately.

The loader currently selects AI-proposed OCR. Accepting checked text later requires selecting and hashing the genuinely reviewed files, updating the loader/checks and rebuilding derived outputs. Changing review flags alone does not promote proposal text.

Stage 2 ends here. The selected second jurisdiction, Tamil Nadu, is now implemented in [Stage 3](STAGE_3_HANDOFF.md). The next development stage is central-source ingestion. No embeddings, Chroma index, policy-answer generation or UI is part of this checkpoint.
