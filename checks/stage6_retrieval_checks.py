"""Run from the project root: uv run --locked python checks/stage6_retrieval_checks.py."""
import copy
import json
from pathlib import Path
from datetime import datetime, timezone
import tempfile
from langchain_core.embeddings import Embeddings


def load_stage6():
    notebook = json.loads(Path('EV Policy Assistant.ipynb').read_text())
    namespace = {}
    cells = ('stage5-imports', 'stage5-index-functions', 'stage5-inputs', 'stage5-open',
             'stage6-inputs', 'stage6-load', 'stage6-routing', 'stage6-context')
    for cell in notebook['cells']:
        if cell['id'] in cells:
            exec(compile(''.join(cell['source']), cell['id'], 'exec'), namespace)
    return namespace


class QueryOnlyEmbeddings(Embeddings):
    def __init__(self, model):
        self.model = model
        self.query_count = 0

    def embed_documents(self, texts):
        raise AssertionError('Stage 6 must not embed corpus documents.')

    def embed_query(self, text):
        self.query_count += 1
        return self.model.embed_query(text)


class NoSearch:
    def as_retriever(self, **kwargs):
        raise AssertionError('Rejected input reached vector search.')


def expect_error(action, message):
    try:
        action()
    except ValueError as error:
        assert message in str(error), str(error)
    else:
        raise AssertionError(f'Expected error containing: {message}')


