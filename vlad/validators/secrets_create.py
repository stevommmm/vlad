# handles: /secrets/create:post

from vlad.validators import handles


@handles.post('secrets', 'create')
async def validate_request(req):
    '''Allow creating secrets within the OU'''
    if not req.req_body['Name'].startswith(req.OU_prefix):
        return f'That secret is outside your OU prefix. ({req.OU_prefix})'
    return True
