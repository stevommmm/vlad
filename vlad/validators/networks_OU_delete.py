# handles: /networks/{id}:delete


async def validate_request(req):
    '''Allow deleting networks in the OU prefix'''
    url_parts = req.req_target.split('/')
    if (
        req.req_method == 'DELETE'
        and len(url_parts) == 3
        and url_parts[0] == ''
        and url_parts[1] == 'networks'
    ):
        if url_parts[2].startswith(req.OU_prefix):
            return True

        # Check ID based lookups
        r_net = await req.resolve_network(url_parts[2])
        if r_net and r_net.startswith(req.OU_prefix):
            return True

        return 'That network is outside your OU prefix.'
