# handles: /nodes/{id}/update:post


async def validate_request(req):
    '''Allow indexing nodes in the cluster'''
    if (
        req.req_method == 'POST'
        and req.req_target.startswith('/nodes')
        and req.req_target.endswith('/update')
    ):
        return 'You cannot interact with nodes over TLS.'
