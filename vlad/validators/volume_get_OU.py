async def validate_request(req):
    '''Allow inspecting volumes in the OU prefix'''
    if req.req_method == 'GET' and req.req_target.startswith(req.OU_vol_prefix):
        return True
