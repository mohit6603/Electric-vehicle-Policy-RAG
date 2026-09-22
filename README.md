# Electric Vehicle Policy RAG

An EV policy assistant planned for the Generative AI mini-project at Jio Institute. It will answer questions from official policy documents, with jurisdiction filtering and document/page citations.

**Status:** planning only. Application implementation has not started.

## Project documents

- [Staged plan](STAGED_PLAN.md): 30–45-minute work sessions, acceptance checks and current decisions.
- [Implementation guide](IMPLEMENTATION_GUIDE.md): technical workflow and validation guidance.
- [Requirements and reuse map](REQUIREMENTS_AND_REUSE.md): assignment requirements and exact classroom-code references.

## Agreed scope

Coverage: Maharashtra, Tamil Nadu, Uttar Pradesh, Delhi (NCT), Gujarat, Telangana, Karnataka and Madhya Pradesh, plus a central scheme to be selected during source review. Answers will address one jurisdiction per query. Comparisons are deferred.

The corpus will use official documents and amendments to verify benefits through a fixed cutoff. The cutoff date and final stage-plan agreement are still pending.

Planned stack: Python 3.12, LangChain, local Ollama embeddings (`nomic-embed-text`), persisted Chroma, Groq (`openai/gpt-oss-120b`) and Gradio.

## Reference and assistance

Implementation will adapt applicable examples from the [course repository](https://github.com/aagarwal4/generative-ai-pgp-ji-2026/tree/33c2faa22450cde16ead9071f7ce7ecc78ca592a). The reuse map records the relevant notebooks and cells.

AI assistance so far has covered requirements review, repository inspection, planning documentation and Git setup. No application code or evaluation results have been generated. Assistance remains within the agreed helper-only scope, and its actual use will be disclosed in the presentation appendix.
