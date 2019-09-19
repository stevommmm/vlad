# handles: /services/{id}/logs:get


async def validate_request(req):
    '''Allow reading OU specific service logs'''
    url_parts = req.req_target.split('/')
    if (
        req.req_method == 'GET'
        and len(url_parts) == 4
        and url_parts[0] == ''
        and url_parts[1] == 'services'
        # url_parts[2] is the service name checked below...
        and url_parts[3] == 'logs'
    ):
        if url_parts[2].startswith(req.OU_prefix):
            return True

        # Resolve ID based service updates
        r_svc = await req.resolve_service(url_parts[2])
        if r_svc and r_svc.startswith(req.OU_prefix):
            return True

        return 'That service is outside your OU prefix.'
