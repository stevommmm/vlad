# handles: /exec/{id}/start:post
# handles: /exec/{id}/resize:post
# handles: /exec/{id}/json:get

# Also check containers.py for /containers/{id}/exec entrypoint


async def validate_request(req):
    '''Deny exec interactions over TLS'''
    if req.req_target.startswith('/exec/'):
        return 'You cannot interact with host containers over this connection.'
