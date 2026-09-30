"""Check Madhya Pradesh ingestion/retrieval; --live adds two Gradio/Groq development cases."""
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
    assert stage['index_spec']['chunks_by_state']['Madhya Pradesh'] == 156
    checks += ['reopen_all_records_without_corpus_embedding', '156_madhya_pradesh_chunks']
    for selection in ('Madhya Pradesh', 'madhya pradesh', 'MP'):
        result = stage['route_policy_question'](selection, 'What purchase incentive is described?')
        assert result['jurisdiction'] == 'Madhya Pradesh', result
    checks.append('three_madhya_pradesh_aliases')
    policy = 'madhya_pradesh_policy_2025'
    guide = 'madhya_pradesh_guidelines_2025-09-15'
    questions = [
        ('What small public charging station subsidy rate, cost basis, cap and station count do the supplied documents state?', [f'{guide}:p16', f'{guide}:p65']),
        ('What NOC deadline, safety exceptions and written-rejection requirement does section 14 state for resident charging from an RWA common load connection?', [f'{guide}:p19', f'{guide}:p20', f'{guide}:p72']),
        ('What incentive does the policy state for retrofitting a car, and what conditions apply?', [f'{policy}:p25', f'{guide}:p10', f'{guide}:p11']),
        ('What first-year e-car tax exemption and ex-factory price ceiling does the policy describe?', [f'{policy}:p20', f'{guide}:p8', f'{guide}:p9']),
        ('What monthly uptime and incentive-recovery steps apply to public charging stations?', [f'{guide}:p17', f'{guide}:p66', f'{guide}:p67']),
    ]
    required = set(stage['retrieval_rules']['required_pages']['Madhya Pradesh'])
    for question, expected in questions:
        result = stage['retrieve_policy']('Madhya Pradesh', question, k=1)
        assert result['status'] == 'retrieved', result
        docs = result['context_docs']
        assert {d.metadata['state'] for d in docs} == {'Madhya Pradesh'}
        assert required.union(expected) <= {d.metadata['page_id'] for d in docs}, (question, [d.metadata['page_id'] for d in docs])
        assert all(d.metadata['policy_year'] == 2025 for d in docs)
        size = sum(len(d.page_content) for d in docs)
        assert size < 50000
        observations.append({'question': question, 'page_ids': [d.metadata['page_id'] for d in docs],
                             'context_chars': size, 'status': result['status']})
    checks += ['five_filtered_semantic_queries', 'conditions_and_continuations_present', 'two_registered_mp_sources']
    sizes = []
    for page_id in (p for p in stage['retrieval_page_by_id'] if p.startswith('madhya_pradesh_')):
        chunk = next(d for d in stage['index_documents'] if d.metadata['page_id'] == page_id)
        docs, omitted = stage['assemble_policy_context']([chunk], 'Madhya Pradesh')
        assert not omitted
        size = sum(len(d.page_content) for d in docs)
        assert size < 50000, (page_id, size)
        sizes.append(size)
    assert len(sizes) == 60
    observations.append({'all_page_context_range': [min(sizes), max(sizes)]})
    checks.append('all_60_pages_assemble_within_context_limit')
    assert stage['retrieval_page_by_id'][f'{guide}:p16'].metadata['text_status'] == 'ai_proposal'
    assert all(not d.metadata['accepted_for_ingestion'] or d.metadata['team_verified'] for d in stage['index_documents'])
    checks.append('ocr_proposals_and_pending_review_preserved')
    before = copy.deepcopy(counts)
    for selection, question, status in [
        ('MP', 'Tamil Nadu purchase subsidy?', 'clarification_required'),
        ('Madhya Pradesh', 'Compare Madhya Pradesh and Maharashtra incentives', 'clarification_required'),
        ('Kerala', 'Electric car subsidy?', 'unsupported_jurisdiction'),
        ('Madhya Pradesh', '', 'clarification_required'),
        ('Madhya Pradesh', 'Can I claim an EV subsidy today?', 'not_established'),
    ]:
        result = stage['ask_policy'](selection, question)
        assert result['status'] == status and not result['sources'], result
        observations.append({'selection': selection, 'question': question, 'result': result})
    assert counts == before
    checks.append('five_rejections_skip_models_and_clear_sources')
    for cell in ('stage9-callback', 'stage9-startup', 'stage9-interface'):
        run_cell(stage, cell)
    assert stage['ui_choices'] == sorted(stage['index_spec']['chunks_by_state'])
    assert 'Madhya Pradesh' in stage['ui_choices']
    checks.append('gradio_lists_madhya_pradesh_and_other_loaded_jurisdictions')
    report_path = Path('data/processed/madhya_pradesh/stage10_live_checks.json' if live
                       else 'data/processed/madhya_pradesh/stage10_integration_checks.json')
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
        print('Stage 10 Madhya Pradesh integration checks passed:', len(checks), flush=True)
        return
    cases = [
        ('small_charging', questions[0][0],
         [r'30\s*%|thirty\s+percent', r'500|five hundred', r'1,?50,?000|150,?000|1\.5\s*lakh',
          r'equipment|machinery'], f'{guide}:p16'),
        ('rwa_noc', questions[1][0],
         [r'(?:7|seven)\s+working\s+days', r'safety', r'written'], f'{guide}:p20'),
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
            rendered = client.predict('Madhya Pradesh', question, api_name='/answer_policy')
            result = outputs[-1]
            observations.append({'case': name, 'question': question, 'result': result, 'ui_outputs': rendered})
            save('running')
            assert result['status'] == 'document_answer', (name, result)
            assert all(re.search(p, result['answer'], re.I) for p in patterns), (name, result['answer'])
            assert any(expected_page in s['evidence_id'] for s in result['sources']), name
            assert all(s['state'] == 'Madhya Pradesh' and '#page=' in s['official_url'] for s in result['sources'])
            assert '#page=' in rendered[0] and '#page=' in rendered[1]
            if name == 'small_charging':
                assert 'OCR' in rendered[1] or 'transcription' in rendered[1]
            checks.append('live_gradio_'+name)
            print('Live Madhya Pradesh case passed:', name, flush=True)
        rendered = client.predict('Madhya Pradesh', 'Compare Madhya Pradesh and Tamil Nadu EV subsidies', api_name='/answer_policy')
        assert outputs[-1]['status'] == 'clarification_required'
        assert rendered[1] == '### Sources\n\nNo sources cited.'
        checks.append('gradio_rejection_clears_previous_citations')
        save('passed')
    except Exception:
        save('failed')
        raise
    finally:
        demo.close()
    print('Stage 10 Madhya Pradesh live checks passed:', len(checks), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--case', choices=['small_charging', 'rwa_noc'])
    args = parser.parse_args()
    assert not args.case or args.live, '--case requires --live'
    run_checks(args.live, args.case)
