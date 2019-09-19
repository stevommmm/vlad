#!/usr/bin/env python3
from aiohttp import web
import asyncio
import logging
import os
import socket

import vlad

# logging.basicConfig(level=logging.DEBUG)
vlad.logger.setLevel(logging.DEBUG)


async def serve(app):
    runner = web.AppRunner(app)
    await runner.setup()
    try:
        # Try and open up the unix socket passed to us from systemd
        site = web.SockSite(runner, socket.fromfd(3, socket.AF_UNIX, socket.SOCK_STREAM))
        await site.start()
        logging.info("Using systemd socket activation")
    except:
        # We must be running in some other setup - bind the socket ourselves
        site = web.UnixSite(runner, path='/run/docker/plugins/vlad.sock')
        await site.start()
        logging.info("Trying to open the plugin socket...")

    try:
        while True:
            await asyncio.sleep(3600)  # sleep forever by 1 hour intervals
    except KeyboardInterrupt:
        print("Got CTRL+C, shutting down...")
    except Exception as e:
        print(e)
    finally:
        await runner.cleanup()
        # If we created the unix socket, clean it up
        if isinstance(site, web.UnixSite):
            os.unlink('/run/docker/plugins/vlad.sock')


if __name__ == '__main__':
    app = vlad.make_app()
    asyncio.run(serve(app))
