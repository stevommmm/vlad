# handles: /nodes/{id}:get


async def validate_request(req):
    '''Allow indexing nodes in the cluster'''
    if (
        req.req_method == 'GET'
        and req.req_target.startswith('/nodes')
        and not req.req_target.endswith('/update')
    ):
        return True
