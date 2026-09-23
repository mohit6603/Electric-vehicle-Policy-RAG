# Maharashtra circular OCR drafts

Prepared on 23 September 2026. **Preparation complete; team verification pending.** These are draft transcriptions of five physical pages, not accepted RAG context. The original PDFs were not modified. Dates, names and some words are misread; do not copy these drafts into the index yet.

| Original PDF | Page-matched drafts |
|---|---|
| [19 June circular](../../policies/maharashtra/maharashtra_ev_operational_guidelines_2025-06-19.pdf) | [Page 1](2025-06-19/page-1.txt), [page 2](2025-06-19/page-2.txt), [page 3](2025-06-19/page-3.txt), [page 4](2025-06-19/page-4.txt) |
| [28 July circular](../../policies/maharashtra/maharashtra_ev_operational_guidelines_2025-07-28.pdf) | [Page 1](2025-07-28/page-1.txt) |

[review.json](review.json) records source and draft hashes, OCR settings, known issues and empty reviewer fields for each page. The source manifest still rejects these documents for ingestion. The August corrigendum is outside this five-page preparation batch and still needs its own text review.

Current review: [June page 1 proposed corrections](2025-06-19/page-1-review.md) are ready for team comparison. A `.proposed.txt` file contains AI-assisted suggestions; `.checked.txt` is reserved for the team's actual checked result. Neither filename alone establishes verification.

## Team review

Open each draft beside the corresponding original PDF page. Check the full Marathi text, including dates, clause numbers, negations, conditions and sentences that continue onto the next page. AI spot checks identify examples of errors; they are not an exhaustive verification.

| Page | Checks to prioritize |
|---|---|
| June 1 | Date stamp, handwritten circular/dispatch numbers, policy reference, rules year, ex-factory-price definition |
| June 2 | Eligibility date, responsible parties, invoice wording, two deadline triggers, limits, and first-come qualification |
| June 3 | Continuation from page 2, clause order, payment recipient, exceptions, GST requirement, notification references and policy precedence |
| June 4 | Authority/precedence paragraphs and signatory block |
| July 1 | Date stamp, references, historic registration interval, proof requirements, conditional revised invoices and portal-related deadline |

The invoice's `Subsidy Rs...` is a placeholder, not a benefit amount. An OCR correction must reproduce the source, not rewrite or interpret its policy. If a scan is unclear, record the uncertainty rather than guessing.

Keep the draft `.txt` files unchanged as the OCR record. Save team corrections as `page-N.checked.txt` in the same document folder. For each fully reviewed page, record the checked file's repository-relative path in `corrected_text`, the reviewer's name, review date and `team_verified: true` in `review.json`. Git will preserve the corrections for inspection. A reviewer must actually compare the whole page before marking it verified.

Page verification does not by itself accept the document for ingestion: the source-stage review must also resolve applicable amendments and current-status limits. Citation targets remain the original PDF and physical page. No evaluation questions or expected answers were generated in this session.

## Reproducing the drafts

This run used Tesseract 5.5.3, 300-DPI grayscale PNGs, Marathi plus English, and the LSTM engine. [Tesseract's official CLI documentation](https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html) describes these options. Marathi model provenance and both model hashes are saved in `review.json`; the existing local English model was copied from `/opt/homebrew/share/tessdata/eng.traineddata`. Model files, renders and TSV diagnostics are kept under ignored `tmp/maharashtra/ocr/`.

Example commands from the repository root, after restoring the recorded models into the local tessdata directory:

```sh
pdftoppm -r 300 -gray -png data/policies/maharashtra/maharashtra_ev_operational_guidelines_2025-06-19.pdf tmp/maharashtra/ocr/render/june
tesseract tmp/maharashtra/ocr/render/june-1.png tmp/maharashtra/ocr/raw/june-1 --tessdata-dir tmp/maharashtra/ocr/tessdata -l mar+eng --oem 1 --psm 3 -c tessedit_create_txt=1 -c tessedit_create_tsv=1
```

Repeat for the other physical pages and the July PDF. Use `--psm 6` on June page 3: the first run with automatic segmentation detached clause numbers, while the second kept them beside their paragraphs. All other pages use `--psm 3`. Only trailing whitespace and extra blank lines at file boundaries were removed from the selected output; content errors were retained and flagged. Matching model hashes/settings helps reproduce this run; regenerated outputs still need review.

This is a source-preparation step using local tools. No OCR package was added to the project's Python dependencies, and no OCR, ingestion or answering code was added to the notebook.
