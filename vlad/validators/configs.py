# handles: /configs

async def validate_request(req):
    '''Allow indexing configs'''
    if req.req_method == 'GET' and req.req_target == '/configs':
        return True
