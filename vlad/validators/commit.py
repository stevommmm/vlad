# handles: /commit:post


async def validate_request(req):
    '''Deny image interaction over tls'''
    if req.req_method == 'POST' and req.req_target == '/commit':
        return 'You cannot interact with images over TLS.'
