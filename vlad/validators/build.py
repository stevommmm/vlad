# handles: /build:post
# handles: /build/prune:post


async def validate_request(req):
    '''Disable image building over TLS'''
    if req.req_target.startswith('/build'):
        return 'You cannot build images over this connection.'
