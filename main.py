#!/usr/bin/env python3
from aiohttp import web
import base64
import asyncio
import logging
import json
from multidict import MultiDict
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from pprint import pprint as pp
import os

logging.basicConfig(level=logging.DEBUG)

def _load_b64_certificate(b64s: str):
    rcert = base64.b64decode(b64s)
    return x509.load_pem_x509_certificate(rcert, default_backend())


def _subject_to_dict(subject):
    attrs = MultiDict()
    for x in subject.rdns:
        for r in x:
            attrs[r.oid._name] = r.value
    return attrs


def _decode_request(data):
    if 'ResponseBody' in data:
        data['ResponseBody'] = json.loads(base64.b64decode(data['ResponseBody']))
    if 'RequestPeerCertificates' in data:
        data['RequestPeerCertificates'] = [_subject_to_dict(_load_b64_certificate(x).subject) for x in data['RequestPeerCertificates']]


async def plugin_activate(request):
    return web.json_response({'Implements': ['authz']})


async def pre_docker(request):
    '''This authorize request method is called before the Docker daemon processes the client request.'''
    data = await request.json()

    # We'll only deal with TLS enabled requests
    if not 'UserAuthNMethod' in data or not data['UserAuthNMethod'] == 'TLS':
        web.json_response({'Allow': True})

    _decode_request(data)

    pp(data)
    return web.json_response({'Allow': True})


async def post_docker(request):
    '''This authorize response method is called before the response is returned from Docker daemon to the client.'''
    data = await request.json()

    # We'll only deal with TLS enabled requests
    if not 'UserAuthNMethod' in data or not data['UserAuthNMethod'] == 'TLS':
        web.json_response({'Allow': True})


    _decode_request(data)

    pp(data)
    return web.json_response({'Allow': True})


def make_app():
    app = web.Application()
    app.router.add_post("/Plugin.Activate", plugin_activate)
    app.router.add_post("/AuthZPlugin.AuthZReq", pre_docker)
    app.router.add_post("/AuthZPlugin.AuthZRes", post_docker)

    return app


async def serve(app):
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.UnixSite(runner, path='/run/docker/plugins/docking.sock')
    await site.start()
    try:
        while True:
            await asyncio.sleep(3600)  # sleep forever by 1 hour intervals
    except KeyboardInterrupt:
        print("Got CTRL+C, shutting down...")
    except Exception as e:
        print(e)
    finally:
        await runner.cleanup()
        os.unlink('/run/docker/plugins/docking.sock')


if __name__ == '__main__':
    app = make_app()
    asyncio.run(serve(app))
