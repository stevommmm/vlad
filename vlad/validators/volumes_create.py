# handles: /volumes/create:post

from vlad.validators import handles


@handles.post('volumes', 'create')
async def validate_request(req):
    '''Allow creation of volumes in our OU'''
    if not req.req_body['Name'].startswith(req.OU_prefix):
        return 'Cannot create volumes outside your OU prefix.'
    if req.req_body['DriverOpts'].get('device', '').startswith('/'):
        return 'You cannot bind mount.'

    return True
