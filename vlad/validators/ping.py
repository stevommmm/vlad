# handles: /_ping:get


async def validate_request(req):
    '''Allow ping activity'''
    if req.req_method == 'GET' and req.req_target == '/_ping':
        return True
