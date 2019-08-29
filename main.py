#!/usr/bin/env python3
from aiohttp import web
import asyncio
import logging
import os

from vlad import make_app

logging.basicConfig(level=logging.DEBUG)


async def serve(app):
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.UnixSite(runner, path='/run/docker/plugins/vlad.sock')
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
        os.unlink('/run/docker/plugins/vlad.sock')


if __name__ == '__main__':
    app = make_app()
    asyncio.run(serve(app))
