# handles: /services/{id}:delete


async def validate_request(req):
    '''Allow deleting services in the OU prefix'''
    url_parts = req.req_target.split('/')
    if (
        req.req_method == 'DELETE'
        and len(url_parts) == 3
        and url_parts[0] == ''
        and url_parts[1] == 'services'
    ):
        if url_parts[2].startswith(req.OU_prefix):
            return True

        # Check ID based lookups
        r_svc = await req.resolve_service(url_parts[2])
        if r_svc and r_svc.startswith(req.OU_prefix):
            return True

        return 'That service is outside your OU prefix.'
