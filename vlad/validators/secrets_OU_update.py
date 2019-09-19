# handles: /secrets/{id}/update:post


async def validate_request(req):
    '''Allow inspecting secrets within the OU'''
    url_parts = req.req_target.split('/')
    if (
        req.req_method == 'POST'
        and len(url_parts) == 4
        and url_parts[0] == ''
        and url_parts[1] == 'secrets'
        and url_parts[3] == 'update'
    ):
        if not req.req_body['Name'].startswith(req.OU_prefix):
            return 'That secret is outside your OU prefix.'

        if url_parts[2].startswith(req.OU_prefix):
            return True

        # Check ID based lookups
        r_sec = await req.resolve_secret(url_parts[2])
        if r_sec and r_sec.startswith(req.OU_prefix):
            return True

        return 'That secret is outside your OU prefix.'
