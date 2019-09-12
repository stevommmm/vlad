# handles: /networks/{id}:get


async def validate_request(req):
    '''Allow inspecting networks in the OU prefix'''
    if req.req_method == 'GET' and req.req_target.startswith(req.OU_net_prefix):
        return True
