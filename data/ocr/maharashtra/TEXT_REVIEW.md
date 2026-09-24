# Maharashtra text review

AI-assisted comparison completed on 24 September 2026. **These are proposed transcriptions, not team-verified text.** Original PDFs and the five earlier raw circular OCR files are unchanged. All page numbers below are physical PDF pages, starting at 1.

The batch contains five circular pages and three corrigendum pages. Raw OCR is `page-N.txt`; corrections are in `page-N.proposed.txt`. [review.json](review.json) maps both to the original PDF and records their hashes. `.checked.txt` remains reserved for an actual team review. Compare the complete proposal against its scan before accepting it; the correction notes below are not a substitute for that check.

## Circular corrections

| Document/page | Proposed corrections and comparison result |
|---|---|
| June 1 | Previously prepared [change log](2025-06-19/page-1-review.md): date, handwritten identifiers, reference and eligibility wording. The printed rules year appears to be `१९५९`; it was retained, not silently changed to a presumed legal reference. Contact-line `l`/`1` glyphs remain uncertain. |
| June 2 | Corrected the invoice placeholder's policy year to `२०२५`, `करारांवर` to `करांवर`, and restored `व` before GST in clause 6. Compared the 23 May registration date, OEM responsibility, conditional GST requirement, both 30-day deadline triggers and first-come allocation. This page also appears to print `१९५९`; legal-reference accuracy is unresolved. Clause 6 continues onto page 3. |
| June 3 | Corrected OCR errors in verification/review wording, plural incentive references, `किंबा` to `किंवा` and `प्रंकरणी` to `प्रकरणी`. Kept the continuation of clause 6 before clauses 7–12. Compared OEM payment, public-transport exceptions, Maharashtra GST condition and policy precedence. The printed notification dates read `२७/०७/२०२१` and `०२/०८/२०२१`; this transcription does not independently verify the referenced notifications. |
| June 4 | Restored the signatory `(विवेक भीमनवार) भा.प्र.से.` and `परिवहन आयुक्त`; removed stray OCR marks. Retained authority, policy-precedence paragraphs and the distribution list. |
| July 1 | Corrected dispatch `9068`, stamp `28 JUL 2025`, circular `53/2025`, policy reference date and contact-line OCR. Restored the signatory after a further full-page visual comparison. Compared the 23 May–19 June interval, proof of passing incentives to customers, revised invoices only if needed, and the 30-day window after portal launch. The actual launch date is not established. Contact glyphs should still be checked if used. |

The June and July proposals omit the source-computer path/page-number footer; the PDF page remains in metadata. Body wording and unusual printed spellings were retained rather than rewritten. None of these documents supplies a confirmed current claim balance.

## August corrigendum

Rendered all three pages at 300 DPI, then ran the recorded Marathi/English Tesseract models with PSM 3. Compared the OCR and proposed text with the page images.

| Page | Corrections and role |
|---|---|
| 1 | Corrected the header's OCR `2024` to printed `२०२५`, garbled `इलेक्ट्रिक`, `छत्नमार्गाचे` to `छत्रमार्गाचे`, and `न्हावा रेवा` to `न्हावा शेवा`. This page quotes the **old** section 4.2(1) wording. Retain it as amendment history, not the replacement rule. |
| 2 | Preserved `याऐवजी` and the full replacement paragraph. Corrected the corridor word, percentage script, `हिंदूहृदय`, website punctuation and first distribution-list number. Removed OCR fragments of the digital-certificate block, keeping the visible signatory name/title; the original PDF retains the complete signature. The government reference reads `२०२५०८२९१२५२२७७२२९`. |
| 3 | Distribution list only, entries 13–31. Corrected `(ऊज)` to `(ऊर्जा)` and removed a stray `र्ड` before `/ नागपूर`. This page adds no benefit clause and need not become an answer chunk. |

The replacement concerns reimbursement by Transport to the concerned department/authority, in place of naming PWD alone. The passenger-EV 100% toll wording for the named roads remains. Do not interpret this as a change to purchase-incentive amounts or as proof of current toll-system implementation. Cite the original corrigendum page 2 for the replacement; keep page 1 available to explain the change.

## Main policy: English extraction check

Compared physical pages 16–25 with their `pypdf` extraction. The English body, tables and numeric fields are readable; Marathi header/reference glyphs are imperfect. Use original page metadata for identity, not garbled header text. This is an English-section extraction check, not a certification that both language versions are identical.

- Page 16: policy period 1 April 2025–31 March 2030. Keep it separate from the June circular's registration eligibility date.
- Pages 17–18: distinguish adoption targets (Table 1) from incentive percentages, vehicle-count limits and rupee caps (Table 2). The target table prints buses M2/M3, while Table 2 prints M3/M4; preserve and flag the source inconsistency. Do not silently normalize the category.
- Pages 18–19: retain Table 2 rows with their headings and associate them with the page-19 conditions. The earlier table comparison remains valid before splitting; chunk integrity must be tested in Stage 2.
- Pages 19–20: charging provisions continue into Table 3. It distinguishes minimum charging-point counts, kW ranges, percentages, per-station rupee caps and station limits. Keep the exclusion of land/ancillary costs attached. The printed range `250 to > 500 kW` must not be silently rewritten.
- Pages 21–22: section 4.4(4) continues across the page boundary. Page 22's printed heading says “Demand Side Intervention” even though its following text discusses manufacturing; retain the source heading.
- Pages 22–23: R&D list continues onto page 23. Pages 23–24 continue section 4.8, including OEM pass-through and the portal mechanism. Pages 24–25 continue implementation responsibilities.
- Pages 24–25: committee and department tables extract in reading order. Table 4's PWD designation cell is blank in the PDF; do not fill it by inference. The original English toll paragraph does not reproduce every Marathi reimbursement detail; the corrigendum must accompany it.

## Acceptance

The technical comparison batch is finished. No human reviewer or review date has been supplied, so every `team_verified` flag stays false. The team can review all eight proposals as one packet and record its real reviewer/date and corrected file paths together. No separate chat approval is needed for each page. Source availability and amendment-completeness limits are recorded in [SOURCE_REVIEW.md](../../policies/maharashtra/SOURCE_REVIEW.md); readable text alone does not resolve them.
