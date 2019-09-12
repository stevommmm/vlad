# handles: /volumes

async def validate_request(req):
    '''Allow indexing volumes'''
    if req.req_method == 'GET' and req.req_target == '/volumes':
        return True
