"""Run from the project root: uv run --locked python checks/stage5_index_checks.py."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

from langchain_core.embeddings import Embeddings


class CountedEmbeddings(Embeddings):
    def __init__(self, model, forbid_documents=False):
        self.model = model
        self.forbid_documents = forbid_documents
        self.document_count = 0
        self.query_count = 0

    def embed_documents(self, texts):
        if self.forbid_documents:
            raise AssertionError('Startup attempted corpus embedding.')
        self.document_count += len(texts)
        return self.model.embed_documents(texts)

    def embed_query(self, text):
        self.query_count += 1
        return self.model.embed_query(text)


def load_stage5():
    notebook = json.loads(Path('EV Policy Assistant.ipynb').read_text())
    namespace = {}
    for cell in notebook['cells']:
        if cell['id'] in ('stage5-imports', 'stage5-index-functions', 'stage5-inputs'):
            exec(compile(''.join(cell['source']), cell['id'], 'exec'), namespace)
    return namespace


def expect_error(action, message):
    try:
        action()
    except ValueError as error:
        assert message in str(error), str(error)
    else:
        raise AssertionError(f'Expected rejection containing: {message}')


def restart_check(output_path):
    stage = load_stage5()
    model = CountedEmbeddings(stage['embeddings_model'], forbid_documents=True)
    store = stage['open_policy_index'](stage['index_documents'], model, stage['embedding_info'])
    before_query = {'documents': model.document_count, 'queries': model.query_count}
    assert before_query == {'documents': 0, 'queries': 0}
    question = 'How does the PM E-DRIVE buyer and dealer sign the e-voucher?'
    hits = store.as_retriever(search_kwargs={'k': 3}).invoke(question)
    assert len(hits) == 3 and model.document_count == 0 and model.query_count == 1
    assert any(doc.metadata['state'] == 'Central' and 'voucher' in doc.page_content.lower() for doc in hits)
    output_path.write_text(json.dumps({
        'chunk_count': len(store.get()['ids']), 'embedding_calls_before_query': before_query,
        'document_embeddings_after_query': model.document_count, 'query_embeddings': model.query_count,
        'retrieved_chunk_ids': [doc.metadata['chunk_id'] for doc in hits],
    }, indent=2) + '\n')


def run_checks():
    Path('tmp').mkdir(exist_ok=True)
    stage = load_stage5()
    documents = stage['index_documents']
    info = stage['embedding_info']
    model = CountedEmbeddings(stage['embeddings_model'])
    build = stage['rebuild_policy_index']
    reopen = stage['open_policy_index']
    check = stage['check_index_contents']
    passed = []
    with tempfile.TemporaryDirectory(prefix='stage5-check-', dir='tmp') as folder:
        folder = Path(folder)
        restart_output = folder / 'restart.json'
        subprocess.run([sys.executable, __file__, '--restart', str(restart_output)], check=True)
        restart = json.loads(restart_output.read_text())
        assert restart['chunk_count'] == len(documents) == 231
        passed += ['fresh_process_reopens_all_231_without_embeddings', 'query_embeds_only_question']

        # Real policy chunks in an isolated store; production data is read-only here.
        sample = [doc for state in ('Maharashtra', 'Tamil Nadu', 'Central')
                  for doc in [d for d in documents if d.metadata['state'] == state][:2]]
        path = folder / 'chroma'
        expect_error(lambda: reopen(sample, model, info, path), 'missing/incomplete')
        assert not path.exists()
        passed.append('missing_index_rejected_without_creation')
        store = build(sample, model, info, path)
        assert check(store, sample, True) == 768
        assert model.document_count == len(sample)
        store = build(sample, model, info, path)
        assert check(store, sample) == len(sample) and model.document_count == 2 * len(sample)
        passed.append('repeat_full_rebuild_has_no_duplicates')

        previous_calls = model.document_count
        for unused in range(2):
            reopen(sample, model, info, path)
        assert model.document_count == previous_calls
        passed.append('repeated_open_does_not_embed_documents')

        changed = copy.deepcopy(sample)
        changed[0].metadata['test_revision'] = 1
        expect_error(lambda: reopen(changed, model, info, path), 'Corpus or embedding model changed')
        changed = copy.deepcopy(sample)
        changed[0].page_content += '\nTest-only changed text.'
        expect_error(lambda: reopen(changed, model, info, path), 'Corpus or embedding model changed')
        expect_error(lambda: reopen(sample[:-1], model, info, path), 'Corpus or embedding model changed')
        changed_info = dict(info, digest='test-changed-model-digest')
        expect_error(lambda: reopen(sample, model, changed_info, path), 'Corpus or embedding model changed')
        assert model.document_count == previous_calls
        passed += ['metadata_change_requires_rebuild', 'text_change_requires_rebuild',
                   'removed_chunk_requires_rebuild', 'changed_model_digest_requires_rebuild']

        receipt = (path / 'index_manifest.json').read_bytes()
        expect_error(lambda: build(sample + [sample[0]], model, info, path), 'duplicate chunk IDs')
        expect_error(lambda: build([], model, info, path), 'empty input')
        assert (path / 'index_manifest.json').read_bytes() == receipt
        assert check(store, sample) == len(sample)
        passed.append('invalid_build_input_keeps_previous_index')

        # Same IDs/count are insufficient: check the stored metadata and text too.
        chunk_id = sample[0].metadata['chunk_id']
        store._collection.update(ids=[chunk_id], metadatas=[dict(sample[0].metadata, test_revision=1)])
        expect_error(lambda: reopen(sample, model, info, path), 'text/metadata differs')
        saved_vector = store.get(ids=[chunk_id], include=['embeddings'])['embeddings'][0]
        store._collection.update(ids=[chunk_id], documents=['Test-only altered database text.'], embeddings=[saved_vector])
        expect_error(lambda: reopen(sample, model, info, path), 'text/metadata differs')
        store.delete(ids=[sample[-1].metadata['chunk_id']])
        expect_error(lambda: reopen(sample, model, info, path), 'missing or stale chunks')
        passed += ['stored_metadata_or_text_change_rejected', 'missing_saved_chunk_rejected']

        replacement = next(doc for doc in documents if doc.metadata['chunk_id'] not in {d.metadata['chunk_id'] for d in sample})
        changed = copy.deepcopy(sample[:-1]) + [replacement]
        changed[0].metadata['test_revision'] = 2
        store = build(changed, model, info, path)
        assert check(store, changed) == len(changed)
        assert sample[-1].metadata['chunk_id'] not in store.get()['ids']
        passed.append('changed_rebuild_replaces_metadata_adds_and_removes_chunks')

        receipt_path = path / 'index_manifest.json'
        receipt_path.write_text('{unfinished')
        expect_error(lambda: reopen(changed, model, info, path), 'Invalid index manifest')
        receipt_path.unlink()
        expect_error(lambda: reopen(changed, model, info, path), 'missing/incomplete')
        passed.append('invalid_or_missing_receipt_rejected')

        # Interrupt after one inserted batch and ensure no completed receipt survives.
        real_add = stage['Chroma'].add_documents
        calls = []
        def interrupted_add(self, *args, **kwargs):
            calls.append(1)
            if len(calls) == 2:
                raise RuntimeError('simulated interruption')
            return real_add(self, *args, **kwargs)
        stage['Chroma'].add_documents = interrupted_add
        try:
            try:
                build(documents[:33], model, info, path)
            except RuntimeError as error:
                assert str(error) == 'simulated interruption'
            else:
                raise AssertionError('Expected interrupted build.')
        finally:
            stage['Chroma'].add_documents = real_add
        assert not receipt_path.exists()
        expect_error(lambda: reopen(documents[:33], model, info, path), 'missing/incomplete')
        store = build(sample, model, info, path)
        assert check(reopen(sample, model, info, path), sample) == len(sample)
        passed.append('interrupted_build_rejected_then_recovered')
        store.delete_collection()
        expect_error(lambda: reopen(sample, model, info, path), 'collection is missing')
        passed.append('missing_collection_not_silently_created')

    report = {
        'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'technical_status': 'passed',
        'checks_passed': passed, 'restart': restart, 'isolated_rebuild_sample_chunks': len(sample),
        'test_store_document_embeddings': model.document_count,
        'corpus_sha256': stage['index_spec']['corpus_sha256'],
        'notebook_sha256': stage['index_file_hash']('EV Policy Assistant.ipynb'),
        'check_script_sha256': stage['index_file_hash'](__file__),
        'scope': 'persistence/integrity checks; no policy-answer evaluation or human source review',
    }
    Path('data/processed/search/stage5_persistence_checks.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Stage 5 persistence checks passed:', len(passed))


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--restart':
        restart_check(Path(sys.argv[2]))
    else:
        run_checks()
