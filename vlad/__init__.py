from .request import DockerRequest
from .server import make_app
from . import validators

# make pyflakes happy
assert validators
assert DockerRequest
assert make_app
