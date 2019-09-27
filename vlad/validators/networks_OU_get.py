# handles: /networks/{id}:get

from vlad.validators import handles


@handles.get('networks', '*')
async def validate_request(req):
    '''Allow inspecting networks in the OU prefix'''
    url_parts = req.req_target.split('/')
    if url_parts[2].startswith(req.OU_prefix):
        return True

    # Check ID based lookups
    r_net = await req.resolve_network(url_parts[2])
    if r_net and r_net.startswith(req.OU_prefix):
        return True

    return f'That network is outside your OU prefix. ({req.OU_prefix})'
