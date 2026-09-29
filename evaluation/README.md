# Team evaluation — pending

`team_cases.json` contains 24 empty slots, not an AI-written question set or completed evaluation. Two cases belong to each of the eight jurisdictions, four to Central and four to negative/ambiguous behavior. Independently write the question, expected answer and physical source page IDs from the original PDFs before inspecting model output. Include relevant amendments/expiry conditions. Enter actual author/reviewer names and dates.

After the consolidated source/prompt review, update actual acceptance records and rerun affected ingestion/index checks. Current-benefit gaps remain separate and must not be marked resolved without evidence. The runner refuses formal evaluation while sources are unaccepted or cases are incomplete.

From the project root:

```sh
uv run --locked python evaluate.py --freeze
uv run --locked python evaluate.py --batch 1
uv run --locked python evaluate.py --batch 2
```

Freeze records the case file, notebook, corpus, retrieval rules, OCR review, dependency lock and runner hashes. Batches record actual retrieval page IDs, responses, citations and statuses after each case. Restart skips recorded cases. Requests are paced by 60 seconds; service failures remain recorded and never count as successful abstention. Preserve failed runs before conducting a separately versioned retry. The runner does not invent semantic grades: fill retrieval/answer/citation correctness and reviewer notes after comparing output with frozen expectations. Report actual numerators and denominators, and classify service failures separately.

No formal cases have run. Existing Stage 7–10 development observations are not substitutes for these independent cases. Stages 11–12 remain pending team inputs.
