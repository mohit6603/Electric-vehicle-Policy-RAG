"""Run offline checks; --live adds six paced Groq questions using the saved index."""
import argparse
import copy
import json
import os
import re
import tempfile
import time
from pathlib import Path
from datetime import datetime, timezone
from unittest.mock import patch
from urllib.error import URLError
import httpx
import ollama
import groq
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda
from stage7_answer_checks import check_live_result, live_cases as stage7_cases


def load_stage8():
    notebook = json.loads(Path('EV Policy Assistant.ipynb').read_text())
    cells = ('stage5-imports', 'stage5-index-functions', 'stage6-inputs', 'stage6-routing',
             'stage6-context', 'stage7-schema', 'stage7-prompt', 'stage7-citations', 'stage7-answer',
             'stage8-results', 'stage8-startup', 'stage8-ask')
    stage = {}
    for cell in notebook['cells']:
        if cell['id'] in cells:
            exec(compile(''.join(cell['source']), cell['id'], 'exec'), stage)
    return stage


def save_report(stage, filename, **fields):
    report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
        'notebook_sha256': stage['index_file_hash']('EV Policy Assistant.ipynb'),
        'check_script_sha256': stage['index_file_hash'](__file__),
        'corpus_sha256': stage['index_spec']['corpus_sha256'],
        'retrieval_rules_sha256': stage['index_file_hash']('data/retrieval_rules.json'),
        'scope': 'AI-authored technical checks, not formal team evaluation', **fields}
    folder = Path('data/processed/answers')
    folder.mkdir(exist_ok=True, parents=True)
    (folder / filename).write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')


def fail(error):
    def raise_error(*args, **kwargs):
        raise error
    return raise_error


class FakeStore:
    def __init__(self, stage):
        self.stage = stage
        self.empty = False
        self.missing = False
        self.query_count = 0

    def get(self, include):
        docs = self.stage['index_documents']
        if self.missing:
            docs = docs[:-1]
        return {'ids': [doc.metadata['chunk_id'] for doc in docs],
                'documents': [doc.page_content for doc in docs],
                'metadatas': [doc.metadata for doc in docs]}

    def as_retriever(self, search_kwargs):
        assert search_kwargs['k'] == 1
        self.jurisdiction = search_kwargs['filter']['state']
        return self

    def invoke(self, question):
        self.query_count += 1
        if self.empty:
            return []
        page = {'Central': 'central_pm_edrive_extension_2026-08-10:p3',
                'Maharashtra': 'maharashtra_policy_2025-05-23:p18',
                'Tamil Nadu': 'tamil_nadu_motor_vehicle_tax_2025-12-29:p1'}[self.jurisdiction]
        return [next(doc for doc in self.stage['index_documents'] if doc.metadata['page_id'] == page)]


