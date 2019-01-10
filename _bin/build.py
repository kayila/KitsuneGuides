#!/usr/bin/env python3

import json
from pathlib import Path
import sys

def load_json_file(path):
    with open(path) as fp:
        return json.load(fp)

def dump_json_file(path, obj):
    with open(path, 'w') as fp:
        return fp.write(json.dumps(obj, indent="  "))

root_dir = Path(__file__).resolve().parent.parent

api = load_json_file(Path(root_dir, 'api', 'api.json.template'))
guide_files = Path('.').glob("**/data.json")

api['guides'] = [load_json_file(f) for f in guide_files]

if "--stdout" in sys.argv:
    print(api_json)
else:
    api_json_file = Path(root_dir, "api", "api.json")
    dump_json_file(api_json_file, api)
