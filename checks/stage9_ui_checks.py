"""Check the Gradio callback over local HTTP; --serve runs the observed live pilot."""
import argparse
import copy
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from gradio_client import Client
from stage8_failure_checks import load_stage8


def run_cell(stage, name):
    notebook = json.loads(Path('EV Policy Assistant.ipynb').read_text())
    cell = next(cell for cell in notebook['cells'] if cell['id'] == name)
    exec(compile(''.join(cell['source']), name, 'exec'), stage)


def save_report(stage, name, **fields):
    folder = Path('data/processed/ui')
    folder.mkdir(parents=True, exist_ok=True)
    report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
        'notebook_sha256': stage['index_file_hash']('EV Policy Assistant.ipynb'),
        'check_script_sha256': stage['index_file_hash'](__file__),
        'retrieval_rules_sha256': stage['index_file_hash']('data/retrieval_rules.json'),
        'scope': 'AI-authored development checks; source review and formal evaluation pending', **fields}
    (folder / name).write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')


def run_checks():
    stage = load_stage8()
    assert stage['prepare_policy_sources']()['status'] == 'ready'
    run_cell(stage, 'stage9-callback')
    source_report = json.loads(Path('data/processed/answers/stage8_live_checks.json').read_text())
    fixture = next(row['result'] for row in source_report['observations']
                   if row['case']['id'] == 'central_two_wheeler')
    ask = stage['ask_policy']
    calls, checks, observations = [], [], []

    def fail(*args, **kwargs):
        raise AssertionError('These UI checks must not call model services or rebuild.')

    def test_ask(selection, question):
        calls.append((selection, question))
        if question == 'supported fixture':
            return copy.deepcopy(fixture)
        if question == 'rate limit fixture':
            return stage['groq_failure_reply']({'jurisdiction': selection,
                'error_type': 'RateLimitError', 'http_status': 429})
        return ask(selection, question)

    stage.update(ask_policy=test_ask, get_answer_llm=fail, read_embedding_info=fail,
        rebuild_policy_index=fail, answer_key_available=lambda: False,
        stage9_startup=stage['policy_reply']('ready', 'Test sources loaded.'),
        ui_choices=list(stage['retrieval_choices']))
    run_cell(stage, 'stage9-interface')
    demo = stage['demo']
    assert stage['ui_choices'] == ['Central', 'Maharashtra', 'Tamil Nadu']
    assert len(demo.input_components) == len(demo.output_components) == 2
    assert demo.input_components[0].allow_custom_value is False
    assert all(component.sanitize_html for component in demo.output_components)
    assert demo.concurrency_limit == 1 and demo.enable_queue
    assert demo.flagging_mode == 'never' and not demo.analytics_enabled
    checks += ['only_indexed_choices', 'two_inputs_and_outputs', 'no_custom_selection',
               'markdown_sanitization', 'serial_queue', 'no_flagging_or_analytics']
    try:
        _, url, _ = demo.launch(server_name='127.0.0.1', share=False,
            prevent_thread_lock=True, show_error=False, show_api=False, quiet=True)
        client = Client(url, verbose=False)
        for name, selection, question, expected in [
            ('supported_fixture_over_http', 'Central', 'supported fixture', '₹2,500'),
            ('empty_question_clears_citations', 'Central', '', 'Enter a specific'),
            ('mismatch_over_http', 'Maharashtra', 'Tamil Nadu road tax?', 'Align the selected'),
            ('unsupported_named_state', 'Central', 'What does the Delhi EV policy state?', 'Align the selected'),
            ('unsupported_central_segment', 'Central', 'What electric bus grant does Central provide?', 'pilot covers'),
            ('current_entitlement_abstains', 'Central', 'Can I claim an e-2W incentive today?', 'cannot verify'),
            ('missing_key_over_http', 'Central', 'What e-2W rate does the amendment state?', 'GROQ_API_KEY'),
            ('rate_limit_fixture_over_http', 'Central', 'rate limit fixture', 'allowance'),
        ]:
            output = client.predict(selection, question, api_name='/answer_policy')
            assert len(output) == 2 and all(isinstance(value, str) for value in output), (name, output)
            assert expected.casefold() in output[0].casefold(), (name, output)
            assert calls[-1] == (selection, question), name
            if name.startswith('supported'):
                assert '#page=3' in output[0] and '#page=3' in output[1]
                assert 'Central' in output[1] and 'PDF page 3' in output[1]
                assert '\n\nSources:\n\n' not in output[0]
            else:
                assert output[1] == '### Sources\n\nNo sources cited.' and '#page=' not in output[0], name
            observations.append({'case': name, 'outputs': output})
            checks.append(name)
        with tempfile.TemporaryDirectory(prefix='stage9-', dir='tmp') as folder:
            stage['index_dir'] = Path(folder)
            stage['answer_key_available'] = lambda: True
            output = client.predict('Central', 'What e-2W rate is in the amendment?', api_name='/answer_policy')
            assert 'saved index' in output[0] and output[1] == '### Sources\n\nNo sources cited.', output
            checks.append('missing_index_over_http_without_rebuild')
            observations.append({'case': checks[-1], 'outputs': output})
    finally:
        demo.close()
    save_report(stage, 'stage9_ui_checks.json', technical_status='passed', checks_passed=checks,
        observations=observations, groq_calls=0, ollama_calls=0,
        note='Supported/rate-limit responses are explicit fixtures; other cases use actual Stage 8 guards through Gradio HTTP.')
    print('Stage 9 UI checks passed:', len(checks), flush=True)


