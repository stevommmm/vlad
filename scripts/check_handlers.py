import ast
from pathlib import Path
import yaml
import urllib.request
import re

braces = re.compile(r'\{\w+\}')

known_paths = set()
handled_paths = set()

def walk_nodes_for_handlers(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.AsyncFunctionDef) and node.name == 'validate_request':
            if node.decorator_list:
                for dec in node.decorator_list:
                    if dec.func.attr == 'many':
                        for r in dec.args:
                            method = r.elts[0].s.lower()
                            url = '/' + '/'.join([x.s for x in r.elts[1:]])
                            yield ':'.join([method, url])
                    else:
                        method = dec.func.attr.lower()
                        url = '/' + '/'.join([x.s for x in dec.args])
                        yield ':'.join([method, url])

def walk_swagger():
    with urllib.request.urlopen('https://docs.docker.com/engine/api/v1.40/swagger.yaml') as f:
        spec = yaml.safe_load(f)
        for uri, methods in spec['paths'].items():
            uri = braces.sub('*', uri)
            for method in methods:
                yield ':'.join([method,uri])

if __name__ == '__main__':
    for _path in walk_swagger():
        known_paths.add(_path)

    print("\n### Handler Index:\n")
    for fn in Path('vlad/validators').iterdir():
        if not fn.is_file():
            continue
        tree = ast.parse(fn.read_text())
        for handler in walk_nodes_for_handlers(tree):
            handled_paths.add(handler)
            print(f"- [{handler}]({fn.as_posix()})")


    missing = known_paths.difference(handled_paths)
    if missing:
        print("\n### We are missing handlers for:\n")
        for x in missing:
            print(f" - {x}")
