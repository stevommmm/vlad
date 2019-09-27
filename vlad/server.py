from . import validators
from .validators import import_validators
from . import DockerRequest, DockerResponse
from aiohttp import web
import asyncio
import logging
import uuid

logger = logging.getLogger(__name__)


async def plugin_activate(request: web.Request):
    return web.json_response({'Implements': ['authz']})


async def pre_docker(request: web.Request):
    '''This authorize request method is called before the Docker daemon processes the client request.'''
    data = await request.json()
    async with DockerRequest(data) as req:
        # We'll only deal with TLS enabled requests
        if not req.is_tls_auth:
            return web.json_response({'Allow': True})

        logger.debug(req)
        try:
            tasks = []
            for func in request.app['validators']['request']:
                tasks.append(func(req))

            results = await asyncio.gather(*tasks)

            # If any validator explicitly allows this pass it on
            if any(x is True for x in results):
                return web.json_response({'Allow': True})

            # Check for validator responses of str types indicating a reason for deny
            for response in results:
                if response:
                    return web.json_response({'Allow': False, 'Msg': response})

        # For some reason someone has a problem, deny the request
        # @todo dont expose internal error messages to clients
        except Exception as e:
            uu = uuid.uuid4().hex
            logger.warning("%s catch %r", uu, e)
            return web.json_response(
                {
                    'Allow': False,
                    'Msg': f"Server error, contact your administrator with code '{uu}'.",
                }
            )

    # If none of the validators have given us a green light fail the request
    # @todo add meaningful contact your admin blurb
    return web.json_response(
        {
            'Allow': False,
            'Msg': 'That action is not specifically allowed. Contact your administrator.',
        }
    )


async def post_docker(request: web.Request):
    '''This authorize response method is called before the response is returned from Docker daemon to the client.'''
    data = await request.json()
    async with DockerResponse(data) as res:
        # We'll only deal with TLS enabled requests
        if not res.is_tls_auth:
            return web.json_response({'Allow': True})

        logger.debug(res)
        try:
            tasks = []
            for func in request.app['validators']['response']:
                tasks.append(func(res))

            results = await asyncio.gather(*tasks)

            # for responses we only deny if someone explicitly says so
            for response in results:
                if response:
                    return web.json_response({'Allow': False, 'Msg': response})

        except Exception as e:
            return web.json_response({'Allow': False, 'Msg': repr(e)})

    return web.json_response({'Allow': True})


def _fetch_validators():
    _req = []
    _res = []
    import_validators()
    for m in [
        getattr(validators, x) for x in dir(validators) if not x.startswith('__')
    ]:
        if hasattr(m, 'validate_request'):
            _req.append(m.validate_request)
        if hasattr(m, 'validate_response'):
            _res.append(m.validate_response)

    logger.info("Found %d request, %d response validators...", len(_req), len(_res))
    return {'request': _req, 'response': _res}


def make_app():
    app = web.Application()
    app['validators'] = _fetch_validators()
    app.router.add_post("/Plugin.Activate", plugin_activate)
    app.router.add_post("/AuthZPlugin.AuthZReq", pre_docker)
    app.router.add_post("/AuthZPlugin.AuthZRes", post_docker)

    return app
