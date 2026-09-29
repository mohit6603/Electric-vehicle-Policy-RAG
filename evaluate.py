"""Freeze team-written cases, then record two resumable evaluation batches."""
import argparse
import hashlib
import json
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from run import DEFINITION_CELLS, load_cells

CASE_FILE = Path('evaluation/team_cases.json')
FROZEN_FILE = Path('evaluation/frozen_cases.json')
STATES = ['Maharashtra', 'Tamil Nadu', 'Uttar Pradesh', 'Delhi', 'Gujarat',
          'Telangana', 'Karnataka', 'Madhya Pradesh']


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def validate_cases(data, pages, sources):
    review = data['source_review']
    if review['completed'] is not True or not review['reviewer'] or not review['reviewed_on']:
        raise ValueError('Complete and record the deferred team source review before formal evaluation.')
    if not all(s['accepted_for_ingestion'] and s['team_verified'] for s in sources):
        raise ValueError('Source manifest still contains unaccepted sources; finish review and refresh ingestion first.')
    cases = data['cases']
    if len(cases) != 24 or len({c['id'] for c in cases}) != 24:
        raise ValueError('Use 24 unique case IDs.')
    counts = Counter(c['group'] for c in cases)
    if counts != Counter({**dict.fromkeys(STATES, 2), 'Central': 4, 'negative': 4}):
        raise ValueError('Use two cases per jurisdiction, four Central cases and four negative cases.')
    for case in cases:
        for field in ('question', 'selection', 'expected_answer', 'expected_status', 'authored_by', 'verified_by', 'verified_on'):
            if not isinstance(case[field], str) or not case[field].strip():
                raise ValueError(f'{case["id"]}: fill {field} independently from official evidence.')
        date = datetime.strptime(case['verified_on'], '%Y-%m-%d').date()
        if date > datetime.now().date():
            raise ValueError('Verification date cannot be in the future.')
        if not isinstance(case['expected_page_ids'], list) or any(p not in pages for p in case['expected_page_ids']):
            raise ValueError(f'{case["id"]}: unknown physical page reference.')
        if case['group'] != 'negative':
            if case['expected_status'] != 'document_answer' or not case['expected_page_ids']:
                raise ValueError(f'{case["id"]}: supported case needs a document answer and source pages.')
            if case['selection'] != case['group'] or any(pages[p] != case['group'] for p in case['expected_page_ids']):
                raise ValueError(f'{case["id"]}: selection and source jurisdiction must match.')
        elif case['expected_status'] not in ('not_established', 'clarification_required', 'unsupported_jurisdiction'):
            raise ValueError('Negative cases need an abstention or clarification expectation.')
    return cases


def snapshot():
    paths = [Path(p) for p in ('EV Policy Assistant.ipynb', 'data/source_manifest.json',
             'data/retrieval_rules.json', 'uv.lock', 'run.py', 'evaluate.py')]
    paths += sorted(Path('data/processed').glob('*/*.jsonl'))
    paths += sorted(Path('data/ocr').glob('*/review.json'))
    return {str(p): file_hash(p) for p in paths}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--freeze', action='store_true')
    mode.add_argument('--batch', type=int, choices=(1, 2))
    args = parser.parse_args()
    data = json.loads(CASE_FILE.read_text())
    pages = {r['metadata']['page_id']: r['metadata']['state']
             for p in Path('data/processed').glob('*/pages.jsonl')
             for line in p.read_text().splitlines() for r in [json.loads(line)]}
    sources = json.loads(Path('data/source_manifest.json').read_text())['sources']
    cases = validate_cases(data, pages, sources)
    if args.freeze:
        frozen = {'frozen_at_utc': datetime.now(timezone.utc).isoformat(),
                  'team_cases_sha256': file_hash(CASE_FILE), 'artifacts': snapshot(), 'cases': cases}
        with FROZEN_FILE.open('x') as f:
            json.dump(frozen, f, ensure_ascii=False, indent=2)
        print('Frozen 24 independently prepared cases. No model calls made.')
        return
    frozen = json.loads(FROZEN_FILE.read_text())
    if frozen['team_cases_sha256'] != file_hash(CASE_FILE) or frozen['artifacts'] != snapshot():
        raise ValueError('Cases or implementation changed after freezing; retain old results and review a new version.')
    output = Path(f'evaluation/batch_{args.batch}.json')
    report = json.loads(output.read_text()) if output.exists() else {
        'frozen_sha256': file_hash(FROZEN_FILE), 'batch': args.batch,
        'scope': 'Actual responses; retrieval, answer and citation grades require team review.', 'observations': []}
    if report['frozen_sha256'] != file_hash(FROZEN_FILE):
        raise ValueError('Existing observations belong to a different frozen set.')
    stage = load_cells(DEFINITION_CELLS)
    ready = stage['start_policy_assistant']()
    if ready['status'] != 'ready':
        raise RuntimeError(ready['answer'])
    original = stage['retrieve_policy']
    retrieval = []

    def observed_retrieval(*args, **kwargs):
        result = original(*args, **kwargs)
        retrieval.append({'status': result['status'], 'seed_chunk_ids': result.get('seed_chunk_ids', []),
            'context_page_ids': [d.metadata['page_id'] for d in result.get('context_docs', [])]})
        return result

    stage['retrieve_policy'] = observed_retrieval
    completed = {o['case_id'] for o in report['observations']}
    selected = cases[(args.batch - 1) * 12:args.batch * 12]
    for case in selected:
        if case['id'] in completed:
            continue
        if report['observations']:
            time.sleep(60)
        retrieval.clear()
        result = stage['ask_policy'](case['selection'], case['question'])
        report['observations'].append({'case_id': case['id'],
            'observed_at_utc': datetime.now(timezone.utc).isoformat(), 'result': result,
            'retrieval': list(retrieval), 'status_matches': result['status'] == case['expected_status'],
            'team_grades': {'retrieval_correct': None, 'answer_correct': None, 'citation_correct': None,
                            'reviewer': None, 'notes': ''}})
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
        print(case['id'], result['status'], flush=True)
        if result['status'] in ('rate_limited', 'authentication_error', 'configuration_error', 'model_unavailable'):
            print('Stopped after recorded service failure. Retain this observation before a separate retry.')
            break


if __name__ == '__main__':
    try:
        main()
    except (ValueError, FileNotFoundError, FileExistsError) as error:
        raise SystemExit(str(error))
