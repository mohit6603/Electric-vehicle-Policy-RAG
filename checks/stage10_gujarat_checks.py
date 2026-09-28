"""Check Gujarat ingestion/retrieval; --live adds two Gradio/Groq development cases."""
import argparse
import copy
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from gradio_client import Client
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda
from stage8_failure_checks import load_stage8
from stage9_ui_checks import run_cell


def run_checks(live=False, case=None):
    stage = load_stage8()
    counts = {'corpus': 0, 'query': 0}
    base = stage['OllamaEmbeddings']

    class QueryOnly(base):
        def embed_documents(self, texts):
            counts['corpus'] += 1
            raise AssertionError('Restart must not embed the corpus.')

        def embed_query(self, text):
            counts['query'] += 1
            return base.embed_documents(self, [text])[0]

    def no_rebuild(*args, **kwargs):
        raise AssertionError('No implicit rebuild allowed.')

    stage.update(OllamaEmbeddings=QueryOnly, rebuild_policy_index=no_rebuild)
    checks, observations = [], []
    result = stage['start_policy_assistant']()
    assert result['status'] == 'ready', result
    assert counts == {'corpus': 0, 'query': 0}
    assert stage['vector_store_chroma']._collection.count() == stage['index_spec']['chunk_count']
    assert stage['index_spec']['chunks_by_state']['Gujarat'] == 31
    checks += ['reopen_all_records_without_corpus_embedding', '31_gujarat_chunks']
    for selection in ('Gujarat', 'Gujrat', 'GJ'):
        result = stage['route_policy_question'](selection, 'What purchase incentive is described?')
        assert result['jurisdiction'] == 'Gujarat', result
    checks.append('three_gujarat_aliases')
    policy = 'gujarat_policy_2021-06-23'
    tax = 'gujarat_motor_vehicle_tax_2025-04-17'
    extension = 'gujarat_motor_vehicle_tax_extension_2026-03-30'
    questions = [
        ('What two-wheeler purchase incentive rate, battery capacity limit, ex-factory price ceiling, policy period and scheme-stacking conditions did the 2021 policy state?',
         [f'{policy}:p3', f'{policy}:p4', f'{policy}:p5']),
        ('What tax rates and rebates are listed for electric auto rickshaws licensed for up to three passengers, and what deadline does the 2026 extension state?',
         [f'{tax}:p1', f'{tax}:p2', f'{extension}:p4', f'{extension}:p5']),
        ('What charging-station equipment subsidy, cap, station count and other-subsidy exclusion did the 2021 policy describe?',
         [f'{policy}:p3', f'{policy}:p5', f'{policy}:p6']),
        ('What tax rate, rebate and effective rate are listed for electric private service vehicles transporting educational-institution students or staff?',
         [f'{tax}:p1', f'{tax}:p3', f'{extension}:p5']),
        ('What historical manufacturing-policy reference and charging tariff conditions are stated?',
         [f'{policy}:p3', f'{policy}:p6']),
    ]
    required = set(stage['retrieval_rules']['required_pages']['Gujarat'])
    for question, expected in questions:
        result = stage['retrieve_policy']('Gujarat', question, k=1)
        assert result['status'] == 'retrieved', result
        docs = result['context_docs']
        assert {d.metadata['state'] for d in docs} == {'Gujarat'}
        assert required.union(expected) <= {d.metadata['page_id'] for d in docs}, question
        assert {d.metadata['policy_year'] for d in docs} <= {2021, 2025, 2026}
        assert all(d.metadata['context_role'] == 'historical_only'
                   for d in docs if d.metadata['source_id'] == policy)
        context = '\n'.join(d.page_content for d in docs)
        assert 'Admission Committee' not in context and 'REVENUE DEPARTMENT' not in context
        if any(d.metadata['source_id'] == tax for d in docs):
            assert '31st March, 2027' in context
        if question == questions[0][0]:
            assert {d.metadata['source_id'] for d in docs} == {policy}
        size = sum(len(d.page_content) for d in docs)
        assert size < 50000
        observations.append({'question': question, 'page_ids': [d.metadata['page_id'] for d in docs],
                             'context_chars': size, 'status': result['status']})
    checks += ['five_filtered_semantic_queries', 'conditions_and_continuations_present', 'historical_context_isolated_and_tax_chain_complete']
    sizes = []
    for page_id in (p for p in stage['retrieval_page_by_id'] if p.startswith('gujarat_')):
        chunk = next(d for d in stage['index_documents'] if d.metadata['page_id'] == page_id)
        docs, omitted = stage['assemble_policy_context']([chunk], 'Gujarat')
        if page_id.startswith((tax, extension)):
            assert {f'{tax}:p1', f'{tax}:p2', f'{tax}:p3', f'{extension}:p4', f'{extension}:p5'} <= {d.metadata['page_id'] for d in docs}
            assert len(omitted) == 2
        else:
            assert {d.metadata['source_id'] for d in docs} == {policy}
            assert len(omitted) in (0, 1)
        assert all('Admission Committee' not in d.page_content and 'REVENUE DEPARTMENT' not in d.page_content for d in docs)
        size = sum(len(d.page_content) for d in docs)
        assert size < 50000, (page_id, size)
        sizes.append(size)
    assert len(sizes) == 10
    observations.append({'all_page_context_range': [min(sizes), max(sizes)]})
    checks.append('all_10_pages_assemble_with_hashed_exclusions_within_limit')
    fixture = stage['retrieve_policy']('Gujarat', questions[0][0], k=1)
    _, sources = stage['label_answer_evidence'](fixture)
    label = next(key for key, doc in sources.items() if doc.metadata['page_id'] == f'{policy}:p5')
    retrieve, llm = stage['retrieve_policy'], stage['get_answer_llm']
    try:
        stage['retrieve_policy'] = lambda *args, **kwargs: fixture
        for claim in ('Only vehicles with 2 kWh batteries are eligible.', 'Only two kilowatt-hour batteries qualify.'):
            payload = {'status': 'supported', 'points': [{'text': claim, 'citations': [label]}]}
            stage['get_answer_llm'] = lambda: RunnableLambda(lambda prompt: AIMessage(content=json.dumps(payload)))
            result = stage['answer_question']('Gujarat', 'What historical purchase rate was stated?')
            assert result['status'] == 'not_established' and result['reason'] == 'gujarat_battery_limit_review_pending'
            assert result['points'] == [] and result['sources'] == []
    finally:
        stage['retrieve_policy'], stage['get_answer_llm'] = retrieve, llm
    checks.append('known_generated_battery_limit_claims_withheld')
    points = [{'text': 'The printed rate is Rs 10,000 per kWh.', 'citations': [{'source_id': label}]}]
    rendered, _ = stage['render_policy_answer'](points, sources, 'Gujarat', stage['retrieval_cutoff'])
    assert 'Historical provision: The printed rate' in rendered
    assert points[0]['text'] == 'The printed rate is Rs 10,000 per kWh.'
    checks.append('historical_evidence_label_is_rendered')
    before = copy.deepcopy(counts)
    for selection, question, status in [
        ('GJ', 'Tamil Nadu purchase subsidy?', 'clarification_required'),
        ('Gujarat', 'Compare Gujarat and Maharashtra incentives', 'clarification_required'),
        ('Karnataka', 'Electric car subsidy?', 'unsupported_jurisdiction'),
        ('Gujarat', '', 'clarification_required'),
        ('Gujarat', 'Can I claim an EV subsidy today?', 'not_established'),
        ('Gujarat', questions[0][0], 'not_established'),
    ]:
        result = stage['ask_policy'](selection, question)
        assert result['status'] == status and not result['sources'], result
        observations.append({'selection': selection, 'question': question, 'result': result})
    assert counts == before
    checks.append('six_rejections_skip_models_and_clear_sources')
    for cell in ('stage9-callback', 'stage9-startup', 'stage9-interface'):
        run_cell(stage, cell)
    assert stage['ui_choices'] == sorted(stage['index_spec']['chunks_by_state'])
    assert 'Gujarat' in stage['ui_choices']
    checks.append('gradio_lists_gujarat_and_other_loaded_jurisdictions')
    report_path = Path('data/processed/gujarat/stage10_live_checks.json' if live
                       else 'data/processed/gujarat/stage10_integration_checks.json')
    if case:
        report_path = report_path.with_name(f'stage10_live_{case}.json')

    def save(status):
        report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
            'notebook_sha256': stage['index_file_hash']('EV Policy Assistant.ipynb'),
            'check_script_sha256': stage['index_file_hash'](__file__),
            'source_manifest_sha256': stage['index_file_hash']('data/source_manifest.json'),
            'retrieval_rules_sha256': stage['index_file_hash']('data/retrieval_rules.json'),
            'index_spec': stage['index_spec'], 'technical_status': status,
            'scope': 'AI development checks; not team source review or formal evaluation',
            'checks_passed': checks, 'embedding_calls': counts, 'observations': observations}
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')

    save('passed')
    if not live:
        print('Stage 10 Gujarat integration checks passed:', len(checks), flush=True)
        return
    cases = [
        ('historical_rate', 'According to the historical 2021 policy, what two-wheeler demand incentive rate and ex-factory price ceiling were stated, and what was the policy period?',
         [r'10,?000', r'kWh', r'1\.5', r'2021', r'2025|four years|4 years'],
         [f'{policy}:p3', f'{policy}:p5']),
        ('tax_extension', 'According to the supplied tax notifications, for electric auto rickshaws licensed to carry up to three passengers, what are the existing tax rate, rebate and effective rate, their cost basis, the electric-power qualification and the deadline after the 2026 amendment? Does this tax extension renew the 2021 purchase subsidy?',
         [r'2\.5', r'1\.5', r'1\s*%|1\s*per\s*cent|one\s*per\s*cent',
          r'cost', r'exclusiv', r'battery', r'2027', r'31.*March|March.*31',
          r'not.*renew|does not extend|no.*renew|does not.*purchase|tax.only'],
         [f'{tax}:p1', f'{tax}:p2', f'{extension}:p5']),
    ]
    if case:
        cases = [item for item in cases if item[0] == case]
    ask, outputs = stage['ask_policy'], []

    def observed_ask(selection, question):
        result = ask(selection, question)
        outputs.append(result)
        return result

    stage['ask_policy'] = observed_ask
    demo = stage['demo']
    try:
        _, url, _ = demo.launch(server_name='127.0.0.1', share=False, prevent_thread_lock=True,
                               show_error=False, show_api=False, quiet=True)
        client = Client(url, verbose=False)
        for position, (name, question, patterns, expected_pages) in enumerate(cases):
            if position:
                time.sleep(60)
            rendered = client.predict('Gujarat', question, api_name='/answer_policy')
            result = outputs[-1]
            observations.append({'case': name, 'question': question, 'result': result, 'ui_outputs': rendered})
            save('running')
            assert result['status'] == 'document_answer', (name, result)
            assert all(re.search(p, result['answer'], re.I) for p in patterns), (name, result['answer'])
            assert all(any(page in source['evidence_id'] for source in result['sources']) for page in expected_pages), name
            if name == 'historical_rate':
                assert re.search(r'historical|expired|operated|was|were|past', result['answer'], re.I)
            assert all(s['state'] == 'Gujarat' and '#page=' in s['official_url'] for s in result['sources'])
            assert '#page=' in rendered[0] and '#page=' in rendered[1]
            checks.append('live_gradio_'+name)
            print('Live Gujarat case passed:', name, flush=True)
        rendered = client.predict('Gujarat', 'Compare Gujarat and Tamil Nadu EV subsidies', api_name='/answer_policy')
        assert outputs[-1]['status'] == 'clarification_required'
        assert rendered[1] == '### Sources\n\nNo sources cited.'
        checks.append('gradio_rejection_clears_previous_citations')
        rendered = client.predict('Gujarat', questions[0][0], api_name='/answer_policy')
        assert outputs[-1]['status'] == 'not_established'
        assert outputs[-1]['reason'] == 'gujarat_battery_limit_review_pending'
        assert rendered[1] == '### Sources\n\nNo sources cited.'
        checks.append('gradio_ambiguous_battery_request_abstains')
        save('passed')
    except Exception:
        save('failed')
        raise
    finally:
        demo.close()
    print('Stage 10 Gujarat live checks passed:', len(checks), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--case', choices=['historical_rate', 'tax_extension'])
    args = parser.parse_args()
    assert not args.case or args.live, '--case requires --live'
    run_checks(args.live, args.case)