def run_checks():
    stage = load_stage6()
    retrieve = stage['retrieve_policy']
    route = stage['route_policy_question']
    assemble = stage['assemble_policy_context']
    validate = stage['validate_retrieval_rules']
    pages = stage['retrieval_page_by_id']
    chunks = stage['retrieval_chunk_by_id']
    passed = []
    source_hashes = dict(stage['retrieval_input_hashes'])
    model = QueryOnlyEmbeddings(stage['embeddings_model'])
    store = stage['open_policy_index'](stage['index_documents'], model, stage['embedding_info'])
    stage['vector_store_chroma'] = NoSearch()
    bad_inputs = [
        ('Maharashtra', '', 'clarification_required'),
        ('Maharashtra', None, 'clarification_required'),
        (None, 'Tamil Nadu incentives', 'unsupported_jurisdiction'),
        ('unknown', 'Incentives?', 'unsupported_jurisdiction'),
        ('Delhi', 'Incentives?', 'unsupported_jurisdiction'),
        ('Gujrat', 'Incentives?', 'unsupported_jurisdiction'),
        ('Telengana', 'Incentives?', 'unsupported_jurisdiction'),
        ('Karnataka', 'Incentives?', 'unsupported_jurisdiction'),
        ('UP', 'Incentives?', 'unsupported_jurisdiction'),
        ('MP', 'Incentives?', 'unsupported_jurisdiction'),
        ('FAME', 'Incentives?', 'unsupported_jurisdiction'),
        ('Maharashtra', 'Tamil Nadu road tax?', 'clarification_required'),
        ('Maharashtra', 'Kerala incentives?', 'clarification_required'),
        ('Maharashtra', 'Compare Maharashtra with Tamil Nadu', 'clarification_required'),
        ('Central', 'Combine PM E-DRIVE and Maharashtra incentives', 'clarification_required'),
        ('Maharashtra', 'Central subsidy for an e2w?', 'clarification_required'),
        ('Central', 'Electric buses incentive?', 'unsupported_scope'),
        ('Central', 'FAME II car subsidy?', 'unsupported_scope'),
        ('Central', 'EMPS eligibility?', 'unsupported_scope'),
        ('Central', 'Public charging station grant?', 'unsupported_scope'),
    ]
    for selection, question, status in bad_inputs:
        result = retrieve(selection, question)
        assert result['status'] == status, (selection, question, result)
        assert result['context_docs'] == [] and result['seed_chunk_ids'] == []
    passed.append('20_invalid_conflicting_or_unsupported_inputs_skip_search')
    for selection, question, expected in [
        ('mh', 'What are the incentives?', 'Maharashtra'),
        ('Tamilnadu', 'TN road tax', 'Tamil Nadu'),
        ('tamil nadu', 'Tamil Nadu subsidy', 'Tamil Nadu'),
        ('PM E-DRIVE', 'PM E DRIVE e-voucher', 'Central'),
        ('Maharashtra', 'How do I sign up for an incentive?', 'Maharashtra'),
    ]:
        result = route(selection, question)
        assert result['status'] == 'ready' and result['jurisdiction'] == expected
    assert stage['canonical_jurisdiction']('New Delhi') == 'Delhi'
    assert stage['mentioned_jurisdictions']('startup support') == set()
    passed.append('aliases_word_boundaries_and_lowercase_up_handled')
    stage['vector_store_chroma'] = store

    live_cases = [
        ('Maharashtra', 'What are the demand incentive caps for electric two-wheelers?'),
        ('Maharashtra', 'Which department reimburses toll exemptions?'),
        ('Tamilnadu', 'What period does the motor vehicle tax exemption cover?'),
        ('TN', 'What is the purchase incentive for private electric cycles?'),
        ('Tamil Nadu', 'What subsidy is described for private fast charging stations?'),
        ('Central', 'What is the electric two-wheeler incentive cap and deadline under PM E-DRIVE?'),
        ('Central', 'Are L5 three-wheelers registered after 26 December 2025 covered?'),
        ('PM E-DRIVE', 'How do the buyer and dealer sign the e-voucher?'),
    ]
    observed = []
    for selection, question in live_cases:
        result = retrieve(selection, question)
        assert result['status'] == 'retrieved', (selection, question, result['status'])
        state = result['jurisdiction']
        assert {chunks[id].metadata['state'] for id in result['seed_chunk_ids']} == {state}
        assert {doc.metadata['state'] for doc in result['context_docs']} == {state}
        ids = [doc.metadata['evidence_id'] for doc in result['context_docs']]
        assert len(ids) == len(set(ids))
        context_pages = {doc.metadata['page_id'] for doc in result['context_docs']}
        assert set(stage['retrieval_rules']['required_pages'][state]) <= context_pages
        for doc in result['context_docs']:
            metadata = doc.metadata
            page = pages[metadata['page_id']]
            assert doc.page_content == page.page_content[metadata['excerpt_start']:metadata['excerpt_end']]
            assert metadata['accepted_for_ingestion'] is False and metadata['current_entitlement_answers_allowed'] is False
            assert metadata['source'] == page.metadata['source'] and metadata['pdf_page'] == page.metadata['pdf_page']
            for field, value in page.metadata.items():
                assert metadata[field] == value
            for target in stage['page_links'](metadata, stage['required_link_fields']):
                assert target in context_pages, target
            rule = stage['retrieval_rules']['page_rules'].get(metadata['page_id'], {})
            assert set(rule.get('required_page_ids', [])) <= context_pages
            for span in rule.get('exclude_spans', []):
                assert metadata['excerpt_end'] <= span['start'] or metadata['excerpt_start'] >= span['end']
        observed.append({'selection': selection, 'question': question, 'jurisdiction': state,
            'seed_chunk_ids': result['seed_chunk_ids'], 'context_page_ids': sorted(context_pages),
            'context_characters': sum(len(doc.page_content) for doc in result['context_docs']),
            'omitted_spans': result['omitted_spans']})
    assert model.query_count == len(live_cases)
    passed += ['eight_live_queries_with_no_cross_jurisdiction_leakage',
        'one_query_embedding_each_and_no_corpus_embeddings', 'required_links_resolve_after_expansion',
        'exact_excerpts_citations_metadata_and_unverified_flags', 'unique_context_and_excluded_ranges_not_returned']

    def context_from_page(page_id):
        seed = next(doc for doc in chunks.values() if doc.metadata['page_id'] == page_id)
        return assemble([seed], seed.metadata['state'])[0]

    mh_context = context_from_page('maharashtra_policy_2025-05-23:p19')
    mh_text = '\n'.join(doc.page_content for doc in mh_context)
    assert 'The incentives are applicable for electric vehicles sold' in mh_text
    assert 'The policy will enable demonstration' not in mh_text
    assert any(doc.metadata['page_id'] == 'maharashtra_corrigendum_2025-08-29:p2' for doc in mh_context)
    assert {'maharashtra_operational_guidelines_2025-06-19:p2',
            'maharashtra_operational_guidelines_2025-06-19:p3',
            'maharashtra_operational_guidelines_2025-07-28:p1'} <= {d.metadata['page_id'] for d in mh_context}
    passed.append('maharashtra_replacement_and_operational_continuations_retained')

    tn_context = context_from_page('tamil_nadu_policy_2023:p17')
    tn_text = '\n'.join(doc.page_content for doc in tn_context)
    assert '100% road tax exemption will be provided till 31.12.2025' not in tn_text
    for doc in tn_context:
        if doc.metadata['page_id'] in ('tamil_nadu_policy_2023:p16','tamil_nadu_policy_2023:p17'):
            assert doc.metadata['context_role'] == 'historical_only'
    assert any(doc.metadata['page_id'] == 'tamil_nadu_motor_vehicle_tax_2025-12-29:p1' for doc in tn_context)
    assert '31.12.2025' in tn_text
    passed.append('tamil_nadu_tax_update_does_not_promote_expired_demand_or_fee_terms')

    central_context = context_from_page('central_pm_edrive_extension_2026-03-27:p3')
    central_text = '\n'.join(doc.page_content for doc in central_context)
    compact = ''.join(central_text.split())
    assert '31.07.2026' not in compact and '31stJuly2026' not in compact
    for phrase in ('31.03.2028','₹2,500/kWh, capped at ₹5,000 per vehicle','₹12,500 per vehicle',
                   '15% of ex-factory price','31st December 2027','no further claims will be entertained',
                   'registered after 26.12.2025 shall not be eligible'):
        assert ''.join(phrase.split()) in compact, phrase
    assert not any(doc.metadata['page_id'] == 'central_pm_edrive_amendment_2025-03-03:p8' for doc in central_context)
    assert '2. PMP for Vehicle Category e-buses' not in central_text
    passed += ['central_march_e2w_clause_removed_erickshaw_row_preserved',
        'central_latest_caps_dates_fund_limit_claim_deadline_and_l5_closure_retained',
        'central_buyer_pmp_conditions_retained_bus_only_context_excluded']

    for page_id, rule in stage['retrieval_rules']['page_rules'].items():
        context = context_from_page(page_id)
        for doc in context:
            applied = stage['retrieval_rules']['page_rules'].get(doc.metadata['page_id'], {})
            assert applied.get('context_role') != 'excluded_outside_scope'
            for span in applied.get('exclude_spans', []):
                assert doc.metadata['excerpt_end'] <= span['start'] or doc.metadata['excerpt_start'] >= span['end']
    passed.append('all_20_page_rules_exercised_without_superseded_or_excluded_spans')

    class EmptySearch:
        def as_retriever(self, search_kwargs):
            assert search_kwargs == {'k': 4, 'filter': {'state': 'Central'}}
            return self

        def invoke(self, question):
            return []

    stage['vector_store_chroma'] = EmptySearch()
    try:
        empty = retrieve('Central', 'e-voucher')
        assert empty['status'] == 'no_evidence' and empty['context_docs'] == []
    finally:
        stage['vector_store_chroma'] = store
    passed.append('empty_filtered_search_does_not_return_required_pages_as_a_match')

    wrong_seed = next(doc for doc in chunks.values() if doc.metadata['state'] == 'Central')
    expect_error(lambda: assemble([wrong_seed], 'Tamil Nadu'), 'another jurisdiction')
    modified_seed = copy.deepcopy(wrong_seed)
    modified_seed.page_content = 'not the indexed text'
    expect_error(lambda: assemble([modified_seed], 'Central'), 'differs from the checked corpus')
    passed.append('leaked_or_modified_search_hit_rejected')

    required = 'central_pm_edrive_extension_2026-08-10:p3'
    saved_page = pages.pop(required)
    try:
        expect_error(lambda: assemble([wrong_seed], 'Central'), 'Missing evidence page')
    finally:
        pages[required] = saved_page
    rule = stage['retrieval_rules']['page_rules']['maharashtra_policy_2025-05-23:p19']
    previous_targets = rule['required_page_ids']
    rule['required_page_ids'] = ['tamil_nadu_policy_2023:p16']
    try:
        expect_error(validate, 'Invalid rule dependency')
    finally:
        rule['required_page_ids'] = previous_targets
    previous_hash = rule['exclude_spans'][0]['text_sha256']
    rule['exclude_spans'][0]['text_sha256'] = '0' * 64
    try:
        expect_error(validate, 'Exclusion text hash mismatch')
    finally:
        rule['exclude_spans'][0]['text_sha256'] = previous_hash
    passed.append('missing_cross_jurisdiction_or_changed_rule_evidence_rejected')

    Path('tmp').mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='stage6-check-', dir='tmp') as folder:
        test_path = Path(folder) / 'changed_input.txt'
        test_path.write_text('original')
        stage['retrieval_input_hashes'][str(test_path)] = stage['index_file_hash'](test_path)
        test_path.write_text('changed')
        try:
            expect_error(lambda: retrieve('Central', 'e-voucher'), 'Retrieval input changed')
        finally:
            del stage['retrieval_input_hashes'][str(test_path)]
    previous_reader = stage['read_embedding_info']
    stage['read_embedding_info'] = lambda: dict(stage['embedding_info'], digest='changed')
    try:
        expect_error(lambda: retrieve('Central', 'e-voucher'), 'Embedding model changed')
    finally:
        stage['read_embedding_info'] = previous_reader
    passed.append('changed_inputs_or_model_rejected_before_search')

    limited = retrieve('Central', 'e-voucher', max_context_chars=1)
    assert limited['status'] == 'context_limit' and limited['context_docs'] == []
    expect_error(lambda: retrieve('Central', 'e-voucher', k=0), 'between 1 and 8')
    passed.append('context_budget_never_silently_drops_required_evidence')
    for path, digest in source_hashes.items():
        assert stage['index_file_hash'](path) == digest
    assert stage['check_index_contents'](store, stage['index_documents']) == 231
    passed.append('source_artifacts_and_saved_231_record_index_unchanged')
    validate()
    report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'technical_status': 'passed',
        'checks_passed': passed, 'rejected_input_cases': len(bad_inputs), 'live_queries': observed,
        'query_embedding_count': model.query_count, 'corpus_embeddings': 0,
        'corpus_sha256': stage['index_spec']['corpus_sha256'], 'input_sha256': source_hashes,
        'notebook_sha256': stage['index_file_hash']('EV Policy Assistant.ipynb'),
        'check_script_sha256': stage['index_file_hash'](__file__),
        'scope': 'technical retrieval checks; not team evaluation or verified current entitlement'}
    Path('data/processed/search/stage6_retrieval_checks.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Stage 6 retrieval checks passed:',len(passed))
    for case in observed:
        print(case['jurisdiction'],len(case['context_page_ids']),'pages;',case['context_characters'],'characters')


if __name__ == '__main__':
    run_checks()
