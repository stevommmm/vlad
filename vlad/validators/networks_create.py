# handles: /networks/create:post

from vlad.validators import handles


@handles.post('networks', 'create')
async def validate_request(req):
    '''Allow creation of networks in our OU'''
    if not req.req_body['Name'].startswith(req.OU_prefix):
        return 'That network is outside your OU prefix.'
    return True
