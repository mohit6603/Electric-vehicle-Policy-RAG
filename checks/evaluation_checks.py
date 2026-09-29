"""Check evaluation gates using synthetic schema fixtures; no policy/model grading."""
import copy
import json
import sys
from datetime import date
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from evaluate import validate_cases


def run_checks():
    template = json.loads(Path('evaluation/team_cases.json').read_text())
    data = copy.deepcopy(template)
    data['source_review'] = {'completed': True, 'reviewer': 'schema fixture', 'reviewed_on': date.today().isoformat()}
    pages = {}
    for case in data['cases']:
        case.update(question='Synthetic schema fixture', expected_answer='Not policy evidence',
                    authored_by='schema fixture', verified_by='schema fixture', verified_on=date.today().isoformat())
        if case['group'] == 'negative':
            case.update(selection='Central', expected_status='not_established')
        else:
            page = case['id'] + ':p1'
            pages[page] = case['group']
            case['expected_page_ids'] = [page]
    accepted = [{'accepted_for_ingestion': True, 'team_verified': True}]
    assert len(validate_cases(data, pages, accepted)) == 24
    checks = ['complete_synthetic_schema_accepted']

    def reject(label, changed, sources=accepted):
        try:
            validate_cases(changed, pages, sources)
        except ValueError:
            checks.append(label)
        else:
            raise AssertionError(label)

    reject('empty_team_template_rejected', template)
    reject('unaccepted_sources_rejected', data, [{'accepted_for_ingestion': False, 'team_verified': False}])
    for label, field, value in [('missing_author', 'authored_by', ''), ('unknown_page', 'expected_page_ids', ['missing:p1']),
                                ('cross_jurisdiction', 'selection', 'Central'), ('wrong_status', 'expected_status', 'not_established')]:
        changed = copy.deepcopy(data)
        changed['cases'][0][field] = value
        reject(label, changed)
    changed = copy.deepcopy(data)
    changed['cases'][1]['id'] = changed['cases'][0]['id']
    reject('duplicate_ids_rejected', changed)
    changed = copy.deepcopy(data)
    changed['cases'].pop()
    reject('incomplete_case_set_rejected', changed)
    print('Evaluation gate checks passed:', len(checks))
    return checks


if __name__ == '__main__':
    run_checks()
