# handles: /info


async def validate_request(req):
    '''Allow informational swarm requests'''
    if req.req_method == 'GET' and req.req_target == '/info':
        return True
