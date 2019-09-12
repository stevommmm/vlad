# handles: /volumes/{name}:delete


async def validate_request(req):
    '''Allow deleting volumes in the OU prefix'''
    if req.req_method == 'DELETE' and req.req_target.startswith(req.OU_vol_prefix):
        return True
