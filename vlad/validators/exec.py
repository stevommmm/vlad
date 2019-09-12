# handles: /exec/{id}/start
# handles: /exec/{id}/resize
# handles: /exec/{id}/json

# Also check containers.py for /containers/{id}/exec entrypoint


async def validate_request(req):
    '''Deny exec interactions over TLS'''
    if req.req_target.startswith('/exec/'):
        return 'You cannot interact with host containers over this connection.'
