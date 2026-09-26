# Stage 9: Gradio pilot

**Technical status: complete — 26 September 2026.** The notebook launches a local Gradio interface with a jurisdiction dropdown, question box, Ask/Clear controls, and separate answer/source outputs. Fifteen UI checks, eight browser checks and five fresh-kernel checks passed. Stage 8's 50 failure checks also passed.

## Launch from the notebook

From the project folder, start Ollama and run:

```sh
uv run --locked jupyter lab "EV Policy Assistant.ipynb"
```

Select the project's Python environment. Run these definition cells in order, then Stage 9:

1. Stage 5: `stage5-imports`, `stage5-index-functions`.
2. Stage 6: `stage6-inputs`, `stage6-routing`, `stage6-context`.
3. Stage 7: `stage7-schema`, `stage7-prompt`, `stage7-citations`, `stage7-answer`.
4. Stage 8: `stage8-results`, `stage8-startup`, `stage8-ask`.
5. All Stage 9 cells: callback, startup, interface and launch.

The definition cells contain the existing loader/index functions, routing/context functions and answer functions. Skip earlier execution/example/check cells when launching this UI; they are separate stage demonstrations. Do not use Run All just to open the demo. The saved Stage 5 index must already exist; a fresh checkout needs its explicit build first. Keep `GROQ_API_KEY` in the ignored local `.env`.

The local link is **http://127.0.0.1:7860**. Keep the notebook kernel running. Startup opens and checks the saved index without rebuilding, embedding the corpus or generating an answer. A supported question uses a local query embedding and a Groq call. Startup does not validate Groq credentials; an absent key is reported on submission.

Select Central, Maharashtra or Tamil Nadu, type a question and click **Ask**. Example rows fill both inputs but do not generate an answer until Ask is clicked. Answers retain inline citation links; Sources lists the cited jurisdiction, document and physical PDF page. **Clear** resets both inputs and outputs, so choose a jurisdiction again afterward. This is a single-question interface with no conversation memory.

Stop the server with `demo.close()` in a notebook cell. Before replacing sources/indexes or rerunning backend cells, close it; then rerun Stage 9's startup, interface and launch cells. If port 7860 is in use, close the earlier demo or choose another local port in the launch cell. No public share link is created.

Notebook-only launch was the stated default after the optional launcher question received no answer. A separate `app.py` was not added. This keeps the classroom notebook as the single implementation.

## Reuse and behavior

Exercise 2 cells 23–24 supply the `gradio_interface`, `gr.Interface` and `demo.launch` pattern. The new callback passes selection/question directly to Stage 8's `ask_policy`, separates Stage 7's existing source footer and returns two Markdown strings for every result. It neither regenerates source metadata nor changes retrieval or prompting.

Dropdown choices come from the loaded corpus. The pilot contains only Maharashtra, Tamil Nadu and Central; other jurisdictions remain Stage 10 work. Conflicting jurisdictions clarify; questions outside the Central pilot's scope stop; unsupported facts abstain; missing prerequisites show the existing actionable messages. Failures replace previous citations with “No sources cited.” Diagnostics remain in the notebook's `last_diagnostic`, outside the interface. Current-benefit verification and source acceptance remain pending and are visibly labelled.

The existing Gradio 5.31.0 dependency is reused. The queue allows one request at a time because the notebook shares backend readiness state, with up to eight waiting requests. Responses are not cached, examples do not auto-run, and Gradio flagging/analytics are disabled. Markdown sanitization remains enabled. The app binds to loopback with `share=False`; it is a local demo, not a hosted or multi-user service.

## Observed checks

Run the repeatable UI checks with:

```sh
uv run --locked python checks/stage9_ui_checks.py
```

This starts and closes an isolated local HTTP server. It uses explicit fixtures for the supported answer and rate-limit reply, and actual Stage 8 guards for empty input, mismatch, unsupported named jurisdiction/central segment, current entitlement, missing key and missing index. The 15 checks include output shape, source replacement, dropdown/configuration and argument forwarding. **No Ollama or Groq calls occur in this check mode.** These are not live policy-answer accuracy results.

For observed browser checks, `--serve` starts the real local pilot and records requests under `data/processed/ui/stage9_live_ui.json`. `--serve --missing-key` starts a separate test server on port 7861 with key absence injected; it never edits `.env`. Stop test servers with Ctrl+C. These are verification modes; normal notebook use does not save user questions. Test-server reports begin as observations and need actual output/browser checks before being labelled passed.

The recorded browser run used **two actual Groq calls**: a supported Central e-2W answer and an irrelevant recipe question that abstained. It checked the displayed rate, cap, price ceiling and percentage limit against the existing technical case, along with physical-PDF-page links. Other browser checks covered mismatch clearing old citations, unsupported Central scope, blank input, Clear, example selection, and the injected missing-key error. Startup reopened all 231 records with zero corpus/query embeddings and zero Groq calls; only the two generated requests embedded a query.

A fresh Jupyter kernel loaded only the documented definitions and Stage 9, reopened the saved index, checked the choices and negative callbacks, and launched/closed Gradio on port 7862 without calling Groq. All six corpus JSONLs, retrieval rules and existing notebook cells remain unchanged. The canonical notebook has no saved outputs.

Reports under `data/processed/ui/`:

- `stage9_ui_checks.json`: 15 configuration/HTTP checks, clearly labelled fixtures.
- `stage9_browser_checks.json`: eight observed browser checks and DOM snapshots.
- `stage9_live_ui.json`: actual answers/statuses, citation checks and embedding counts.
- `stage9_missing_key_ui.json`: separately injected missing-key browser case.
- `stage9_notebook_checks.json`: five fresh-kernel checks.

During development, the test counter initially blocked query embeddings because Ollama's query method delegates to its document method. The instrumentation was corrected to permit that one-query path while forbidding corpus embedding. Gradio's Markdown labels did not provide visible headings, so the callback now renders Answer/Sources headings directly. Neither repair changed the policy backend.

## Remaining work

These are AI-assisted implementation and development checks, not the team's independently authored formal evaluation. Manual source/OCR/prompt review, current-entitlement evidence gaps and known model/alias limitations remain as recorded in Stage 8. No claim of universal relevance detection or answer accuracy is made.

**Next: Stage 10 — add one remaining jurisdiction per session.** It has not started. The next jurisdiction in the agreed list is Uttar Pradesh, followed by Delhi, Gujarat, Telangana, Karnataka and Madhya Pradesh; each needs its own source packet, ingestion and index/UI checks.
