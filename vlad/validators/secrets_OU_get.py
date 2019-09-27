# handles: /secrets/{id}:get

from vlad.validators import handles


@handles.get('secrets', '*')
async def validate_request(req):
    '''Allow inspecting secrets within the OU'''
    url_parts = req.req_target.split('/')
    if url_parts[2].startswith(req.OU_prefix):
        return True

    # Check ID based lookups
    r_sec = await req.resolve_secret(url_parts[2])
    if r_sec and r_sec.startswith(req.OU_prefix):
        return True

    return f'That secret is outside your OU prefix. ({req.OU_prefix})'
