#!/usr/bin/env python3

import json
from pathlib import Path
import shutil
import sys

def copy(src, dest):
    try:
        if Path(src).is_dir():
            shutil.copytree(src, dest)
        else:
            shutil.copy(src, dest)
    except OSError as e:
        print('Error: {}'.format(e))
        exit(1)

def load_json_file(path):
    with open(str(path)) as fp:
        return json.load(fp)

def dump_json_file(path, obj):
    with open(str(path), 'w') as fp:
        return fp.write(json.dumps(obj, indent='  '))

def generate_api_json(root_dir, dest_dir):
    # Load base api.json data.
    api = load_json_file(Path(root_dir, '_templates', 'api.json.template'))

    # Populate guide list from */data.json.
    guide_files = Path('.').glob('**/data.json')
    api['guides'] = [load_json_file(f) for f in guide_files]

    # Create _site/api/
    Path(dest_dir, 'api').mkdir(exist_ok=True)

    # Create _site/api/api.json
    api_json_file = Path(dest_dir, 'api', 'api.json')
    dump_json_file(api_json_file, api)


def copy_source_files(root_dir, dest_dir):
    assert root_dir != dest_dir

    # Remove old generated files.
    if Path(dest_dir).exists():
        shutil.rmtree(dest_dir)
    # Re-create dest_dir.
    Path(dest_dir).mkdir()

    sources = root_dir.glob('*')
    sources = map(lambda x: x.relative_to(root_dir), sources)
    sources = filter(lambda x: str(x)[0] != '.' and str(x)[0] != '_', sources)

    for source in sources:
        source = str(source)
        dest = str(Path(dest_dir, source))
        print('{} => {}'.format(source, Path(dest).relative_to(root_dir)))
        copy(source, dest)


root_dir = Path(__file__).resolve().parent.parent
dest_dir = Path(root_dir, '_site')

copy_source_files(root_dir, dest_dir)
generate_api_json(root_dir, dest_dir)
