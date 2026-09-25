# Stage 5: persistent semantic search

**Technical Stage 5 is complete.** The local `ev_policy_draft` Chroma collection contains all 231 draft chunks: Maharashtra 53, Tamil Nadu 78 and Central 100. Each saved record retains its text, source/page fields, relationship links and pending-review flags. The index uses local `nomic-embed-text` embeddings with 768 dimensions and cosine distance.

## Run this stage

From the project folder, start Ollama with `nomic-embed-text` installed and open `EV Policy Assistant.ipynb` in the pinned Python environment. Run only the **Stage 5** cells in order; the earlier stages and Groq key are not needed. The inputs cell checks the saved ingestion artifacts and looks up the installed model digest without embedding text.

- **Existing local index:** leave `rebuild_index = False`. The notebook opens and checks the saved collection, then embeds the smoke-search question only.
- **Fresh checkout, changed chunks/model or failed build:** first rerun any affected ingestion stage. Set `rebuild_index = True`, run the Stage 5 cells, then return it to `False`. This deliberately embeds the full corpus and replaces this project's `ev_policy_draft` collection.
- **Checks:** expect 231 records, 768-dimensional vectors and eight passed notebook checks. The smoke query returns raw candidate passages with state/document/physical-page labels; it does not generate an answer.

The update policy is an explicit full rebuild. This was the assistant's stated recommended assumption after the optional update-policy question received no answer. Reopening never silently rebuilds or inserts documents. Text, metadata or model-digest changes require a deliberate rebuild. Run one notebook/kernel at a time and close other search sessions before rebuilding. An interrupted build leaves no completed receipt; rerun the full build to recover.

Local files are under `data/chroma/`, excluded from Git. `index_manifest.json` records the corpus digest, model digest/settings, counts and build time. The canonical notebook is committed with `rebuild_index = False` and no outputs. Keep the installed model version consistent; the check report records the model digest used here.

## Reuse and checks

Lab 4 cells 38, 106–108 and 124 provide `OllamaEmbeddings`, `Chroma`, `add_documents` and `.as_retriever().invoke()`. Lab 5 cell 17 provides persistence. This stage adds reproducible IDs, batched insertion of every chunk, a build receipt, exact saved-text/metadata comparison and separate build/open functions. The [official Chroma integration](https://docs.langchain.com/oss/python/integrations/vectorstores/chroma) documents persistence and retrieval; [Ollama's model-list endpoint](https://docs.ollama.com/api/tags) supplies the installed model digest. Implementation was checked against the locally pinned library source.

Run the repeatable persistence checks with:

```sh
uv run --locked python checks/stage5_index_checks.py
```

The script reads the main 231-record index and opens it in a separate Python process with document embedding forbidden. It verifies zero embedding calls at open and one query embedding for search. Six real chunks covering all three jurisdictions exercise repeated full rebuilds, changed text/metadata/model, additions/removals, invalid input, altered/missing saved records and missing/corrupt receipts in temporary stores. A simulated interruption after a 32-record batch verifies rejection and recovery. The 16 checks passed. The production index is never modified by these tests.

Observed reports: [notebook checks](data/processed/search/stage5_checks.json) and [persistence checks](data/processed/search/stage5_persistence_checks.json). A fresh Jupyter kernel also passed the Stage 5 section with the default reopen setting. Earlier stages reproduce their six page/chunk files byte-for-byte. No dependency or source PDF changed.

## Stage boundary

This is an **unfiltered development index**. Search can return different jurisdictions and older provisions. It does not yet follow amendment/conditions links, establish active benefits, generate answers or serve a UI. All source acceptance and entitlement-permission flags remain false. Manual review and the team's independently authored evaluation set are still deferred.

AI assistance covered notebook implementation, the persistence-check script, actual execution, documentation and Git publication. The smoke query and test fixtures are technical checks, not human-authored evaluation cases. Next is **Stage 6: jurisdiction-aware retrieval**, including the agreed handling of state/question conflicts and applicable source versions.
