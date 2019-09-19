# handles: /configs/{id}:delete


async def validate_request(req):
    '''Allow inspecting configs within the OU'''
    url_parts = req.req_target.split('/')
    if (
        req.req_method == 'DELETE'
        and len(url_parts) == 3
        and url_parts[0] == ''
        and url_parts[1] == 'configs'
    ):
        if url_parts[2].startswith(req.OU_prefix):
            return True

        # Check ID based lookups
        r_conf = await req.resolve_config(url_parts[2])
        if r_conf and r_conf.startswith(req.OU_prefix):
            return True

        return 'That config is outside your OU prefix.'
