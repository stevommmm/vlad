# handles: /secrets

async def validate_request(req):
    '''Allow indexing secrets'''
    if req.req_method == 'GET' and req.req_target == '/secrets':
        return True
