# handles: /services/{id}/logs:get

from vlad.validators import handles


@handles.get('services', '*', 'logs')
async def validate_request(req):
    '''Allow reading OU specific service logs'''
    url_parts = req.req_target.split('/')
    if url_parts[2].startswith(req.OU_prefix):
        return True

    # Resolve ID based service updates
    r_svc = await req.resolve_service(url_parts[2])
    if r_svc and r_svc.startswith(req.OU_prefix):
        return True

    return f'That service is outside your OU prefix. ({req.OU_prefix})'
