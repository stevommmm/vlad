# handles: /auth:post


async def validate_request(req):
    '''Don't auth the remote daemon'''
    if req.req_method == 'post' and req.req_target == '/auth':
        return 'No login over TLS. Use --with-registry-auth when deploying stacks'
