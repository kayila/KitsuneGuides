#!/usr/bin/env python3

import json
from pathlib import Path
import sys

def load_json_file(path):
    return json.loads(Path(path).read_text())

def dump_json_file(path, obj):
    return Path(path).write_text(json.dumps(obj))

api = load_json_file('./api/api.json.template')
guide_files = Path('.').glob("**/data.json")

api['guides'] = [load_json_file(f) for f in guide_files]

api_json = json.dumps(api, indent="  ")

if "--stdout" in sys.argv:
    print(api_json)
else:
    root_dir = Path(__file__).resolve().parent.parent
    output_file = Path(root_dir, "api", "api.json")
    output_file.write_text(api_json)
