"""Run citation checks; add --live for six Groq pilot calls (uses API allowance)."""
import argparse
import copy
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda
from stage6_retrieval_checks import load_stage6, expect_error


def load_stage7():
    stage = load_stage6()
    notebook = json.loads(Path('EV Policy Assistant.ipynb').read_text())
    for cell in notebook['cells']:
        if cell['id'] in ('stage7-schema', 'stage7-prompt', 'stage7-citations', 'stage7-answer'):
            exec(compile(''.join(cell['source']), cell['id'], 'exec'), stage)
    return stage


def save_report(stage, filename, **results):
    report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
        'notebook_sha256': stage['index_file_hash']('EV Policy Assistant.ipynb'),
        'check_script_sha256': stage['index_file_hash'](__file__),
        'corpus_sha256': stage['index_spec']['corpus_sha256'],
        'retrieval_k': stage['answer_retrieval_k'],
        'retrieval_rules_sha256': stage['index_file_hash'](stage['retrieval_rules_path']),
        'scope': 'AI-authored technical checks; not formal team evaluation', **results}
    folder = Path('data/processed/answers')
    folder.mkdir(parents=True, exist_ok=True)
    (folder / filename).write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')


def run_checks(stage):
    seed = next(doc for doc in stage['index_documents']
                if doc.metadata['page_id'] == 'central_pm_edrive_extension_2026-08-10:p3')
    docs, omitted = stage['assemble_policy_context']([seed], 'Central')
    retrieval = {'status': 'retrieved', 'message': '', 'jurisdiction': 'Central',
        'context_docs': docs, 'omitted_spans': omitted,
        'verification_cutoff': stage['retrieval_cutoff'], 'version_note': 'Technical fixture.'}
    _, sources = stage['label_answer_evidence'](retrieval)
    source_id = next(id for id, doc in sources.items()
                     if doc.metadata['page_id'] == seed.metadata['page_id'])
    point = {'text': 'The document states ₹2,500/kWh, capped at ₹5,000 per vehicle.',
             'citations': [source_id]}
    valid = {'status': 'supported', 'points': [point]}
    passed = []
    original_retrieve, original_llm = stage['retrieve_policy'], stage['get_answer_llm']
    stage['retrieve_policy'] = lambda selection, question, **kwargs: retrieval
    model_calls = []

    def answer(payload, finish='stop'):
        content = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False)

        def respond(prompt):
            model_calls.append(prompt)
            return AIMessage(content=content, response_metadata={'finish_reason': finish})

        stage['get_answer_llm'] = lambda: RunnableLambda(respond)
        return stage['answer_question']('Central', 'What rate and cap does the document state?')

    try:
        result = answer(valid)
        assert result['status'] == 'document_answer', result
        assert len(result['sources']) == 1 < len(sources)
        source = result['sources'][0]
        assert source['source_id'] == source_id and source['pdf_page'] == 3
        assert source['official_url'] == sources[source_id].metadata['official_url'] + '#page=3'
        assert source['source'] == sources[source_id].metadata['source']
        assert Path(source['source']).is_file()
        assert 'Central' in result['answer'] and 'PDF page 3' in result['answer']
        assert stage['retrieval_cutoff'] in result['answer'] and 'not verified' in result['answer']
        assert result['current_entitlement_answers_allowed'] is False
        assert result['points'][0]['citations'][0]['source_excerpt'] == sources[source_id].page_content
        prompt_text = model_calls[-1].to_messages()[-1].content
        for id, doc in sources.items():
            assert f'[{id}]' in prompt_text
            assert stage['format_answer_excerpt'](doc.page_content) in prompt_text
            assert stage['citation_text'](doc.page_content) in stage['citation_text'](prompt_text)
        passed += ['cited_sources_only_with_original_pdf_page_links',
                   'jurisdiction_cutoff_review_status_and_original_excerpts_retained',
                   'all_assembled_evidence_retained_in_prompt_after_whitespace_compaction']

        duplicate = copy.deepcopy(valid)
        duplicate['points'][0]['citations'].append(source_id)
        assert len(answer(duplicate)['points'][0]['citations']) == 1
        passed.append('duplicate_citation_ids_collapsed')

        invalid = []
        for citations in (['S999'], ['S1', 'S999'],
                          [{'source_id': source_id, 'quote': 'Invented evidence'}]):
            payload = copy.deepcopy(valid)
            payload['points'][0]['citations'] = citations
            invalid.append(payload)
        invalid += [
            {'status': 'supported', 'points': [{'text': 'No citation', 'citations': []}]},
            {'status': 'supported', 'points': []},
            {'status': 'not_established', 'points': [point]},
            {'status': 'supported', 'points': [dict(point, text='Claim [S999]')]},
            {'status': 'supported', 'points': [dict(point, text='Visit https://example.com')]},
            {'status': 'supported', 'points': [dict(point, text='<a href="x">Claim</a>')]},
            {'status': 'supported', 'points': [dict(point, text='  ')]},
            {'status': 'supported', 'points': [dict(point, invented_field='not allowed')]},
            'not valid JSON',
        ]
        for payload in invalid:
            rejected = answer(payload)
            assert rejected['status'] == 'citation_error', (payload, rejected)
            assert rejected['points'] == [] and rejected['sources'] == []
            assert 'No policy answer is shown' in rejected['answer']
        passed += ['unknown_ids_and_model_supplied_evidence_rejected',
                   'missing_citations_empty_support_and_claiming_abstention_rejected',
                   'model_links_markup_and_malformed_output_withheld']
        assert answer(valid, finish='length')['status'] == 'citation_error'
        passed.append('truncated_response_withheld_even_with_parseable_json')

        abstained = answer({'status': 'not_established', 'points': []})
        assert abstained['status'] == 'not_established'
        assert not abstained['sources'] and not abstained['points']
        assert 'not verified' in abstained['answer']
        passed.append('structured_abstention_has_no_policy_claims_or_sources')

        count = len(model_calls)
        original_status, original_docs = retrieval['status'], retrieval['context_docs']
        retrieval['context_docs'] = []
        assert answer(valid)['status'] == 'not_established'
        retrieval['status'] = 'clarification_required'
        assert answer(valid)['status'] == 'clarification_required'
        assert len(model_calls) == count
        retrieval['status'], retrieval['context_docs'] = original_status, original_docs
        passed.append('empty_evidence_and_retrieval_rejections_skip_generation')

        for field, value, message in (
            ('state', 'Tamil Nadu', 'Unexpected jurisdiction'),
            ('current_entitlement_answers_allowed', True, 'review status'),
            ('official_url', 'https://example.com/invented.pdf', 'metadata differs'),
            ('pdf_page', 999, 'metadata differs'),
            ('excerpt_sha256', '0' * 64, 'hash mismatch'),
        ):
            changed = copy.deepcopy(retrieval)
            changed['context_docs'][0].metadata[field] = value
            expect_error(lambda: stage['label_answer_evidence'](changed), message)
        changed = copy.deepcopy(retrieval)
        changed['context_docs'][0].page_content += ' fabricated'
        expect_error(lambda: stage['label_answer_evidence'](changed), 'excerpt differs')
        passed += ['changed_jurisdiction_review_status_or_source_metadata_rejected',
                   'changed_evidence_text_or_hash_rejected']
        tn_seed = next(doc for doc in stage['index_documents']
                       if doc.metadata['page_id'] == 'tamil_nadu_policy_2023:p17')
        tn_docs, _ = stage['assemble_policy_context']([tn_seed], 'Tamil Nadu')
        retrieval.update(jurisdiction='Tamil Nadu', context_docs=tn_docs)
        _, tn_sources = stage['label_answer_evidence'](retrieval)
        tn_id = next(id for id, doc in tn_sources.items() if doc.metadata['page_id'] == tn_seed.metadata['page_id'])
        payload = {'status': 'supported', 'points': [
            {'text': 'E-cycles must be registered and FAME II compliant.', 'citations': [tn_id]}]}
        stage['get_answer_llm'] = lambda: RunnableLambda(lambda prompt: AIMessage(content=json.dumps(payload)))
        withheld = stage['answer_question']('Tamil Nadu', 'What are the e-cycle eligibility conditions?')
        assert withheld['status'] == 'not_established' and withheld['reason'] == 'cycle_eligibility_review_pending'
        assert withheld['points'] == [] and withheld['sources'] == []
        passed.append('known_cycle_eligibility_overstatement_withheld_for_review')
    finally:
        stage['retrieve_policy'], stage['get_answer_llm'] = original_retrieve, original_llm
    save_report(stage, 'stage7_citation_checks.json', technical_status='passed',
                checks_passed=passed, invalid_response_cases=len(invalid) + 1, groq_calls=0)
    print('Stage 7 citation checks passed:', len(passed), flush=True)


