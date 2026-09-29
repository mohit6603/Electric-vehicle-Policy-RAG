# Karnataka table proposals

Nine pages of the searchable English Clean Mobility Policy use labelled AI table readings: **13, 15 and 30–36**. No OCR engine was used. The existing `data/ocr` folder and review schema are reused for provenance; the shared loader now accepts an explicit `ocr_pdf_pages` subset alongside ordinary PDF extraction.

Each page retains separate `.raw.txt` pypdf extraction and `.proposed.txt` text. [review.json](review.json) records original/raw/proposed hashes, physical page, derivation and empty reviewer fields. All proposals were compared by AI with rendered originals. They are selected table readings with explicit repeated category/zone labels, not claimed verbatim full-page transcriptions. Earlier ordinary text on pages 13/15 is retained; table headers and row labels are expanded to preserve their associations.

Page 13 distinguishes general and special categories, micro/small enterprises and Zones 1–3. Page 15 separates electricity-tax duration and effluent-treatment subsidy categories. Pages 30–36 retain 240 taluks and district continuations, with every taluk assigned a zone label. Raw extraction lost some column positions; the proposed page 35 puts Kurugodu in Zone 2 as shown in the image.

**Unresolved discrepancy:** printed totals are 199/32/9 by zone; counts from the proposed rows are 198/33/9. Both sum to 240. The printed total and individual readings are preserved; no assignment was changed merely to reconcile totals. Human comparison and any official correction remain pending. The retrieval note exposes this uncertainty.

The UI labels the derivation as “AI-assisted English table reading with explicit category/zone labels; pending team review.” Citation links target the original policy PDF and physical page. Team reviewer/date are null; acceptance flags are false. These proposals must not be described as verified OCR or team-authored evidence.

For inspection, render a page with Poppler, then compare the original columns with both recorded text files. Example, after creating the scratch directory:

```sh
pdftoppm -f 13 -l 13 -r 150 -singlefile -png data/policies/karnataka/karnataka_clean_mobility_policy_2025-02-11.pdf tmp/karnataka/policy-page-13
```

Do not overwrite the original PDF or mark review complete based solely on successful ingestion checks.
