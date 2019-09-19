# handles: /volumes/{name}:delete


async def validate_request(req):
    '''Allow deleting volumes in the OU prefix'''
    url_parts = req.req_target.split('/')
    if (
        req.req_method == 'DELETE'
        and len(url_parts) == 3
        and url_parts[0] == ''
        and url_parts[1] == 'volumes'
    ):
        if url_parts[2].startswith(req.OU_prefix):
            return True

        # Check ID based lookups
        r_vol = await req.resolve_volume(url_parts[2])
        if r_vol and r_vol.startswith(req.OU_prefix):
            return True

        return 'That volume is outside your OU prefix.'
