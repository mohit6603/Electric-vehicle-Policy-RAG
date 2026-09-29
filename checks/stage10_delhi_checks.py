"""Check Delhi ingestion/retrieval; --live adds two Gradio/Groq development cases."""
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
    assert stage['index_spec']['chunks_by_state']['Delhi'] == 132
    checks += ['reopen_all_records_without_corpus_embedding', '132_delhi_chunks']
    for selection in ('Delhi', 'New Delhi', 'Delhi (NCT)', 'NCT of Delhi', 'DL'):
        result = stage['route_policy_question'](selection, 'What purchase incentive is described?')
        assert result['jurisdiction'] == 'Delhi', result
    checks.append('five_delhi_aliases')
    policy = 'delhi_policy_2026-06-30'
    guide = 'delhi_operating_guidelines_2026-07-02'
    questions = [
        ('What yearly two-wheeler purchase incentive rates, caps and price ceiling does the 2026 policy state?',
         [f'{policy}:p13', f'{policy}:p14', f'{guide}:p7', f'{guide}:p8']),
        ('What car scrapping incentive, applicant limit and price ceiling does the policy state?',
         [f'{policy}:p14', f'{guide}:p9']),
        ('What road tax and registration fee exemptions apply below and above the electric car price ceiling?',
         [f'{policy}:p14']),
        ('What no-entry exemption, vehicle limit and time windows are specified for private N2 electric trucks?',
         [f'{policy}:p15', f'{guide}:p10', f'{guide}:p11']),
        ('What is the purchase incentive application deadline from RC generation and conditional payment timeline?',
         [f'{policy}:p13', f'{guide}:p7', f'{guide}:p8']),
    ]
    required = set(stage['retrieval_rules']['required_pages']['Delhi'])
    for question, expected in questions:
        result = stage['retrieve_policy']('Delhi', question, k=1)
        assert result['status'] == 'retrieved', result
        docs = result['context_docs']
        assert {d.metadata['state'] for d in docs} == {'Delhi'}
        assert required.union(expected) <= {d.metadata['page_id'] for d in docs}, question
        assert all(d.metadata['policy_year'] == 2026 for d in docs)
        size = sum(len(d.page_content) for d in docs)
        assert size < 50000
        observations.append({'question': question, 'page_ids': [d.metadata['page_id'] for d in docs],
                             'context_chars': size, 'status': result['status']})
    checks += ['five_filtered_semantic_queries', 'conditions_and_continuations_present', 'no_draft_or_2020_sources']
    sizes = []
    for page_id in (p for p in stage['retrieval_page_by_id'] if p.startswith('delhi_')):
        chunk = next(d for d in stage['index_documents'] if d.metadata['page_id'] == page_id)
        docs, omitted = stage['assemble_policy_context']([chunk], 'Delhi')
        assert not omitted
        size = sum(len(d.page_content) for d in docs)
        assert size < 50000, (page_id, size)
        sizes.append(size)
    assert len(sizes) == 51
    observations.append({'all_page_context_range': [min(sizes), max(sizes)]})
    checks.append('all_51_pages_assemble_within_context_limit')
    before = copy.deepcopy(counts)
    for selection, question, status in [
        ('DL', 'Tamil Nadu purchase subsidy?', 'clarification_required'),
        ('Delhi', 'Compare Delhi and Maharashtra incentives', 'clarification_required'),
        ('Kerala', 'Electric car subsidy?', 'unsupported_jurisdiction'),
        ('Delhi', '', 'clarification_required'),
        ('Delhi', 'Can I claim an EV subsidy today?', 'not_established'),
    ]:
        result = stage['ask_policy'](selection, question)
        assert result['status'] == status and not result['sources'], result
        observations.append({'selection': selection, 'question': question, 'result': result})
    assert counts == before
    checks.append('five_rejections_skip_models_and_clear_sources')
    for cell in ('stage9-callback', 'stage9-startup', 'stage9-interface'):
        run_cell(stage, cell)
    assert stage['ui_choices'] == sorted(stage['index_spec']['chunks_by_state'])
    assert 'Delhi' in stage['ui_choices']
    checks.append('gradio_lists_delhi_and_other_loaded_jurisdictions')
    report_path = Path('data/processed/delhi/stage10_live_checks.json' if live
                       else 'data/processed/delhi/stage10_integration_checks.json')
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
        print('Stage 10 Delhi integration checks passed:', len(checks), flush=True)
        return
    cases = [
        ('two_wheeler', questions[0][0],
         [r'10,?000', r'30,?000', r'6,?600', r'20,?000', r'3,?300', r'2\.25', r'kWh'], f'{policy}:p13'),
        ('car_scrapping', 'According to the 2026 policy, what is the non-transport electric car scrapping incentive, applicant limit, price ceiling, old-car requirement, new-purchase deadline and who may receive it?',
         [r'1,?00,?000|100,?000|one lakh|1 lakh', r'30\s*lakh', r'BS.?IV', r'six|6', r'owner', r'first'], f'{policy}:p14'),
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
            rendered = client.predict('Delhi', question, api_name='/answer_policy')
            result = outputs[-1]
            observations.append({'case': name, 'question': question, 'result': result, 'ui_outputs': rendered})
            save('running')
            assert result['status'] == 'document_answer', (name, result)
            assert all(re.search(p, result['answer'], re.I) for p in patterns), (name, result['answer'])
            assert any(expected_page in s['evidence_id'] for s in result['sources']), name
            assert all(s['state'] == 'Delhi' and '#page=' in s['official_url'] for s in result['sources'])
            assert '#page=' in rendered[0] and '#page=' in rendered[1]
            checks.append('live_gradio_'+name)
            print('Live Delhi case passed:', name, flush=True)
        rendered = client.predict('Delhi', 'Compare Delhi and Tamil Nadu EV subsidies', api_name='/answer_policy')
        assert outputs[-1]['status'] == 'clarification_required'
        assert rendered[1] == '### Sources\n\nNo sources cited.'
        checks.append('gradio_rejection_clears_previous_citations')
        save('passed')
    except Exception:
        save('failed')
        raise
    finally:
        demo.close()
    print('Stage 10 Delhi live checks passed:', len(checks), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--case', choices=['two_wheeler', 'car_scrapping'])
    args = parser.parse_args()
    assert not args.case or args.live, '--case requires --live'
    run_checks(args.live, args.case)
