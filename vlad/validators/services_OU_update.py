# handles: /services/{id}/update:post


async def validate_request(req):
    '''Allow updating of services in our OU without binds'''
    url_parts = req.req_target.split('/')
    if (
        req.req_method == 'POST'
        and len(url_parts) == 4
        and url_parts[0] == ''
        and url_parts[1] == 'services'
        and url_parts[2].startswith(req.OU_prefix)
        and url_parts[3] == 'update'
    ):
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
