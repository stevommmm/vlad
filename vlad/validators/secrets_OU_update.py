# handles: /secrets/{id}/update:post

from vlad.validators import handles


@handles.post('secrets', '*', 'update')
async def validate_request(req):
    '''Allow updating secrets within the OU'''
    url_parts = req.req_target.split('/')
    if not req.req_body['Name'].startswith(req.OU_prefix):
        return f'That secret is outside your OU prefix. ({req.OU_prefix})'

    if url_parts[2].startswith(req.OU_prefix):
        return True

    # Check ID based lookups
    r_sec = await req.resolve_secret(url_parts[2])
    if r_sec and r_sec.startswith(req.OU_prefix):
        return True

    return f'That secret is outside your OU prefix. ({req.OU_prefix})'
