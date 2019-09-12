# handles: /nodes

async def validate_request(req):
    '''Allow indexing nodes in the cluster'''
    if req.req_method == 'GET' and req.req_target == '/nodes':
        return True
