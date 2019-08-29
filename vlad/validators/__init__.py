from pathlib import Path
import importlib

for mod in Path(__file__).parent.iterdir():
    if mod.suffix == '.py' and mod.stem != '__init__':
        importlib.import_module(f'vlad.validators.{mod.stem}', mod.stem)

del Path, mod, importlib