def run_offline():
    stage = load_stage8()
    passed, observations = [], []
    model_calls = []
    query = 'What e-2W rate does the supplied Central amendment state?'
    secret = 'PRIVATE_TEST_SENTINEL'
    valid = {'status': 'supported', 'points': [
        {'text': 'The supplied amendment states ₹2,500 per kWh.', 'citations': ['S1']}]}

    def model_reply(prompt):
        model_calls.append(1)
        return AIMessage(content=json.dumps(valid), response_metadata={'finish_reason': 'stop'})

    def check(name, result, status):
        assert result['status'] == status, (name, result)
        assert set(result) == {'status', 'answer', 'sources', 'points', 'jurisdiction',
            'verification_cutoff', 'current_entitlement_answers_allowed', 'model', 'usage',
            'reason', 'retryable', 'diagnostics'}, name
        assert result['current_entitlement_answers_allowed'] is False
        assert secret not in json.dumps(result) and secret not in json.dumps(stage['last_diagnostic'])
        if status != 'document_answer':
            assert result['sources'] == [] and result['points'] == [], name
        passed.append(name)
        observations.append({'case': name, 'status': status, 'answer': result['answer'],
                             'diagnostics': result['diagnostics'], 'retryable': result['retryable']})

    real_open, real_hash, real_key = stage['open_policy_index'], stage['index_file_hash'], stage['answer_key_available']
    original_hashes = {str(path): real_hash(path) for state in ('maharashtra', 'tamil_nadu', 'central')
                       for path in Path('data/processed', state).glob('*.jsonl')}
    Path('tmp').mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='stage8-', dir='tmp') as folder:
        index_path = Path(folder) / 'index'
        index_path.mkdir()
        (index_path / 'chroma.sqlite3').write_bytes(b'fixture; Chroma opening is replaced in offline checks')
        receipt = index_path / 'index_manifest.json'
        receipt.write_text('{}')
        stage['index_dir'] = index_path
        fake = FakeStore(stage)
        embedding = {'model': stage['model_name'], 'digest': 'offline-fixture',
                     'num_ctx': stage['embedding_context'], 'langchain_ollama': 'offline-fixture'}
        stage.update(read_embedding_info=lambda: dict(embedding), OllamaEmbeddings=lambda **kwargs: object(),
            open_policy_index=lambda *args, **kwargs: fake,
            rebuild_policy_index=fail(AssertionError('No automatic rebuild is permitted.')),
            answer_key_available=lambda: True, get_answer_llm=lambda: RunnableLambda(model_reply))
        ask = stage['ask_policy']
        assert stage['start_policy_assistant']()['status'] == 'ready'
        assert not model_calls and fake.query_count == 0
        check('supported_fixture_before_failures', ask('Central', query), 'document_answer')
        calls = len(model_calls)
        searches = fake.query_count
        for name, selection, question, status in [
            ('empty_question', 'Central', '', 'clarification_required'),
            ('non_string_question', 'Central', None, 'clarification_required'),
            ('punctuation_only', 'Central', '???', 'clarification_required'),
            ('oversized_question', 'Central', 'x' * 2001, 'clarification_required'),
            ('missing_selection', None, query, 'unsupported_jurisdiction'),
            ('unsupported_state', 'Delhi', query, 'unsupported_jurisdiction'),
            ('jurisdiction_conflict', 'Maharashtra', 'Tamil Nadu road tax?', 'clarification_required'),
            ('two_jurisdictions', 'Maharashtra', 'Compare Maharashtra and Tamil Nadu', 'clarification_required'),
            ('outside_central_pilot', 'Central', 'Electric bus grant?', 'unsupported_scope'),
            ('ambiguous_followup', 'Central', 'What about it?', 'clarification_required'),
            ('current_availability', 'Central', 'Is the e-2W subsidy currently available?', 'not_established'),
            ('personal_eligibility', 'Central', 'Can I get an e-2W incentive?', 'not_established'),
            ('remaining_funds', 'Central', 'What are the remaining funds?', 'not_established'),
        ]:
            check(name, ask(selection, question), status)
        assert len(model_calls) == calls and fake.query_count == searches
        passed.append('rejected_inputs_skip_embedding_and_generation')

        with patch.dict(stage, {'answer_key_available': real_key, 'load_dotenv': lambda *args, **kwargs: False}):
            with patch.dict(os.environ, {}, clear=True):
                check('missing_key', ask('Central', query), 'configuration_error')
        assert len(model_calls) == calls and fake.query_count == searches
        with patch.dict(stage, {'get_answer_llm': fail(ValueError(secret))}):
            check('invalid_model_configuration_is_redacted', ask('Central', query), 'configuration_error')

        fake.empty = True
        check('empty_filtered_evidence', ask('Central', query), 'no_evidence')
        fake.empty = False
        no_answer = lambda prompt: AIMessage(content='{"status":"not_established","points":[]}')
        with patch.dict(stage, {'get_answer_llm': lambda: RunnableLambda(no_answer)}):
            check('irrelevant_evidence_abstention_fixture', ask('Central', 'Recipe?'), 'not_established')
        retrieve = stage['retrieve_policy']
        with patch.dict(stage, {'retrieve_policy': lambda *args, **kwargs: retrieve(*args, **kwargs, max_context_chars=1)}):
            check('context_overflow_returns_no_partial_answer', ask('Central', query), 'context_limit')
        for name, content, finish in [('invalid_source_id', json.dumps({'status': 'supported', 'points': [
                {'text': secret, 'citations': ['S999']}]}), 'stop'),
                ('malformed_model_output', secret, 'stop'),
                ('truncated_completion', json.dumps(valid), 'length')]:
            response = AIMessage(content=content, response_metadata={'finish_reason': finish})
            with patch.dict(stage, {'get_answer_llm': lambda: RunnableLambda(lambda prompt: response)}):
                check(name, ask('Central', query), 'citation_error')

        request = httpx.Request('POST', 'https://example.invalid')
        for code, cls, status in [(401, groq.AuthenticationError, 'authentication_error'),
                (403, groq.PermissionDeniedError, 'authentication_error'),
                (429, groq.RateLimitError, 'rate_limited'), (413, groq.APIStatusError, 'request_too_large'),
                (500, groq.InternalServerError, 'model_unavailable'), (400, groq.BadRequestError, 'model_error')]:
            error = cls(secret, response=httpx.Response(code, request=request), body={'private': secret})
            with patch.dict(stage, {'get_answer_llm': lambda: RunnableLambda(fail(error))}):
                check(f'groq_http_{code}', ask('Central', query), status)
        for error, status in [(groq.APIConnectionError(request=request), 'model_unavailable'),
                              (groq.APITimeoutError(request=request), 'model_timeout')]:
            with patch.dict(stage, {'get_answer_llm': lambda: RunnableLambda(fail(error))}):
                check(type(error).__name__, ask('Central', query), status)

        for name, error, status in [('ollama_query_timeout', httpx.ReadTimeout(secret), 'embedding_timeout'),
                ('ollama_query_disconnect', httpx.ConnectError(secret), 'embedding_unavailable'),
                ('ollama_query_model_missing', ollama.ResponseError(secret, 404), 'embedding_model_missing'),
                ('ollama_query_server_error', ollama.ResponseError(secret, 500), 'embedding_error'),
                ('missing_runtime_evidence', KeyError(secret), 'data_error'),
                ('unexpected_error', RuntimeError(secret), 'internal_error')]:
            assert stage['start_policy_assistant']()['status'] == 'ready'
            with patch.dict(stage, {'answer_question': fail(error)}):
                check(name, ask('Central', query), status)
            assert not stage['assistant_state']['index_ready']

        assert stage['start_policy_assistant']()['status'] == 'ready'
        changed = dict(embedding, digest='changed-model')
        with patch.dict(stage, {'read_embedding_info': lambda: changed}):
            check('model_digest_change', ask('Central', query), 'index_error')
        assert stage['start_policy_assistant']()['status'] == 'ready'
        fake.missing = True
        check('warm_index_missing_records', ask('Central', query), 'index_error')
        fake.missing = False
        assert stage['start_policy_assistant']()['status'] == 'ready'
        receipt.write_text('{"changed":true}')
        check('warm_index_receipt_change', ask('Central', query), 'index_error')
        receipt.unlink()
        check('missing_index_does_not_build', stage['start_policy_assistant'](), 'index_error')
        receipt.write_text('not JSON')
        with patch.dict(stage, {'open_policy_index': real_open}):
            check('corrupt_index_receipt', stage['start_policy_assistant'](), 'index_error')
        receipt.write_text('{"index_spec":{}}')
        with patch.dict(stage, {'open_policy_index': real_open}):
            check('stale_index_receipt', stage['start_policy_assistant'](), 'index_error')
        receipt.write_text('{}')

        for error, status in [(RuntimeError(secret), 'embedding_unavailable'),
                (ValueError('Install the embedding model with ollama pull nomic-embed-text.'), 'embedding_model_missing')]:
            with patch.dict(stage, {'read_embedding_info': fail(error)}):
                check('startup_' + status, stage['start_policy_assistant'](), status)
        stage['reset_policy_assistant']()
        with patch.dict(stage, {'load_index_chunks': fail(FileNotFoundError(secret))}):
            check('missing_source_at_startup', stage['start_policy_assistant'](), 'data_error')
        with patch.dict(stage, {'load_retrieval_inputs': fail(ValueError(secret))}):
            check('corrupt_source_or_rules_at_startup', stage['start_policy_assistant'](), 'data_error')
        assert stage['start_policy_assistant']()['status'] == 'ready'
        path = next(iter(stage['retrieval_input_hashes']))
        with patch.dict(stage, {'index_file_hash': lambda p: 'changed' if str(p) == path else real_hash(p)}):
            check('changed_runtime_source', ask('Central', query), 'data_error')
        stage['reset_policy_assistant']()
        check('recovery_has_fresh_answer_and_no_stale_diagnostic', ask('Central', query), 'document_answer')
        assert stage['last_diagnostic'] == {}
        assert all(real_hash(path) == digest for path, digest in original_hashes.items())
        passed.append('six_corpus_files_unchanged_and_no_live_services_used')
        save_report(stage, 'stage8_failure_checks.json', technical_status='passed', checks_passed=passed,
            cases=observations, groq_calls=0, ollama_calls=0,
            note='Failures are injected with SDK exception types and isolated index files; supported model replies are fixtures.')
    print('Stage 8 offline checks passed:', len(passed))


