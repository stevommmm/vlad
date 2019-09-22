import functools
from pathlib import Path
import importlib


def handles(method: str, *args: str):
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(request):
            url_parts = request.req_target.split('/')
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
