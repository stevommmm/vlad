# handles: /networks/create:post


async def validate_request(req):
    '''Allow creation of networks in our OU'''
    if req.req_method == 'POST' and req.req_target == '/networks/create':
        if not req.req_body['Name'].startswith(req.OU_prefix):
            return 'That network is outside your OU prefix.'
        return True
