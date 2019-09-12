# handles: /networks/{id}:delete


async def validate_request(req):
    '''Allow deleting networks in the OU prefix'''
    if req.req_method == 'DELETE' and req.req_target.startswith(req.OU_net_prefix):
        return True