def serve(missing_key=False):
    stage = load_stage8()
    corpus_hashes = {str(path): stage['index_file_hash'](path)
        for state in ('maharashtra', 'tamil_nadu', 'central')
        for path in Path('data/processed', state).glob('*.jsonl')}
    embedding_calls = {'corpus': 0, 'query': 0}
    base_embedding = stage['OllamaEmbeddings']

    class ObservedEmbeddings(base_embedding):
        def embed_documents(self, texts):
            embedding_calls['corpus'] += 1
            raise AssertionError('UI startup must not embed the corpus.')

        def embed_query(self, text):
            embedding_calls['query'] += 1
            return base_embedding.embed_documents(self, [text])[0]

    def no_rebuild(*args, **kwargs):
        raise AssertionError('UI startup must not rebuild.')

    stage.update(OllamaEmbeddings=ObservedEmbeddings, rebuild_policy_index=no_rebuild)
    run_cell(stage, 'stage9-callback')
    run_cell(stage, 'stage9-startup')
    assert stage['stage9_startup']['status'] == 'ready', stage['stage9_startup']
    assert embedding_calls == {'corpus': 0, 'query': 0}
    assert stage['vector_store_chroma']._collection.count() == 231
    startup = {'status': 'ready', 'records': 231, 'corpus_embeddings': 0, 'query_embeddings': 0,
               'groq_calls': 0, 'corpus_sha256': stage['index_spec']['corpus_sha256']}
    observations = []
    if missing_key:
        stage['answer_key_available'] = lambda: False
    ask = stage['ask_policy']
    report_name = 'stage9_missing_key_ui.json' if missing_key else 'stage9_live_ui.json'

    def observed_ask(selection, question):
        result = ask(selection, question)
        assert all(stage['index_file_hash'](path) == digest for path, digest in corpus_hashes.items())
        observations.append({'selection': selection, 'question': question, 'result': result})
        save_report(stage, report_name, technical_status='observed', startup=startup,
            embedding_calls=embedding_calls, observations=observations,
            missing_key_injected=missing_key)
        print('Observed:', result['status'], flush=True)
        return result

    stage['ask_policy'] = observed_ask
    run_cell(stage, 'stage9-interface')
    print('Live UI ready; startup made zero embedding/Groq calls.', flush=True)
    stage['demo'].launch(server_name='127.0.0.1', server_port=7861 if missing_key else 7860,
        share=False, show_error=False, show_api=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--serve', action='store_true', help='Serve the real pilot for browser checks.')
    parser.add_argument('--missing-key', action='store_true', help='Inject absent-key behavior in the observed test server.')
    args = parser.parse_args()
    assert not args.missing_key or args.serve, '--missing-key requires --serve'
    if args.serve:
        serve(args.missing_key)
    else:
        run_checks()
