# Stage 10 — Gujarat handoff

Gujarat's **technical batch is complete**, with a specific battery-limit abstention pending source review. Telangana is next, then Karnataka and Madhya Pradesh. Team acceptance, current-entitlement verification and formal evaluation remain pending. The agreed source cutoff stays 23 September 2026.

## Sources and implementation

The [source review](data/policies/gujarat/SOURCE_REVIEW.md) covers the official 2021 policy, 17 April 2025 tax notification and 30 March 2026 tax-deadline amendment. All ten selected physical pages were rendered and inspected. The original policy period is historical; the later tax deadline is separate and does not establish renewed cash subsidies. All source acceptance/current-entitlement flags remain false.

Three PDFs yield **10 pages and 31 chunks**. The local index now has **511 chunks**: Maharashtra 53, Tamil Nadu 78, Central 100, Uttar Pradesh 117, Delhi 132 and Gujarat 31. Four new ingestion cells reuse the shared loader, recursive 1000/200 splitter, metadata links and export checks. No dependencies changed. The previous ten corpus JSONL files reproduce byte-for-byte; their ingestion receipts match the expanded manifest.

Gujarat, Gujrat and GJ use the existing jurisdiction routing. Historical purchase context stays within the 2021 policy; any tax source pulls in the complete tax table and both pages of the 2026 update. The policy's operative-period page remains mandatory. Hash-checked exclusions remove unrelated education/land-revenue text and the distribution list from answer context while preserving full audit pages and original citations. All ten possible page seeds fit the 50,000-character budget.

Gradio automatically lists six jurisdictions and has a Gujarat tax example. Startup reopens the saved index without corpus embedding; the explicit full rebuild happened once. The ignored local Chroma files must be rebuilt on a fresh checkout.

## Answer corrections and remaining limit

The initial broad purchase answer passed numeric/link checks but failed AI output review: it treated the maximum subsidised capacity as vehicle eligibility and repeated column (2) without flagging that battery values are in column (3). That original observation is retained with `failed_output_review`. Further attempts exposed tax/subsidy confusion and a wrong period citation. Separating historical and tax context and clarifying page-level citation instructions addressed those paths, but did not reliably resolve battery interpretation.

The final prototype therefore abstains on purchase-subsidy battery-limit requests before model calls; the Stage 7 path also withholds generated claims using the known 2/5/15 kWh limits. The reason is `gujarat_battery_limit_review_pending`, and no sources/points are shown for a withheld answer. This follows the existing Tamil Nadu ambiguity pattern. It is deliberately bounded, not a general claim-checking guarantee. The team still needs to resolve the inconsistent policy reference before enabling these answers.

A narrower historical rate/price/period answer had correct facts and pages but present-tense phrasing. The renderer now prefixes points supported entirely by `historical_only` evidence with **Historical provision:**, for all jurisdictions. The prompt also asks for the page containing each claimed fact/date and distinguishes subsidy limits from vehicle eligibility. No original PDF text was rewritten.

## Run and checks

For ingestion, run `shared-loader` and all four `stage10-gujarat-*` code cells. If the shared manifest changes, rerun all earlier ingestion stages to refresh their receipts. For Gradio, use [Stage 9's definition-cell sequence](STAGE_9_HANDOFF.md), leaving `rebuild_index = False` for this machine's current index.

```sh
uv run --locked python checks/stage10_gujarat_checks.py
uv run --locked python checks/stage10_gujarat_checks.py --live
```

The default uses local Ollama queries but no Groq. Live mode adds `historical_rate` and `tax_extension` questions through Gradio, 60 seconds apart, plus no-model rejection/abstention checks. Use `--live --case historical_rate` or `--live --case tax_extension` for a targeted run. Preserve a failed report before rerunning a command that writes its filename.

Recorded technical checks:

- **12 ingestion checks** cover original hashes, metadata/links, complete non-whitespace coverage, historical period/targets, all three purchase rows, charging limits and the tax chain.
- **11 integration checks** cover restart without corpus embeddings, Gujarat aliases, five filtered semantic queries, historical/tax separation, all page seeds, excluded text, generated-capacity withholding, deterministic historical labels, six no-model rejections and Gradio choices.
- **Six fresh-kernel checks** cover ingestion, ready restart, 511 records, six choices, current-entitlement abstention and local Gradio HTTP startup, with no Groq call.
- Regression suites passed: **16 persistence, 19 retrieval, 13 citation, 50 failure, 15 UI, 10 UP and nine Delhi integration checks**. Stage 5/6 notebook checks passed eight each; the updated Stage 8 example guards also passed without Groq.
- **15 live/integration checks passed** in the final Gradio run: the historical rate/price/period answer cites policy pages 5 and 3, and the auto-rickshaw answer retains 2.5/1.5/1% of vehicle cost, the exclusive-battery qualification, 31 March 2027 and separation from purchase subsidy. Comparison and battery-limit requests clear citations. Final artifact/credential checks are recorded in `data/processed/gujarat/`. The initial failed review and four subsequent failed attempts are kept separately; they are not counted as successful answers or independent evaluation.

These are AI development checks. They do not establish complete amendment coverage, current availability, individual entitlement or general model accuracy. Actual team source acceptance and two independently authored Gujarat evaluation cases remain deferred.

AI assistance covered official-source research/downloads, visual comparison, ingestion/retrieval configuration, answer/abstention fixes, development questions, execution and result review, documentation and authorized Git publication. Disclose this assistance in the assignment appendix. Git attribution uses the user's authorized identity.