live_cases = [
    {'id': 'mh_two_wheeler', 'selection': 'Maharashtra',
     'question': 'According to the Maharashtra policy, what percentage and per-vehicle cap apply to L1/L2 electric two-wheelers? Distinguish the vehicle-count ceiling from money and include the sale/registration condition.',
     'patterns': [r'10\s*%', r'10,?000', r'1,00,000|100,000|100000|one lakh', r'ex.factory', r'sold|sale', r'register'],
     'page_ids': ['maharashtra_policy_2025-05-23:p18', 'maharashtra_policy_2025-05-23:p19']},
    {'id': 'tn_cycle_historical', 'selection': 'Tamil Nadu',
     'question': 'What did the 2023 policy print for private e-cycle purchase incentives, including percentage, cap, vehicle count and restrictions? Distinguish those historical demand provisions from the later tax extension.',
     'patterns': [], 'page_ids': [], 'expected_status': 'not_established',
     'expected_reason': 'cycle_eligibility_review_pending'},
    {'id': 'tn_motor_tax', 'selection': 'Tamil Nadu',
     'question': 'Under the 29 December 2025 notification, which vehicles receive motor vehicle tax exemption and for what exact period? Does that notification itself extend purchase subsidies or registration fees?',
     'patterns': [r'transport', r'non.transport', r'2026', r'2027', r'January|01\.01|1\.1', r'December|31\.12', r'not|only|no '],
     'page_ids': ['tamil_nadu_motor_vehicle_tax_2025-12-29:p1']},
    {'id': 'central_two_wheeler', 'selection': 'Central',
     'question': 'According to the latest supplied amendment, what is the e-2W incentive rate and cap for 01.04.2025 to 31.03.2028? Include the price ceiling and percentage limit.',
     'patterns': [r'2,?500', r'kwh', r'5,?000', r'1\.5\s*lakh|150,?000|1,50,000', r'15\s*%', r'2025', r'2028'],
     'page_ids': ['central_pm_edrive_extension_2026-08-10:p3']},
    {'id': 'central_l5_deadlines', 'selection': 'Central',
     'question': 'Are L5 three-wheelers registered after 26 December 2025 covered? Distinguish that category closure from the latest overall terminal date, final claim deadline and fund limit.',
     'patterns': [r'26', r'2025', r'not eligible|ineligible|no .*incentive|not .*eligible', r'2027', r'2028', r'fund|outlay'],
     'page_ids': ['central_pm_edrive_l5_closure_2025-12-23:p1', 'central_pm_edrive_extension_2026-08-10:p3']},
    {'id': 'irrelevant', 'selection': 'Central',
     'question': 'What is a recipe for chocolate cake?', 'patterns': [], 'page_ids': [],
     'expected_status': 'not_established'},
]


