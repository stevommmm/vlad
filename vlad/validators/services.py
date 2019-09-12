# handles: /services:get


async def validate_request(req):
    '''Allow indexing services'''
    if req.req_method == 'GET' and req.req_target == '/services':
        return True
