# handles: /services/{id}:delete

from vlad.validators import handles


@handles.delete('services', '*')
async def validate_request(req):
    '''Allow deleting services in the OU prefix'''
    url_parts = req.req_target.split('/')
    if url_parts[2].startswith(req.OU_prefix):
        return True

    # Check ID based lookups
    r_svc = await req.resolve_service(url_parts[2])
    if r_svc and r_svc.startswith(req.OU_prefix):
        return True

    return 'That service is outside your OU prefix.'