def check_live_result(case, result):
    claim_text = ' '.join(point['text'] for point in result['points'])
    cited_pages = {source['evidence_id'].split(':x')[0] for source in result['sources']}
    checks = {
        'expected_status': result['status'] == case.get('expected_status', 'document_answer'),
        'expected_fact_patterns': all(re.search(pattern, claim_text, re.I) for pattern in case['patterns']),
        'expected_source_pages': set(case['page_ids']) <= cited_pages,
        'jurisdiction_isolated': all(source['state'] == case['selection'] for source in result['sources']),
        'no_current_entitlement_permission': result['current_entitlement_answers_allowed'] is False,
    }
    if 'expected_reason' in case:
        checks['known_eligibility_ambiguity_withheld'] = result.get('reason') == case['expected_reason'] and not result['points'] and not result['sources']
    if case['id'] == 'mh_two_wheeler':
        texts = [point['text'] for point in result['points']]
        checks['rupee_cap_is_10000_not_vehicle_count'] = any(
            re.search(r'(?:₹|Rs\.?|INR)\s*10,?000\b|10,?000\s*(?:rupees|INR)', text, re.I)
            and re.search(r'cap|maximum|per.vehicle', text, re.I) for text in texts)
        checks['100000_belongs_to_vehicle_count'] = any(
            re.search(r'1,00,000|100,000|100000|one lakh', text, re.I)
            and re.search(r'(?:vehicle|two.wheeler).*(?:ceiling|count|limit|cap)|(?:ceiling|count|limit|cap).*(?:vehicle|two.wheeler)', text, re.I)
            and not re.search(r'(?:₹|Rs\.?|INR)\s*(?:1,00,000|100,000|100000)', text, re.I)
            for text in texts)
    return checks


