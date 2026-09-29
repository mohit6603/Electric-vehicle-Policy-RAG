"""Check Telangana ingestion/retrieval; --live adds two Gradio/Groq development cases."""
import argparse
import copy
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from gradio_client import Client
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
    assert stage['index_spec']['chunks_by_state']['Telangana'] == 32
    checks += ['reopen_all_records_without_corpus_embedding', '32_telangana_chunks']
    for selection in ('Telangana', 'Telengana', 'TS'):
        result = stage['route_policy_question'](selection, 'What purchase incentive is described?')
        assert result['jurisdiction'] == 'Telangana', result
    checks.append('three_telangana_aliases')
    policy = 'telangana_policy_2020'
    tax = 'telangana_tax_fee_2024-11-16'
    questions = [
        ('What road tax and registration fee exemption, deadline and vehicle-count limit does the 2024 notification state for private electric cars?', [f'{tax}:p1']),
        ('What retrofit incentive rate, per-vehicle cap and vehicle-count limit does the policy state for three-seater auto rickshaws?', [f'{policy}:p10']),
        ('What highway charging-station spacing and residential-township size does the policy encourage?', [f'{policy}:p11']),
        ('What investment or employment threshold defines a mega manufacturing project?', [f'{policy}:p13']),
        ('What net SGST annual cap, cumulative cap and reimbursement period are stated for mega enterprises?', [f'{policy}:p13']),
    ]
    required = set(stage['retrieval_rules']['required_pages']['Telangana'])
    for question, expected in questions:
        result = stage['retrieve_policy']('Telangana', question, k=1)
        assert result['status'] == 'retrieved', result
        docs = result['context_docs']
        assert {d.metadata['state'] for d in docs} == {'Telangana'}
        assert required.union(expected) <= {d.metadata['page_id'] for d in docs}, question
        assert all(d.metadata['policy_year'] in (2020, 2024) for d in docs)
        size = sum(len(d.page_content) for d in docs)
        assert size < 50000
        observations.append({'question': question, 'page_ids': [d.metadata['page_id'] for d in docs],
                             'context_chars': size, 'status': result['status']})
    checks += ['five_filtered_semantic_queries', 'conditions_and_continuations_present', 'only_two_registered_telangana_sources']
    sizes = []
    for page_id in (p for p in stage['retrieval_page_by_id'] if p.startswith('telangana_')):
        chunk = next(d for d in stage['index_documents'] if d.metadata['page_id'] == page_id)
        docs, omitted = stage['assemble_policy_context']([chunk], 'Telangana')
        assert all(item['page_id'] == f'{policy}:p10' for item in omitted)
        assert len(omitted) in (0, 7)
        size = sum(len(d.page_content) for d in docs)
        assert size < 50000, (page_id, size)
        sizes.append(size)
    assert len(sizes) == 13
    observations.append({'all_page_context_range': [min(sizes), max(sizes)]})
    checks.append('all_13_pages_assemble_within_context_limit')
    chunk = next(d for d in stage['index_documents'] if d.metadata['page_id'] == f'{policy}:p10')
    docs, omitted = stage['assemble_policy_context']([chunk], 'Telangana')
    text = '\n'.join(d.page_content for d in docs if d.metadata['page_id'] == f'{policy}:p10')
    assert len(omitted) == 7
    assert '15%' in text and '15,000' in text and '5,000 retrofit' in text
    assert '2,00,000' not in text and '20,000' not in text and 'first 500 Electric buses' not in text
    assert 'first 5,000 Electric 4-Wheeler' not in text
    updated = next(d for d in docs if d.metadata['page_id'] == f'{tax}:p1')
    assert 'irrespective of the number' in updated.page_content
    assert updated.metadata['text_status'] == 'ai_proposal' and 'text_derivation' in updated.metadata
    checks.append('old_tax_quotas_excluded_retrofit_and_ocr_update_preserved')
    before = copy.deepcopy(counts)
    for selection, question, status in [
        ('TS', 'Tamil Nadu purchase subsidy?', 'clarification_required'),
        ('Telangana', 'Compare Telangana and Maharashtra incentives', 'clarification_required'),
        ('Madhya Pradesh', 'Electric car subsidy?', 'unsupported_jurisdiction'),
        ('Telangana', '', 'clarification_required'),
        ('Telangana', 'Can I claim an EV subsidy today?', 'not_established'),
    ]:
        result = stage['ask_policy'](selection, question)
        assert result['status'] == status and not result['sources'], result
        observations.append({'selection': selection, 'question': question, 'result': result})
    assert counts == before
    checks.append('five_rejections_skip_models_and_clear_sources')
    for cell in ('stage9-callback', 'stage9-startup', 'stage9-interface'):
        run_cell(stage, cell)
    assert stage['ui_choices'] == sorted(stage['index_spec']['chunks_by_state'])
    assert 'Telangana' in stage['ui_choices']
    checks.append('gradio_lists_telangana_and_other_loaded_jurisdictions')
    report_path = Path('data/processed/telangana/stage10_live_checks.json' if live
                       else 'data/processed/telangana/stage10_integration_checks.json')
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
        print('Stage 10 Telangana integration checks passed:', len(checks), flush=True)
        return
    cases = [
        ('private_car_tax', questions[0][0],
         [r'100\s*%', r'road tax', r'registration', r'2026', r'31', r'December|12',
          r'purchased|purchase', r'registered|registration', r'irrespective|no.*(?:limit|cap)|without.*(?:limit|cap)|unlimited'], f'{tax}:p1'),
        ('retrofit', questions[1][0],
         [r'15\s*%', r'15,?000', r'5,?000', r'retro'], f'{policy}:p10'),
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
        for position, (name, question, patterns, expected_page) in enumerate(cases):
            if position:
                time.sleep(60)
            rendered = client.predict('Telangana', question, api_name='/answer_policy')
            result = outputs[-1]
            observations.append({'case': name, 'question': question, 'result': result, 'ui_outputs': rendered})
            save('running')
            assert result['status'] == 'document_answer', (name, result)
            assert all(re.search(p, result['answer'], re.I) for p in patterns), (name, result['answer'])
            assert any(expected_page in s['evidence_id'] for s in result['sources']), name
            assert all(s['state'] == 'Telangana' and '#page=' in s['official_url'] for s in result['sources'])
            assert '#page=' in rendered[0] and '#page=' in rendered[1]
            if name == 'private_car_tax':
                assert 'OCR' in rendered[1] or 'transcription' in rendered[1]
            checks.append('live_gradio_'+name)
            print('Live Telangana case passed:', name, flush=True)
        rendered = client.predict('Telangana', 'Compare Telangana and Tamil Nadu EV subsidies', api_name='/answer_policy')
        assert outputs[-1]['status'] == 'clarification_required'
        assert rendered[1] == '### Sources\n\nNo sources cited.'
        checks.append('gradio_rejection_clears_previous_citations')
        save('passed')
    except Exception:
        save('failed')
        raise
    finally:
        demo.close()
    print('Stage 10 Telangana live checks passed:', len(checks), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--case', choices=['private_car_tax', 'retrofit'])
    args = parser.parse_args()
    assert not args.case or args.live, '--case requires --live'
    run_checks(args.live, args.case)
