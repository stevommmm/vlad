# handles: /nodes/{id}

async def validate_request(req):
    '''Allow indexing nodes in the cluster'''
    if req.req_method == 'DELETE' and req.req_target.startswith('/nodes'):
        return 'You cannot interact with nodes over TLS.'
