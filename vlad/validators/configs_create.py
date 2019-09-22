# handles: /configs/create:post

from vlad.validators import handles


@handles('POST', '', 'configs', 'create')
async def validate_request(req):
    '''Allow creating configs within the OU'''
    if req.req_body['Name'].startswith(req.OU_prefix):
        return True

    return 'That secret is outside your OU prefix.'
