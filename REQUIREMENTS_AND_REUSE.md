# EV Policy Assistant: requirements and course-code reuse

Reviewed on 22 September 2026. This is a planning and code-review aid, not an implemented assignment or a submission-ready package.

The attached assignment instructions are the assignment specification. The EV idea PDF adds the team's proposed scope. The user confirmed that the instructor approved the four-member group and asked to keep AI assistance within the helper-only limit. No assignment solution code has been written.

## Sources and decisions

- Assignment: `Assignment3_MiniProject_Instructions (1).pdf`, both pages, including the slide table and penalties.
- Proposal: `EV_Policy_Assistant_Idea_Submission.pdf`, page 1.
- Course repository: [aagarwal4/generative-ai-pgp-ji-2026](https://github.com/aagarwal4/generative-ai-pgp-ji-2026/tree/33c2faa22450cde16ead9071f7ce7ecc78ca592a), commit `33c2faa22450cde16ead9071f7ce7ecc78ca592a`.
- A local-only reference checkout is available at `tmp/reference-repo/`, excluded from this project's Git history. Use the linked course commit to obtain the reference files elsewhere. Its assignment-3 PDF has the same substantive requirements as the attached instructions; the extraction differs only in one hyphen's spacing.
- Group: Mohit Patle (27PGAI0102), Pushkar Brahmankar (27PGAI0100), Vaishnavi B (27PGAI0120), Sehal Chodankar (27PGAI0116). Four-person exception confirmed by the user; the written PDF itself says three.
- Section 8 says, "AI tools may be used only as a helper for the code." It also specifies a 30% flat penalty for detected AI-generated code and requires an appendix disclosure. Style matching or a disclosure does not waive this restriction.
- Subsequent scope decisions are recorded in `STAGED_PLAN.md`: eight specified jurisdictions (seven states plus Delhi), current-benefit verification through a date still to be agreed, and one jurisdiction per query. The proposal's original 8–10-state wording is preserved below for traceability; the user clarified the implementation scope.

## Assignment requirements

| ID | Requirement from the assignment | Where it belongs / evidence needed | Current status |
|---|---|---|---|
| A1 | Group of 3 | Team roster | Four members approved, as confirmed by the user |
| A2 | RAG with a custom dataset and problem statement | EV corpus, retrieval and generation implementation; business explanation | Proposed, not implemented |
| A3 | Agents are optional | LangGraph only if the team implements the optional comparison path | Optional |
| A4 | Idea PDF: member names and IDs, problem and why worthwhile, proposed approach, tech stack | Existing idea PDF | All four content categories present |
| A5 | Idea due 22 September 2026, EOD; every member uploads a PDF on Digiicampus | Individual upload confirmations | Uploads not verified |
| A6 | Final code: GitHub link of the project repository | The team's own runnable project repository and its URL | Repository created at https://github.com/mohit6603/Electric-vehicle-Policy-RAG; planning documents only, implementation pending |
| A7 | Exactly 3 presentation slides | Slide 1: business impact. Slide 2: technical stack and GenAI architecture flow. Slide 3: appendix including AI disclosure | Not authored |
| A8 | Every member submits final ZIP on Digiicampus | ZIP containing the repository link and the 3-slide presentation; individual upload confirmations | Not prepared/submitted |
| A9 | Final submission date/time to be announced | Check the announced course deadline | TBD in the PDF |
| A10 | 8-minute team presentation and live demo, approximately 3–4 minutes of Q&A | Rehearsed running application and explanation | Not performed; date/time TBD |
| A11 | Mainly classroom stack and syntax; explain additional syntax | Reuse map below and implementation notes | Reference code inspected |
| A12 | AI only as code helper; brief disclosure in appendix | Student implementation, record of actual AI assistance | Helper-only scope confirmed |
| A13 | Main grading is the demo: technical 80%, presentation including narrative 20% | Working demo, defensible design choices, clear deck | No grades or performance claims made |
| A14 | Any member's late submission or editing GitHub after the deadline can penalize the whole group, including a possible zero | All-member upload check; preserve submitted GitHub revision after deadline | Team action at submission |

The PDF does not specify a minimum accuracy, a mandatory test framework, hosting, a recorded video, a written report, mandatory agents, or a finer technical marking breakdown. Do not present these as grading requirements. A source-code copy inside the ZIP can be useful, but the stated code deliverable is the GitHub link.

## Repository structure and style

The repository is primarily teaching notebooks, organized into `class-labs/`, `class-exercises/exercise-N/`, and `assignments/assignment-N/`. It is not a packaged application with service, controller, or repository layers. The root has `pyproject.toml`, `uv.lock`, `.env.example`, and `.gitignore`.

The closest implementation models are Lab 4 and Exercise 2's completed notebook. They use top-level setup and indexing cells, ordinary lists and dictionaries, snake_case names, four-space indentation in the main Python example, short section comments, and a few direct functions. Names include `embeddings_model`, `vector_store_chroma`, `retriever`, `context_docs`, `relevant_text`, `get_llm`, and `gradio_interface`. Comments and quote spacing are inconsistent across notebooks; follow the relevant example without intentionally reproducing mistakes.

Error handling is local: Exercise 2 prints a message when a row cannot be loaded, catches `OutputParserException` after structured generation, and uses `ValueError` for an invalid model. Most lab cells let failures surface. A small number of understandable validation checks fits this style. Custom exception hierarchies, dependency injection, elaborate configuration classes, and a web backend are not needed for the proposed project.

Use the class's `init_chat_model`, `ChatPromptTemplate`, `Document`, `OllamaEmbeddings`, `Chroma`, `.as_retriever()`, `.invoke()`, and `template | llm` patterns where applicable. The grocery output schemas/gallery and finance-specific assignment rules do not transfer to EV policy QA.

## Exact reuse map

Cell numbers below are **1-based positions counting both markdown and code cells**, not execution counts. Cell IDs make the references unambiguous at the reviewed commit.

| Alias | Repository file |
|---|---|
| L4 | `class-labs/4. Retrieval Augmented Generation (RAG).ipynb` |
| L5 | `class-labs/5. Advanced RAG with LangChain.ipynb` |
| L6 | `class-labs/6. RAG With LangGraph.ipynb` |
| L8 | `class-labs/8. Introduction to Agents with LangGraph.ipynb` |
| E2 | `class-exercises/exercise-2/exercise2_solution.ipynb` |
| E2 starter | `class-exercises/exercise-2/exercise2_starter_code.py` |

| Proposal requirement | Existing code to reuse | Adaptation the team must make | Verification |
|---|---|---|---|
| P1. Official PDFs for 8–10 states plus central scheme | No EV dataset or policy downloader exists. L4 cells 65–66 demonstrate PDF ingestion | Assemble and document the official corpus; check extraction before accepting a PDF | Count distinct states separately from central; inspect source pages and extracted text |
| P2. Load PDF text | L4 cell 65 `UnstructuredPDFLoader`; cell 66 `loader = UnstructuredPDFLoader(...)`, `data = loader.load()` | Replace the research-paper source; deliberately preserve page provenance. Its `hi_res`/image/table options are a demonstration, not all mandatory | Inspect policy tables, bilingual pages, and empty/scanned pages; do not silently index unreadable evidence |
| P3. Chunk loaded documents | L4 cell 77 `RecursiveCharacterTextSplitter`, `split_documents(docs)`; L5 cell 25 repeats it | Feed actual policy documents; begin with the class's 1000-character size and 200-character overlap, then inspect evidence | Every chunk has usable source metadata; amounts remain associated with their vehicle category and conditions |
| P4. State, policy year and page metadata; document identity for citations | E2 cell 9 constructs `Document(page_content=page_text, metadata=metadata)`; E2 starter lines 23–41 | Replace grocery fields with policy metadata before splitting; retain document title, official URL and consistent page numbering | Inspect records from multiple states and verify their PDF pages |
| P5. Local `nomic-embed-text` embeddings | L4 cells 37–38, `OllamaEmbeddings(model="nomic-embed-text")`; E2 cell 12 | Reuse the model and embedding pattern | Same embedding model used when building and querying; local Ollama available |
| P6. Persisted Chroma, without startup rebuild | L5 cell 17 `Chroma(..., persist_directory="./chroma_langchain_db")`; L4 cells 106–108 initialize and add documents | Use an EV collection and a known path; separate index-building from application startup; ingest all accepted chunks | Restart opens existing collection without re-embedding; repeated ingestion does not multiply identical chunks |
| P7. Restrict retrieval to the question's state | L4 cell 127 `.as_retriever(search_kwargs={"filter": {"source": ...}})`; cell 129 `.invoke(question)`; cell 124 demonstrates `k` | Filter on policy `state` instead of webpage `source`; define dropdown/question agreement and a separate central option | Every retrieved document has the requested jurisdiction; mismatches and unsupported states are handled explicitly |
| P8. Groq `openai/gpt-oss-120b` through `init_chat_model` | L4 cell 150; L5 cell 11; E2 cell 18 `get_llm` | Reuse the single proposed model; model selector is unnecessary unless the team has a reason | Successful authenticated invocation; no secrets committed |
| P9. Grounded answers and abstention | L4 cells 153–155 `ChatPromptTemplate` and `prompt | llm`; cells 158–162 demonstrate a hub prompt that says not to guess; E2 cell 20 `generate_cart` shows retrieve → format → invoke | Write the team's EV-specific instructions; include labelled evidence; handle empty/insufficient context and avoid importing unrelated grocery constraints | Supported answer agrees with evidence; unsupported answer says the available documents do not establish it |
| P10. Show state, document and page | E2 cell 20's context construction is a starting pattern, but joins only `page_content`; no citation implementation exists | Include metadata when formatting context and return verifiable source references with the answer | Every cited page exists and supports the claim; do not treat all retrieved pages as proven support |
| P11. Gradio state picker and question input | E2 cells 23–24 `gradio_interface`, `gr.Interface`, `demo.launch`; cells 26–28 show a Blocks alternative. E2 starter lines 95–133 | Replace model/grocery inputs and gallery with jurisdiction, question, answer and sources | State is actually passed to retrieval; error cases return the expected outputs |
| P12. 20–30 self-written questions with known PDF answers | L4 cells 111, 156 and 162 illustrate an out-of-context question only. No evaluation dataset or scoring harness exists | Students write questions and verify answers/pages before running the app; log actual outcomes | Separate retrieval failures, answer errors and citation errors; no invented results |
| P13. Optional comparison router | L6 cells 32–34 `State`, `retrieve`, `generate`, `StateGraph`; L8 cell 19 demonstrates `add_conditional_edges` for tool routing | A two-state comparison route is new work. Retrieve independently for each state and keep sources separate | Compare evidence without cross-state attribution; retain abstention for either missing side |

### Cell IDs for direct navigation

| File | Cell → ID |
|---|---|
| L4 | 37 → `d1f0a862`; 38 → `3d9ca667`; 65 → `72c38057`; 66 → `1aa9de96`; 77 → `fda795c4` |
| L4 | 106 → `5506ff49`; 107 → `f8d19997`; 108 → `c96ac39b`; 111 → `02c9f71b`; 124 → `eee65b21`; 127 → `17d9e4c3`; 129 → `e140f976` |
| L4 | 150 → `a8995b34`; 153 → `2431c60b`; 154 → `297a12ce`; 155 → `787ddbaa`; 156 → `90447bb3`; 158 → `85a6dc7b`; 159 → `8b5745a1`; 160 → `49508d21`; 161 → `cb251f7c`; 162 → `d198386a` |
| L5 | 11 → `00448d6c-cfb0-4177-99f9-702827acecb8`; 17 → `a14351ef-15fd-4aeb-8553-4c6f7018aa5b`; 25 → `10618d57-9450-4c38-b080-087b62194091`; 28 → `9af9b9ec-18d8-443f-b38c-9a93f937595c` |
| E2 | 9 → `1c772180-6fcb-4b17-bbb0-47a2d6730f40`; 12 → `325c79ba-d931-467e-b691-31c812ff3fc5`; 18 → `decfeaf2-9bcc-41b8-8880-98b12caf61ea`; 20 → `12d4018e-e25d-4213-bc3f-ce0ca3a278a0` |
| E2 | 23 → `19f83764-2089-490d-9d02-19d6d80f63f8`; 24 → `8730ccb2-0f79-4b03-b7a5-4019629964b1`; 26 → `f6778429-f3e0-481a-aa4e-d288cc5bdc0e`; 27 → `69afab14-756e-4b87-b320-81523402074c`; 28 → `ae0d63bd-03c6-42eb-991a-c6c87ed914f6` |
| L6 | 32 → `7ae490dd-bc96-4659-babc-446e45931203`; 33 → `05cc2de3-14c7-4aa0-b4b9-b909e4e67b34`; 34 → `1cf71916-f7e6-40f2-871d-ac75c87d55cc` |
| L8 | 19 → no cell ID; locate `builder.add_conditional_edges` |

## Reuse caveats found in the code

1. L4's PDF output is called `data`, while its recursive splitter later uses `docs` from the webpage example. Running the whole notebook unchanged does not make the PDF the indexed corpus.
2. L4 cell 107 comments out `persist_directory`. L5 cell 17 enables it, but cell 28 indexes only the first ten chunks for speed. E2 cell 13 indexes only 100 grocery records and does not specify persistence.
3. L4/L5 generate fresh UUIDs before each insertion. Re-running ingestion into a persistent collection can duplicate content. The student implementation needs an explicit rebuild/update decision.
4. L4 cell 165 uses `prompt` rather than `prompt_hub_rag`, despite the preceding hub discussion. Its `ensemble_retriever` also uses an unfiltered BM25 branch. Copying that chain would not automatically preserve abstention or state isolation.
5. E2 cell 20 and L6 `generate` join only page text. Neither implements page citations. Formatting metadata into evidence is a real addition, not an existing feature.
6. E2 cell 6 uses `getpass` without importing it in cell 4. The standalone starter also contains unfinished names and TODOs. Neither should be described as ready to run unchanged.
7. Lab 7 is a conceptual markdown cell about multimodal RAG, not an implemented table-extraction pipeline. Lab 6 uses FAISS; only its graph organization transfers to the proposed Chroma solution.
8. Course examples print diagnostics and sometimes suppress warnings globally. Keep useful diagnostic output while developing; do not hide failed ingestion or missing services just to imitate notebook style.

## Dependency baseline

The course `pyproject.toml` says Python `>=3.12`; the proposal specifically chooses Python 3.12. The following are versions recorded in the reviewed `uv.lock`, not a claim that this project's environment has been installed or tested:

| Dependency | Locked version |
|---|---|
| langchain | 0.3.25 |
| langchain-core | 0.3.76 |
| langchain-community | 0.3.24 |
| langchain-text-splitters | 0.3.8 |
| langchain-chroma / chromadb | 0.2.6 / 1.0.20 |
| langchain-ollama | 0.3.7 |
| langchain-groq | 0.3.8 |
| gradio | 5.31.0 |
| python-dotenv | 1.1.0 |
| pypdf / unstructured | 6.1.1 / 0.18.14 |
| langgraph (optional) | 0.4.7 |

Start from the course environment when possible. A smaller environment should retain compatible classroom versions and be tested by the team; blindly installing the latest packages is not equivalent to reproducing the class setup. Copying every course dependency is also unnecessary for this project's scope.

## What this review establishes

Both PDFs were read and their rendered pages inspected. The reference repo's source cells, starter script, manifest and lockfile were inspected. The mapping distinguishes working examples, partial examples and genuine gaps. The user subsequently created the project repository for these planning documents. At the initial review, no corpus, application, model checks, evaluation, deck or submission had been completed. Subsequent environment checks are recorded in `PROGRESS.md`; policy implementation and its evaluation remain later-stage work.
