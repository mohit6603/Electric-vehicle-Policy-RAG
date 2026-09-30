# Audit evidence

See [the requirement audit](../../PROFESSOR_AUDIT.md) for interpretation and outstanding work. These are development observations; no human acceptance or formal accuracy result is implied.

- `repository_check.json`: anonymous export of published `4b85eed`, compared with the 285 tracked files.
- `regressions_before.json`: 184 existing checks on that fresh export.
- `regressions_after.json`: the same checks plus 12 review-transition checks with the audited code overlaid into its fresh environment. The review suite also executes ingestion assertions; those are not counted again in the 196-suite total.
- `ingestion.json`: all 18 real corpus JSONLs reproduced unchanged; notebook hash at export.
- `static_checks.json`: source hashes, notebook syntax/schema, pending-source/case counts, Git attribution and bounded credential checks.
- `browser_before.json`: original two observations, including the real Central rate error. Retained as a failure.
- `browser_after.json`: six actual submissions against the patched export, with responses, excerpts, latency and embedding instrumentation.
- `findings.json`: observed semantic interpretation, browser checks, expected evaluation refusal and tested file hashes.
- `central_repaired.png`: actual browser screenshot of the corrected generic query.

The original setup was `uv sync --locked` in a fresh export, then `python run.py --build-index` and `python run.py --check` using that environment and the existing local Ollama service. The local key was passed through the environment for live tests, never copied into the export or saved in these reports. This is same-machine reproduction.

To rerun the automated suites from a configured project, use the locked environment and run each script under `checks/` ending in `_checks.py`, without `--live`. These are the Stage 5–9, six Stage 10, evaluation and review-transition scripts. Ollama and local HTTP sockets are needed for integration checks. For real ingestion, run the notebook's shared loader and the Stage 2–4/10 ingestion cells; this refreshes derived outputs and receipts. Rebuild the index explicitly if corpus artifacts change.

Live model results can vary; repeat the recorded questions only as development probes. The team still needs to author and independently grade its own frozen evaluation cases. Reports from 29 September are the preserved baseline; repaired results are dated 30 September.