def run_live():
    stage = load_stage8()
    service_url = stage['ollama_url']
    stage['ollama_url'] = 'http://127.0.0.1:1'
    disconnected = stage['start_policy_assistant']()
    assert disconnected['status'] == 'embedding_unavailable', disconnected
    stage['ollama_url'] = service_url
    stage['reset_policy_assistant']()
    ready = stage['start_policy_assistant']()
    assert ready['status'] == 'ready', ready
    original_llm = stage['get_answer_llm']
    service_errors = []

    def observed_llm():
        llm = original_llm()

        def invoke(prompt):
            try:
                return llm.invoke(prompt)
            except groq.APIError as error:
                body = error.body if isinstance(error.body, dict) else {}
                message = body.get('message', '')
                if not message and isinstance(body.get('error'), dict):
                    message = body['error'].get('message', '')
                fields = re.findall(r'(?:Limit|Requested)[ :]+[0-9,]+', message)
                diagnostic = {'http_status': getattr(error, 'status_code', None),
                    'prompt_characters': sum(len(m.content) for m in prompt.to_messages()),
                    'size_fields': fields}
                service_errors.append(diagnostic)
                print('Service diagnostic:', diagnostic, flush=True)
                raise

        return RunnableLambda(invoke)

    stage['get_answer_llm'] = observed_llm
    cases = [case for case in stage7_cases if case['id'] in
             ('mh_two_wheeler', 'tn_motor_tax', 'central_two_wheeler', 'central_l5_deadlines')]
    cases += [
        {'id': 'missing_insurance_fact', 'selection': 'Tamil Nadu',
         'question': 'What exact annual insurance premium does the policy specify for a Bajaj Chetak?',
         'patterns': [], 'page_ids': [], 'expected_status': 'not_established'},
        {'id': 'irrelevant_even_with_policy_words', 'selection': 'Central',
         'question': 'For an EV policy event, give me a chocolate cake recipe.',
         'patterns': [], 'page_ids': [], 'expected_status': 'not_established'},
    ]
    observations = []
    for number, case in enumerate(cases):
        print('Waiting 55 seconds before the Groq check.', flush=True)
        time.sleep(55)
        print('Live case:', case['id'], flush=True)
        result = stage['ask_policy'](case['selection'], case['question'])
        earlier = []
        if result['status'] == 'rate_limited':
            earlier.append(result)
            print('Rate limit: one retry after 55 seconds.', flush=True)
            time.sleep(55)
            result = stage['ask_policy'](case['selection'], case['question'])
        checks = check_live_result(case, result)
        checks['consistent_reply_fields'] = set(result) == set(stage['policy_reply']('ready', ''))
        if case.get('expected_status') == 'not_established':
            checks['no_unsupported_claims_or_sources'] = not result['points'] and not result['sources']
        observations.append({'case': case, 'checks': checks, 'result': result, 'earlier_attempts': earlier})
        passed = all(all(row['checks'].values()) for row in observations)
        save_report(stage, 'stage8_live_checks.json', technical_status=('passed' if passed else 'failed')
            if len(observations) == len(cases) else 'in_progress', observations=observations,
            completed_cases=len(observations), model=stage['answer_model_name'],
            model_settings=stage['answer_model_settings'], retrieval_k=stage['answer_retrieval_k'],
            unavailable_local_endpoint_check=disconnected, service_errors=service_errors)
        print(result['status'], checks, flush=True)
        print(result['answer'], flush=True)
    assert passed, 'Inspect stage8_live_checks.json; no failed case counts as passed.'
    print('Stage 8 live cases passed:', len(cases), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true')
    args = parser.parse_args()
    run_offline()
    if args.live:
        run_live()
