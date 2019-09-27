# handles: /volumes/{name}:delete

from vlad.validators import handles


@handles.delete('volumes', '*')
async def validate_request(req):
    '''Allow deleting volumes in the OU prefix'''
    url_parts = req.req_target.split('/')
    if url_parts[2].startswith(req.OU_prefix):
        return True

    # Check ID based lookups
    r_vol = await req.resolve_volume(url_parts[2])
    if r_vol and r_vol.startswith(req.OU_prefix):
        return True

    return f'That volume is outside your OU prefix. ({req.OU_prefix})'
