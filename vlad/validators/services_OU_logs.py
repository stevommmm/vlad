# handles: /services/{id}/logs

async def validate_request(req):
    '''Allow updating of services in our OU without binds'''
    if (
        req.req_method == 'POST'
        and req.req_target.startswith(req.OU_svc_prefix)
        and req.req_target.endswith('/logs')
    ):
        return True
