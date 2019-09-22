# handles: /configs/{id}:get

from vlad.validators import handles


@handles('GET', '', 'configs', '*')
async def validate_request(req):
    '''Allow inspecting configs within the OU'''
    url_parts = req.req_target.split('/')
    if url_parts[2].startswith(req.OU_prefix):
        return True

    # Check ID based lookups
    r_conf = await req.resolve_config(url_parts[2])
    if r_conf and r_conf.startswith(req.OU_prefix):
        return True

    return 'That config is outside your OU prefix.'
