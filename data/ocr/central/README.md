# Central OCR proposals

Five proposed page texts support Stage 4. Original PDFs and raw Tesseract output are retained. [review.json](review.json) records original-PDF, raw-text and proposed-text SHA-256 hashes and physical-page mappings. Every reviewer/date field is empty and all acceptance flags are false.

| Source | Pages | Why a sidecar is needed |
|---|---|---|
| 10 August 2026 amendment | 3 | The embedded text layer omits rupee amounts and parts of several sentences. Rendered at 220 DPI; raw English OCR also misreads currency signs and ordinals. |
| 23 December 2025 L5 closure letter | 1–2 | Scanned pages; rendered at 150 DPI and read with English OCR. |
| 29 October 2025 exceptional claim-window letter | 1–2 | Scanned pages; rendered at 150 DPI and read with English OCR. Kept for historical audit only. |

Engine: local Tesseract 5.5.3, `eng`, `--psm 3`. No new Python dependency was installed. The full rendered pages were inspected during AI comparison; this is not human verification.

The August proposal transcribes the English notification and linearizes its single table with explicit column labels. It restores the printed rupee signs, 11,900 crore outlay, 45,79,120 target, year-specific incentive amounts/caps, 1.5 lakh price ceiling, 2,767 crore category allocation, 15% limitation, fund-limited closure, L5 closure and separate final claim/payment dates. It omits the Hindi running header and digital-signature graphic; it retains the typed publishing footer. No amount was inferred from another source.

The letter proposals correct visible OCR errors in SIAM, date ordinals, the government heading and a few words, while retaining source wording. Non-text signature scribbles are omitted; typed names/contact information are retained. The October letter's date-bound exception is not treated as a current open claim window. Its referenced enclosure is not present in the downloaded two-page PDF; no missing attachment was invented.

Before acceptance, the team must compare the complete proposed pages to the PDFs, resolve any remaining transcription errors, save actually checked text and record real reviewer/date information. The loader deliberately uses proposals with `text_status=ai_proposal`; changing a review flag alone cannot promote these files to verified text.
