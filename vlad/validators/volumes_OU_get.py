# handles: /volumes/{name}:get

from vlad.validators import handles


@handles.get('volumes', '*')
async def validate_request(req):
    '''Allow inspecting volumes in the OU prefix'''
    url_parts = req.req_target.split('/')
    if url_parts[2].startswith(req.OU_prefix):
        return True

    # Check ID based lookups
    r_vol = await req.resolve_volume(url_parts[2])
    if r_vol and r_vol.startswith(req.OU_prefix):
        return True

    return 'That volume is outside your OU prefix.'
