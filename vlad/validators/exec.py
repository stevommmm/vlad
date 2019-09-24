# handles: /exec/{id}/start:post
# handles: /exec/{id}/resize:post
# handles: /exec/{id}/json:get

# Also check containers.py for /containers/{id}/exec entrypoint

from vlad.validators import handles


@handles.many(
    ['POST', 'exec', '*', 'start'],
    ['POST', 'exec', '*', 'resize'],
    ['GET', 'exec', '*', 'json'],
)
async def validate_request(req):
    '''Deny exec interactions over TLS'''
    return 'You cannot interact with host containers over this connection.'
