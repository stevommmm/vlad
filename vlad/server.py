from . import validators
from . import DockerRequest
from aiohttp import web
import asyncio

def _whitelisted_route(uri):
    return uri.path in [
        '/_ping',
        '/v1.39/nodes',
        '/v1.39/tasks',
        '/v1.39/info',
        '/v1.39/version',
    ]


async def plugin_activate(request: web.Request):
    return web.json_response({'Implements': ['authz']})


async def pre_docker(request: web.Request):
    '''This authorize request method is called before the Docker daemon processes the client request.'''
    data = await request.json()
    req = DockerRequest(data)

    # We'll only deal with TLS enabled requests
    if not req.is_tls_auth or _whitelisted_route(req.req_uri):
        return web.json_response({'Allow': True})

    print(req)
    try:
        tasks = []
        for m in [x for x in dir(validators) if not x.startswith('__')]:
            tasks.append(getattr(validators, m).validate_request(req))

        results = await asyncio.gather(*tasks)
        print(results)

        # If any validator explicitly allows this pass it on
        if any(x is True for x in results):
            return web.json_response({'Allow': True})

        # Check for validator responses of str types indicating a reason for deny
        for response in results:
            if response:
                return web.json_response({'Allow': False, 'Msg': response})

    # For some reason someone has a problem, deny the request
    except Exception as e:
        return web.json_response({'Allow': False, 'Msg': e.message})

    # If none of the validators have given us a green light fail the request
    return web.json_response({'Allow': False})


async def post_docker(request: web.Request):
    '''This authorize response method is called before the response is returned from Docker daemon to the client.'''
    data = await request.json()
    req = DockerRequest(data)

    # We'll only deal with TLS enabled requests
    if not req.is_tls_auth or _whitelisted_route(req.req_uri):
        return web.json_response({'Allow': True})

    # print(req)
    return web.json_response({'Allow': True})


def make_app():
    app = web.Application()
    app.router.add_post("/Plugin.Activate", plugin_activate)
    app.router.add_post("/AuthZPlugin.AuthZReq", pre_docker)
    app.router.add_post("/AuthZPlugin.AuthZRes", post_docker)

    return app
