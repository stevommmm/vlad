# handles: /services/{id}/update:post


def check_task(req):
    if not req.req_body['Name'].startswith(req.OU_prefix):
        return 'That service is outside your OU prefix.'
    # Explicitly check for bind mounts because no thx
    if req.req_body and 'TaskTemplate' in req.req_body:
        if 'ContainerSpec' in req.req_body['TaskTemplate']:
            if 'Mounts' in req.req_body['TaskTemplate']['ContainerSpec']:
                for mount in req.req_body['TaskTemplate']['ContainerSpec'][
                    'Mounts'
                ]:
                    if mount.get('Type', '').lower() == 'bind':
                        return 'You cannot bind mount.'
    # If the req is in the OU and has no bind mounts we're good
    return True


async def validate_request(req):
    '''Allow updating of services in our OU without binds'''
    url_parts = req.req_target.split('/')
    if (
        req.req_method == 'POST'
        and len(url_parts) == 4
        and url_parts[0] == ''
        and url_parts[1] == 'services'
        # url_parts[2] is the service name checked below...
        and url_parts[3] == 'update'
    ):
        if url_parts[2].startswith(req.OU_prefix):
            return check_task(req)

        # Resolve ID based service updates
        r_svc = await req.resolve_service(url_parts[2])
        if r_svc and r_svc.startswith(req.OU_prefix):
            return check_task(req)

        return 'That service is outside your OU prefix.'
