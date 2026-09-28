# Telangana OCR proposal

The body of the one-page 16 November 2024 gazette is an image although the PDF has a searchable header/signature layer. The complete page was rendered at 220 DPI and compared by AI with Tesseract 5.5.3 English output (`--psm 3`). No Python OCR dependency was added.

[Raw OCR](tax-2024-page-1-raw.txt), [proposed English text](tax-2024-page-1.proposed.txt) and [review/hash records](review.json) remain separate. The proposal starts at the English gazette title; it omits the masthead's price, registration identifiers and garbled Telugu title. It corrects the department suffix, superscript date, `1IOO` to `100`, `usec` to `used` and `ie.` punctuation, without changing the operative terms. It retains the complete exemption paragraph, bus qualifications, date, unrestricted vehicle count, signature and printer line.

Citation links target the original gazette and physical page 1. The UI labels this as AI-assisted English OCR transcription. This is an AI proposal, not a checked transcription or legal interpretation. All human reviewer fields are empty and acceptance flags false. Team comparison with the full page remains pending.

Reproduce locally with Poppler and Tesseract (output directory must exist):

```sh
pdftoppm -f 1 -l 1 -r 220 -singlefile -png data/policies/telangana/telangana_tax_fee_2024-11-16.pdf tmp/telangana/tax-page
tesseract tmp/telangana/tax-page.png tmp/telangana/tax-page -l eng --psm 3
```

Generated output may differ across tool/model versions. Do not replace the recorded raw/proposed files or mark review complete without comparing changes to the original.
