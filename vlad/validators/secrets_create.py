# handles: /secrets/create:post


async def validate_request(req):
    '''Allow creating secrets within the OU'''
    if req.req_method == 'POST' and req.req_target == '/secrets/create':
        if not req.req_body['Name'].startswith(req.OU_prefix):
            return 'That secret is outside your OU prefix.'
        return True
