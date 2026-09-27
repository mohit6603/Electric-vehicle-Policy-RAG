"""Check Uttar Pradesh integration; --live exercises real answers through Gradio HTTP."""
import argparse
import copy
import hashlib
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
            raise AssertionError('Restart/retrieval must not embed the corpus.')

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
    assert stage['vector_store_chroma']._collection.count() == 348
    assert stage['index_spec']['chunks_by_state'] == {
        'Maharashtra': 53, 'Tamil Nadu': 78, 'Central': 100, 'Uttar Pradesh': 117}
    checks += ['reopen_348_records_without_embedding_or_rebuild', 'four_jurisdiction_counts']
    for selection in ('UP', 'uttar pradesh', 'Uttar Pradesh'):
        assert stage['route_policy_question'](selection, 'What purchase subsidy is described?')['jurisdiction'] == 'Uttar Pradesh'
    assert stage['mentioned_jurisdictions']('sign up for EV subsidy') == set()
    checks.append('up_alias_and_lowercase_word_distinguished')
    questions = [
        'What two-wheeler purchase subsidy and funding limit does the July 2024 amendment state?',
        'What does the amendment say about three-wheeler purchase subsidy?',
        'What road tax and registration fee exemptions do the November 2025 notifications specify?',
        'Which fleet ownership minimum and subsidy maximum are stated?',
        'What capital subsidy does the original policy specify for charging and swapping stations?',
    ]
    required = set(stage['retrieval_rules']['required_pages']['Uttar Pradesh'])
    for question in questions:
        result = stage['retrieve_policy']('Uttar Pradesh', question, k=1)
        assert result['status'] == 'retrieved', result
        docs = result['context_docs']
        assert {d.metadata['state'] for d in docs} == {'Uttar Pradesh'}
        assert required <= {d.metadata['page_id'] for d in docs}
        text = '\n'.join(d.page_content for d in docs)
        assert 'Rs 12000' not in text and 'manufactured, purchased & registered' not in text
        assert 'cancelled (निरस्त)' in text and '403.97 crore' in text
        assert 'at least 10' in text and 'at most ten' in text
        assert 'only pure electric vehicles' in text
        assert sum(len(d.page_content) for d in docs) < 50000
        observations.append({'question': question, 'page_ids': [d.metadata['page_id'] for d in docs],
                             'context_chars': len(text), 'status': result['status']})
    checks += ['five_filtered_semantic_queries', 'mandatory_amendments_and_conditions',
               'superseded_hidden_3w_and_manufacture_clause_absent', 'context_within_limit']
    # Exercise every UP page as a seed, including old clauses that may rank highly.
    for page_id in (p for p in stage['retrieval_page_by_id'] if p.startswith('uttar_pradesh_')):
        chunk = next(d for d in stage['index_documents'] if d.metadata['page_id'] == page_id)
        docs, omitted = stage['assemble_policy_context']([chunk], 'Uttar Pradesh')
        for span in omitted:
            for doc in docs:
                if doc.metadata['page_id'] == span['page_id']:
                    assert doc.metadata['excerpt_end'] <= span['start'] or doc.metadata['excerpt_start'] >= span['end']
    checks.append('all_39_up_pages_assemble_with_version_rules')
    before = copy.deepcopy(counts)
    for selection, question, status in [
        ('UP', 'Tamil Nadu purchase subsidy?', 'clarification_required'),
        ('UP', 'Compare UP and Maharashtra incentives', 'clarification_required'),
        ('Delhi', 'Electric car subsidy?', 'unsupported_jurisdiction'),
        ('UP', '', 'clarification_required'),
        ('UP', 'Can I claim an EV subsidy today?', 'not_established'),
    ]:
        result = stage['ask_policy'](selection, question)
        assert result['status'] == status and not result['sources'], result
        observations.append({'selection': selection, 'question': question, 'result': result})
    assert counts == before
    checks.append('five_rejections_skip_models_and_clear_sources')
    run_cell(stage, 'stage9-callback')
    run_cell(stage, 'stage9-startup')
    run_cell(stage, 'stage9-interface')
    assert stage['ui_choices'] == ['Central', 'Maharashtra', 'Tamil Nadu', 'Uttar Pradesh']
    checks.append('gradio_lists_four_loaded_jurisdictions')
    report_path = Path('data/processed/uttar_pradesh/stage10_live_checks.json' if live
                       else 'data/processed/uttar_pradesh/stage10_integration_checks.json')

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
        print('Stage 10 UP integration checks passed:', len(checks), flush=True)
        return
    cases = [
        ('purchase', 'According to the July 2024 amendment, what is the two-wheeler purchase-subsidy rate, per-vehicle cap, vehicle limit and scheme period or funding limit?',
         [r'15\s*%', r'5,?000', r'2\s*lakh|200,?000|2,00,000', r'403\.97', r'five years|5 years|2027'], 'uttar_pradesh_purchase_amendment_2024-07-15'),
        ('pure_ev_tax_fee', 'According to the November 2025 notifications, what road tax and registration fee exemptions cover pure EVs purchased and registered in UP during the fourth and fifth policy years? State the dates.',
         [r'100\s*%', r'pure', r'2025', r'2027', r'purchas', r'register'], 'uttar_pradesh_road_tax_2025-11-05'),
        ('cancelled_3w', 'What does the July 2024 amendment say about the three-wheeler purchase-subsidy provision?',
         [r'cancel|remov|repeal|withdraw|discontinu'], 'uttar_pradesh_purchase_amendment_2024-07-15'),
    ]
    if case:
        cases = [item for item in cases if item[0] == case]
    ask = stage['ask_policy']
    outputs = []

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
        for position, (name, question, patterns, expected_source) in enumerate(cases):
            if position:
                time.sleep(60)
            rendered = client.predict('Uttar Pradesh', question, api_name='/answer_policy')
            result = outputs[-1]
            observations.append({'case': name, 'question': question, 'result': result, 'ui_outputs': rendered})
            save('running')
            assert result['status'] == 'document_answer', (name, result)
            assert all(re.search(p, result['answer'], re.I) for p in patterns), (name, result['answer'])
            assert any(expected_source in s['evidence_id'] for s in result['sources']), name
            assert all(s['state'] == 'Uttar Pradesh' and '#page=' in s['official_url'] for s in result['sources'])
            if name == 'pure_ev_tax_fee':
                assert any('uttar_pradesh_registration_fee_' in s['evidence_id'] for s in result['sources'])
            if name == 'purchase':
                assert 'not an official translation' in rendered[1]
            assert '#page=' in rendered[0] and '#page=' in rendered[1]
            checks.append('live_gradio_'+name)
            print('Live UP case passed:', name, flush=True)
        rendered = client.predict('Uttar Pradesh', 'Compare UP and Tamil Nadu EV subsidies', api_name='/answer_policy')
        assert outputs[-1]['status'] == 'clarification_required'
        assert rendered[1] == '### Sources\n\nNo sources cited.'
        checks.append('gradio_rejection_clears_previous_citations')
        save('passed')
    except Exception:
        save('failed')
        raise
    finally:
        demo.close()
    print('Stage 10 UP live checks passed:', len(checks), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--case', choices=['purchase', 'pure_ev_tax_fee', 'cancelled_3w'])
    args = parser.parse_args()
    assert not args.case or args.live, '--case requires --live'
    run_checks(args.live, args.case)