def run_live(stage):
    observed = []
    for number, case in enumerate(live_cases):
        if number:
            print('Waiting 55 seconds before the next Groq pilot call.', flush=True)
            time.sleep(55)
        print('Live case:', case['id'], flush=True)
        result = stage['answer_question'](case['selection'], case['question'])
        attempts = [result]
        if result.get('http_status') == 429:
            print('Groq rate limit: waiting 55 seconds for one retry.', flush=True)
            time.sleep(55)
            result = stage['answer_question'](case['selection'], case['question'])
            attempts.append(result)
        checks = check_live_result(case, result)
        observed.append({'case': case, 'checks': checks, 'result': result,
                         'earlier_attempts': attempts[:-1]})
        all_passed = all(all(row['checks'].values()) for row in observed)
        save_report(stage, 'stage7_live_checks.json',
            technical_status=('passed' if all_passed else 'failed') if len(observed) == len(live_cases) else 'in_progress',
            completed_cases=len(observed), planned_cases=len(live_cases),
            model=stage['answer_model_name'], model_settings=stage['answer_model_settings'], observations=observed,
            note='Fact patterns and source pages are smoke checks; inspect claims against attached excerpts separately. Team review is pending.')
        print(result['status'], checks, flush=True)
        print(result['answer'], flush=True)
    assert all_passed, 'Inspect stage7_live_checks.json for failed cases.'
    print('Stage 7 live cases passed:', len(observed), flush=True)


def check_saved_live(stage):
    path = Path('data/processed/answers/stage7_live_checks.json')
    report = json.loads(path.read_text())
    assert report['completed_cases'] == len(live_cases), 'The saved batch is incomplete.'
    assert report['notebook_sha256'] == stage['index_file_hash']('EV Policy Assistant.ipynb')
    assert report['corpus_sha256'] == stage['index_spec']['corpus_sha256']
    assert report['retrieval_rules_sha256'] == stage['index_file_hash'](stage['retrieval_rules_path'])
    assert report['model_settings'] == stage['answer_model_settings']
    assert [row['case'] for row in report['observations']] == live_cases
    previous_checks = [row['checks'] for row in report['observations']]
    for row in report['observations']:
        row['checks'] = check_live_result(row['case'], row['result'])
    report['technical_status'] = 'passed' if all(all(row['checks'].values()) for row in report['observations']) else 'failed'
    report['saved_output_recheck'] = {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
        'check_script_sha256': stage['index_file_hash'](__file__), 'groq_calls': 0,
        'previous_checks': previous_checks}
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    assert report['technical_status'] == 'passed', 'Saved answers still fail a check.'
    print('Saved Stage 7 live cases passed:', len(report['observations']), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true', help='Also send six pilot questions to Groq.')
    parser.add_argument('--check-saved', action='store_true', help='Recheck a complete saved batch; no Groq calls.')
    args = parser.parse_args()
    assert not (args.live and args.check_saved), 'Choose live or saved checks, not both.'
    stage = load_stage7()
    run_checks(stage)
    if args.live:
        run_live(stage)
    elif args.check_saved:
        check_saved_live(stage)
