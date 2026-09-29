"""Run the notebook implementation from the project root."""
import argparse
import json
from pathlib import Path

DEFINITION_CELLS = (
    'stage5-imports', 'stage5-index-functions', 'stage6-inputs', 'stage6-routing',
    'stage6-context', 'stage7-schema', 'stage7-prompt', 'stage7-citations',
    'stage7-answer', 'stage8-results', 'stage8-startup', 'stage8-ask',
)


def load_cells(names, stage=None):
    stage = {} if stage is None else stage
    notebook = json.loads(Path('EV Policy Assistant.ipynb').read_text())
    cells = {cell['id']: cell for cell in notebook['cells']}
    for name in names:
        exec(compile(''.join(cells[name]['source']), name, 'exec'), stage)
    return stage


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--build-index', action='store_true', help='Explicitly rebuild local embeddings.')
    mode.add_argument('--check', action='store_true', help='Check saved-index startup without calling Groq.')
    parser.add_argument('--port', type=int, default=7860)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error('Use a port between 1 and 65535.')
    if args.build_index:
        stage = load_cells(('stage5-imports', 'stage5-index-functions', 'stage5-inputs'))
        stage['rebuild_policy_index'](stage['index_documents'], stage['embeddings_model'], stage['embedding_info'])
        return
    stage = load_cells(DEFINITION_CELLS)
    if args.check:
        result = stage['start_policy_assistant']()
        print(result['answer'])
        if result['status'] != 'ready':
            raise SystemExit(1)
        print('Chunks:', stage['index_spec']['chunk_count'])
        print('Jurisdictions:', ', '.join(stage['retrieval_choices']))
        return
    load_cells(('stage9-callback', 'stage9-startup', 'stage9-interface'), stage)
    stage['demo'].launch(server_name='127.0.0.1', server_port=args.port, share=False,
                         show_error=False, show_api=False)


if __name__ == '__main__':
    main()
