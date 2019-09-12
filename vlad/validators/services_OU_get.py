# handles: /services/{id}


async def validate_request(req):
    '''Allow inspecting/logs services in the OU prefix'''
    if req.req_method == 'GET' and req.req_target.startswith(req.OU_svc_prefix):
        return True
