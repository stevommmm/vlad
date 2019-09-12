# handles: /version

async def validate_request(req):
    '''Allow version requests'''
    if req.req_method == 'GET' and req.req_target == '/version':
        return True
