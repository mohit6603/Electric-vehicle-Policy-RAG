"""Test review transitions in memory; never mark real sources as accepted."""
import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch


def run_checks():
    notebook = json.loads(Path('EV Policy Assistant.ipynb').read_text())
    manifest = json.loads(Path('data/source_manifest.json').read_text())
    reviews = {str(p): json.loads(p.read_text()) for p in Path('data/ocr').glob('*/review.json')}
    paths = [Path('data/source_manifest.json'), *map(Path, reviews), *Path('data/processed').glob('*/*.jsonl')]
    before = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    loader = next(c for c in notebook['cells'] if c['id'] == 'shared-loader')
    stage = {}
    exec(compile(''.join(loader['source']), 'shared-loader', 'exec'), stage)
    validate = stage['validate_review_status']
    checks = []
    today = datetime.now(timezone.utc).date().isoformat()
    reviewed = {'team_verified': True, 'accepted_for_ingestion': True,
                'reviewer': 'Synthetic test fixture only', 'reviewed_on': today}
    validate(reviewed, 'fixture')
    checks.append('recorded_review_accepted')
    validate({'team_verified': False}, 'legacy pending OCR')
    checks.append('legacy_pending_ocr_without_acceptance_flag')
    for label, update in [('missing_reviewer', {'reviewer': ''}),
        ('invalid_date', {'reviewed_on': '2026-09-31'}), ('future_date', {'reviewed_on': '2999-01-01'}),
        ('unverified_acceptance', {'team_verified': False}), ('non_boolean_flags', {'team_verified': 'yes'})]:
        try:
            validate({**reviewed, **update}, label)
        except ValueError:
            checks.append(label + '_rejected')
        else:
            raise AssertionError(label)

    accepted_manifest = copy.deepcopy(manifest)
    for source in accepted_manifest['sources']:
        source.update(reviewed)
    accepted_reviews = copy.deepcopy(reviews)
    for review in accepted_reviews.values():
        for page in review['pages']:
            page.update(reviewed)
    original_read = Path.read_text

    def fixture_read(path, *args, **kwargs):
        if str(path) == 'data/source_manifest.json':
            return json.dumps(accepted_manifest)
        if str(path) in accepted_reviews:
            return json.dumps(accepted_reviews[str(path)])
        return original_read(path, *args, **kwargs)

    with patch.object(Path, 'read_text', fixture_read):
        for cell in notebook['cells']:
            if cell['cell_type'] != 'code' or cell['id'].endswith('-export'):
                continue
            if cell['id'].startswith(('stage2-', 'stage3-', 'stage4-', 'stage10-')):
                exec(compile(''.join(cell['source']), cell['id'], 'exec'), stage)
    groups = ['page_documents', 'tn_pages', 'central_pages', 'up_pages', 'delhi_pages',
              'gujarat_pages', 'telangana_pages', 'karnataka_pages', 'mp_pages']
    for group in groups:
        assert all(d.metadata['accepted_for_ingestion'] and d.metadata['team_verified'] for d in stage[group])
        assert stage['ingestion_acceptance'](stage[group]) == 'team_review_recorded'
    checks.append('all_nine_ingestion_paths_accept_recorded_review')
    ai_pages = [d for group in groups for d in stage[group] if d.metadata['text_status'] == 'ai_proposal']
    assert ai_pages and all(d.metadata['reviewer'] == reviewed['reviewer'] for d in ai_pages)
    assert all('pending team review' not in d.metadata['text_derivation'].lower() for d in ai_pages)
    checks.append('ocr_review_and_derivation_preserved')
    try:
        stage['load_policy_pages'](accepted_manifest, reviews['data/ocr/telangana/review.json'], 'Telangana')
    except ValueError as error:
        assert 'unaccepted OCR' in str(error)
        checks.append('accepted_source_with_unaccepted_ocr_rejected')
    else:
        raise AssertionError('Unaccepted OCR was silently accepted.')
    for state in dict.fromkeys(source['state'] for source in manifest['sources']):
        sources = [source for source in manifest['sources'] if source['state'] == state]
        review_files = {source['ocr_review_file'] for source in sources if 'ocr_review_file' in source}
        review = {'pages': [page for name in review_files for page in reviews[name]['pages']]}
        candidate = stage['load_policy_pages'](manifest, review, state)
        assert all(not d.metadata['team_verified'] and not d.metadata['accepted_for_ingestion'] for d in candidate)
        assert stage['ingestion_acceptance'](candidate) == 'deferred_not_verified'
    checks.append('real_candidate_flags_stay_false')
    assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest() == value for p, value in before.items())
    checks.append('source_reviews_and_corpus_files_untouched')
    print('Review transition checks passed:', len(checks))
    return checks


if __name__ == '__main__':
    run_checks()
