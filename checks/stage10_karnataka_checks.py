"""Check Karnataka ingestion/retrieval; --live adds two Gradio/Groq development cases."""
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


def check_live_answer(name, result, rendered):
    policy = 'karnataka_policy_2025-02-11'
    tax = 'karnataka_tax_amendment_2026-04-10'
    if name == 'fast_charging':
        patterns = [r'(?:25|twenty\W+five)\s*(?:%|percent)',
                    r'10,?00,?000|(?:10|ten)\s*lakh', r'500|five\s+hundred', r'slow', r'no|not']
        expected_page = f'{policy}:p22'
    else:
        patterns = [r'(?:5|five)\s*(?:%|percent)', r'(?:8|eight)\s*(?:%|percent)',
                    r'(?:10|ten)\s*(?:%|percent)', r'(?:10|ten)\s*lakh',
                    r'(?:25|twenty\W+five)\s*lakh', r'cost']
        expected_page = f'{tax}:p6'
    assert result['status'] == 'document_answer', (name, result)
    assert all(re.search(p, result['answer'], re.I) for p in patterns), (name, result['answer'])
    assert any(expected_page in s['evidence_id'] for s in result['sources']), name
    assert all(s['state'] == 'Karnataka' and '#page=' in s['official_url'] for s in result['sources'])
    cited = {s['evidence_id'].split(':x')[0] for s in result['sources']}
    claim_text = ' '.join(p['text'] for p in result['points'])
    if name == 'fast_charging':
        assert f'{policy}:p22' in cited and cited <= {f'{policy}:p22', f'{policy}:p26'}, cited
        assert not re.search(r'(?:project|station)\s+cost', claim_text, re.I), claim_text
    else:
        assert cited == {f'{tax}:p2', f'{tax}:p6'}, cited
        assert re.search(r'commenc|effective', claim_text, re.I), claim_text
        assert re.search(r'not\s+(?:yet\s+)?(?:verified|established|collected|confirmed)', claim_text, re.I), claim_text
    assert '#page=' in rendered[0] and '#page=' in rendered[1]


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
    assert stage['index_spec']['chunks_by_state']['Karnataka'] == 105
    checks += ['reopen_all_records_without_corpus_embedding', '105_karnataka_chunks']
    for selection in ('Karnataka', 'KA'):
        result = stage['route_policy_question'](selection, 'What purchase incentive is described?')
        assert result['jurisdiction'] == 'Karnataka', result
    checks.append('two_karnataka_aliases')
    policy = 'karnataka_policy_2025-02-11'
    tax = 'karnataka_tax_amendment_2026-04-10'
    fee = 'karnataka_registration_fee_2021-08-02'
    questions = [
        ('What fast-charging subsidy rate, per-station cap and station count does the 2025 policy state, and are slow chargers incentivized?', [f'{policy}:p22']),
        ('What lifetime-tax cost slabs and rates for newly registered electric private cars does Part A5(a) of the 2026 Act state?', [f'{tax}:p2', f'{tax}:p6', f'{tax}:p7']),
        ('What capital subsidy rates, land limit and payment installments are stated for large, mega and ultra-mega manufacturing enterprises?', [f'{policy}:p16', f'{policy}:p17']),
        ('What capital subsidy rates and caps does the policy give for general and special category micro industries?', [f'{policy}:p13']),
        ('Which policy zone covers Anekal in Bengaluru Urban?', [f'{policy}:p30']),
        ('What registration certificate fees does GSR 525(E) exempt for battery-operated vehicles?', [f'{fee}:p3']),
    ]
    required = set(stage['retrieval_rules']['required_pages']['Karnataka'])
    for question, expected in questions:
        result = stage['retrieve_policy']('Karnataka', question, k=1)
        assert result['status'] == 'retrieved', result
        docs = result['context_docs']
        assert {d.metadata['state'] for d in docs} == {'Karnataka'}
        assert required.union(expected) <= {d.metadata['page_id'] for d in docs}, question
        assert all(d.metadata['policy_year'] in (2021, 2025, 2026) for d in docs)
        size = sum(len(d.page_content) for d in docs)
        assert size < 50000
        observations.append({'question': question, 'page_ids': [d.metadata['page_id'] for d in docs],
                             'context_chars': size, 'status': result['status']})
    checks += ['six_filtered_semantic_queries', 'conditions_and_continuations_present', 'only_three_registered_karnataka_sources']
    sizes = []
    for page_id in (p for p in stage['retrieval_page_by_id'] if p.startswith('karnataka_')):
        chunk = next(d for d in stage['index_documents'] if d.metadata['page_id'] == page_id)
        docs, omitted = stage['assemble_policy_context']([chunk], 'Karnataka')
        assert all(item['page_id'] in stage['retrieval_rules']['page_rules'] for item in omitted)
        size = sum(len(d.page_content) for d in docs)
        assert size < 50000, (page_id, size)
        sizes.append(size)
    assert len(sizes) == 41
    observations.append({'all_page_context_range': [min(sizes), max(sizes)]})
    checks.append('all_41_pages_assemble_within_context_limit')
    chunk = next(d for d in stage['index_documents'] if d.metadata['page_id'] == f'{policy}:p12')
    docs, omitted = stage['assemble_policy_context']([chunk], 'Karnataka')
    text = '\n'.join(d.page_content for d in docs if d.metadata['page_id'] == f'{policy}:p12')
    assert 'exempts from payment of taxes on all categories' not in text
    assert 'minimum 50%' in text and 'retrofitting' in text
    assert {f'{tax}:p6', f'{tax}:p9', f'{fee}:p3'} <= {d.metadata['page_id'] for d in docs}
    tax_text = '\n'.join(d.page_content for d in docs if d.metadata['source_id'] == tax)
    assert 'Construction Equipment' not in tax_text and 'Drilling Rigs' not in tax_text
    assert 'PART A5(a)' in tax_text and 'PART A8(a)' in tax_text and 'PART C4(a)' in tax_text
    checks.append('old_tax_and_unrelated_schedules_excluded_ev_updates_and_fee_retained')
    run_cell(stage, 'shared-loader')
    manifest = json.loads(Path('data/source_manifest.json').read_text())
    review = json.loads(Path('data/ocr/karnataka/review.json').read_text())
    pages = stage['load_policy_pages'](manifest, review, 'Karnataka')
    assert sum(d.metadata['text_status'] == 'ai_proposal' for d in pages) == 9
    assert all(not d.metadata['team_verified'] and not d.metadata['accepted_for_ingestion'] for d in pages)
    broken = copy.deepcopy(review)
    broken['pages'].pop()
    try:
        stage['load_policy_pages'](manifest, broken, 'Karnataka')
    except ValueError as error:
        assert 'coverage mismatch' in str(error)
    else:
        raise AssertionError('Missing table proposal accepted.')
    broken_manifest = copy.deepcopy(manifest)
    source = next(s for s in broken_manifest['sources'] if s['source_id'] == policy)
    source['ocr_pdf_pages'].append(99)
    try:
        stage['load_policy_pages'](broken_manifest, review, 'Karnataka')
    except ValueError as error:
        assert 'outside candidate pages' in str(error)
    else:
        raise AssertionError('Out-of-range proposal page accepted.')
    checks.append('mixed_plain_and_table_pages_preserve_flags_and_reject_bad_coverage')
    before = copy.deepcopy(counts)
    for selection, question, status in [
        ('KA', 'Tamil Nadu purchase subsidy?', 'clarification_required'),
        ('Karnataka', 'Compare Karnataka and Maharashtra incentives', 'clarification_required'),
        ('Madhya Pradesh', 'Electric car subsidy?', 'unsupported_jurisdiction'),
        ('Karnataka', '', 'clarification_required'),
        ('Karnataka', 'Can I claim an EV subsidy today?', 'not_established'),
    ]:
        result = stage['ask_policy'](selection, question)
        assert result['status'] == status and not result['sources'], result
        observations.append({'selection': selection, 'question': question, 'result': result})
    assert counts == before
    checks.append('five_rejections_skip_models_and_clear_sources')
    for cell in ('stage9-callback', 'stage9-startup', 'stage9-interface'):
        run_cell(stage, cell)
    assert stage['ui_choices'] == sorted(stage['index_spec']['chunks_by_state'])
    assert 'Karnataka' in stage['ui_choices']
    checks.append('gradio_lists_karnataka_and_other_loaded_jurisdictions')
    report_path = Path('data/processed/karnataka/stage10_live_checks.json' if live
                       else 'data/processed/karnataka/stage10_integration_checks.json')
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
        print('Stage 10 Karnataka integration checks passed:', len(checks), flush=True)
        return
    cases = [('fast_charging', questions[0][0]), ('car_tax', questions[1][0])]
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
        for position, (name, question) in enumerate(cases):
            if position:
                time.sleep(60)
            rendered = client.predict('Karnataka', question, api_name='/answer_policy')
            result = outputs[-1]
            observations.append({'case': name, 'question': question, 'result': result, 'ui_outputs': rendered})
            save('running')
            check_live_answer(name, result, rendered)
            checks.append('live_gradio_'+name)
            print('Live Karnataka case passed:', name, flush=True)
        rendered = client.predict('Karnataka', 'Compare Karnataka and Tamil Nadu EV subsidies', api_name='/answer_policy')
        assert outputs[-1]['status'] == 'clarification_required'
        assert rendered[1] == '### Sources\n\nNo sources cited.'
        checks.append('gradio_rejection_clears_previous_citations')
        save('passed')
    except Exception:
        save('failed')
        raise
    finally:
        demo.close()
    print('Stage 10 Karnataka live checks passed:', len(checks), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--case', choices=['fast_charging', 'car_tax'])
    args = parser.parse_args()
    assert not args.case or args.live, '--case requires --live'
    run_checks(args.live, args.case)
