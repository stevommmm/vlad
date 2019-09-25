import ast
from pathlib import Path
import yaml
import urllib.request
import re

braces = re.compile(r'\{\w+\}')

known_paths = set()
handled_paths = set()

with urllib.request.urlopen('https://docs.docker.com/engine/api/v1.40/swagger.yaml') as f:
    spec = yaml.safe_load(f)
    for uri, methods in spec['paths'].items():
        uri = braces.sub('*', uri)
        for method in methods:
            known_paths.add(':'.join([method,uri]))


for fn in Path('vlad/validators').iterdir():
    if not fn.is_file():
        continue
    tree = ast.parse(fn.read_text())

    for node in ast.walk(tree):
        if isinstance(node, ast.AsyncFunctionDef) and node.name == 'validate_request':
            if node.decorator_list:
                for dec in node.decorator_list:
                    if dec.func.attr == 'many':
                        for r in dec.args:
                            method = r.elts[0].s.lower()
                            url = '/' + '/'.join([x.s for x in r.elts[1:]])
                            handled_paths.add(':'.join([method, url]))
                    else:
                        method = dec.func.attr.lower()
                        url = '/' + '/'.join([x.s for x in dec.args])
                        handled_paths.add(':'.join([method, url]))


missing = known_paths.difference(handled_paths)
if missing:
    print("We are missing handlers for:")
    print('\n'.join(missing))
