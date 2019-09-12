# handles: /volumes/create:post


async def validate_request(req):
    '''Allow creation of volumes in our OU'''
    if req.req_method == 'POST' and req.req_target == '/volumes/create':
        if not req.req_body['Name'].startswith(req.OU_prefix):
            return 'Cannot create volumes outside your OU prefix.'
        if req.req_body['DriverOpts'].get('device', '').startswith('/'):
            return 'You cannot bind mount.'

        return True
