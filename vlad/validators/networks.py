# handles: /networks

async def validate_request(req):
    '''Allow indexing networks'''
    if req.req_method == 'GET' and req.req_target == '/networks':
        return True
