# handles: /configs/create:post


async def validate_request(req):
    '''Allow creating configs within the OU'''
    if req.req_method == 'POST' and req.req_target == '/configs/create':
        if not req.req_body['Name'].startswith(req.OU_prefix):
            return 'That secret is outside your OU prefix.'
        return True
