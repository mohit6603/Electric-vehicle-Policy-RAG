# Stage 2: first-state extraction and splitting

Current work: Maharashtra only, targeting 30–45-minute sessions. The notebook loads ten English policy pages and demonstrates one OCR page separately. The team next generalizes OCR loading to all eight records and combines the 18 unique pages before splitting. Stage S's preparation batch is finished; source acceptance and current-benefit verification remain open. The user has deferred manual review until the full prototype is built. Candidate data may be used for development with unverified status retained; manual review is a final acceptance requirement, not a Stage 2 development blocker.

AI assistance remains helper-only: the team implements the notebook cells and writes its own two evaluation examples; assistance can explain, review and debug that work. No Stage 2 application cells or expected answers were written during source preparation.

## Reuse confirmed before implementation

The [existing reuse map](REQUIREMENTS_AND_REUSE.md) pins the course reference to commit `33c2faa22450cde16ead9071f7ce7ecc78ca592a`. Cell numbers include markdown cells.

| Work | Course code | Adaptation to inspect |
|---|---|---|
| Load PDF text | `class-labs/4. Retrieval Augmented Generation (RAG).ipynb`, cells 65–66, `UnstructuredPDFLoader` / `loader.load()` | Preserve physical page numbers. The English policy is text-readable; the circulars/corrigendum require the prepared page sidecars. A simpler page-preserving loader is a justified gap to fill, not something the course already implements. |
| Attach metadata | `class-exercises/exercise-2/exercise2_solution.ipynb`, cell 9, `Document(page_content=page_text, metadata=metadata)` | Replace grocery metadata with source identity, Maharashtra, policy year, physical page, URL, date, review/status fields and amendment relationships. |
| Split | Lab 4 cell 77; Lab 5 cell 25, `RecursiveCharacterTextSplitter` / `split_documents(docs)` | Start with 1000 characters and 200 overlap. Feed policy documents, not Lab 4's unrelated webpage `docs`. Inspect table rows and continuations before choosing final settings. |

Use the same small top-level notebook cells, lists/dictionaries and short comments as these examples. An application framework or new OCR dependency is unnecessary for this stage.

## Inputs

- [Source manifest](data/source_manifest.json): four original PDFs, dates, URLs, page counts and hashes. `ready_for_extraction_tests` is distinct from `accepted_for_ingestion`; the latter is still false.
- Base policy: physical pages 16–25, ten page records. Retain physical numbering after selecting the English section; never renumber these pages 1–10 for citations.
- [OCR review records](data/ocr/maharashtra/review.json): five circular pages and three corrigendum pages. Use the proposed sidecars explicitly for tests, with `team_verified: false`. Do not read every `.txt` in the directory: that would duplicate raw/proposed text and later checked text.
- [Text review](data/ocr/maharashtra/TEXT_REVIEW.md): page roles, table caveats and continuations. Corrigendum page 1 is old wording; page 2 replaces it; page 3 is distribution only. Retain all pages in the audit; exclude the distribution-only page from answer chunks.
- [Research log](data/policies/maharashtra/research_log.json): cutoff 23 September 2026, current availability unknown. Research notes and portal counts are audit evidence, not policy answer context.

## Work in order

1. Load the ten English pages and eight sidecar pages into inspectable page records. Check counts, nonempty content and source/page mappings before splitting. Keep raw extraction separate from any cleanup.
2. Add metadata before constructing the splitter. Inspect a policy record, a circular record and the replacement-clause record. Keep citations pointed at original PDFs, not text files. Do not lose `team_verified`, current-status restrictions or document relationships when splitting.
3. Split, then inspect the complete incentive table and its conditions, June's clause spanning pages 2–3, and the old/replacement toll clause. Preserve a heading and units with each table row; keep cross-page relationships in metadata rather than assigning a fabricated single source page to combined text.
4. Record the technical results and carry the source-review and two-question tasks into the consolidated team-review batch after prototype development. Do not mark them complete or generate expected answers using the assistant.

## Done checks and stopping point

Technical tests pass when all 18 candidate page records map correctly, the distribution-only page is distinguished, inspected chunks preserve table values/conditions and the required provenance, and old toll wording cannot be mistaken for its replacement. Record actual chunk counts only after running the team's implementation. Test that an unknown current-status flag stays unknown after splitting.

Stage 2 technical completion permits moving to the next development stage. Final acceptance still needs the team's checked source text and two human-verified examples, now deferred to the consolidated review batch before formal evaluation/submission. Current-benefit verification remains unresolved separately; candidate tests cannot satisfy it. No embeddings, Chroma index, answer generation or UI belongs in this session. Save the observed checks and one focused Git commit, then stop at the Stage 2 boundary.
