# handles: /configs/{id}/update:post

from vlad.validators import handles


@handles.post('configs', '*', 'update')
async def validate_request(req):
    '''Allow inspecting configs within the OU'''
    url_parts = req.req_target.split('/')
    if not req.req_body['Name'].startswith(req.OU_prefix):
        return 'That config is outside your OU prefix.'

    if url_parts[2].startswith(req.OU_prefix):
        return True

    # Check ID based lookups
    r_sec = await req.resolve_config(url_parts[2])
    if r_sec and r_sec.startswith(req.OU_prefix):
        return True

    return 'That config is outside your OU prefix.'
