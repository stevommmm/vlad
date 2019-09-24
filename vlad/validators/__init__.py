import functools
from pathlib import Path
import importlib
from typing import List


class handles:
    @staticmethod
    def get(*args):
        return handles.many(['GET', *args])

    @staticmethod
    def post(*args):
        return handles.many(['POST', *args])

    @staticmethod
    def delete(*args):
        return handles.many(['DELETE', *args])

    @staticmethod
    def head(*args):
        return handles.many(['HEAD', *args])

    @staticmethod
    def many(*routes: List[str]):
        def wrapper(func):
            @functools.wraps(func)
            async def wrapped(request):
                # split our url, ignore first / split
                url_parts = request.req_target.split('/')[1:]
                for route in routes:
                    # Copy our list as we mutate it
                    args = route.copy()
                    method = args.pop(0)
                    if (
                        request.req_method == method
                        and len(url_parts) == len(args)
                        and all(
                            (url_parts[x] == args[x] or args[x] == '*')
                            for x in range(len(args))
                        )
                    ):
                        return await func(request)

            return wrapped

        return wrapper


def import_validators():
    for mod in Path(__file__).parent.iterdir():
        if mod.suffix == '.py' and mod.stem != '__init__':
            importlib.import_module(f'vlad.validators.{mod.stem}', mod.stem)
