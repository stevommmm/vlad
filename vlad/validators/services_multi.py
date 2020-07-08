# handles: /services/create:post
# handles: /services/{id}/update:post

from vlad.validators import handles

async def check_task(req):
    if not req.req_body['Name'].startswith(req.OU_prefix):
        return f'That service is outside your OU prefix. {req.OU_prefix}'
    # Explicitly check for bind mounts because no thx
    if not req.opts['bind_mount'] and req.req_body and 'TaskTemplate' in req.req_body:
        if 'ContainerSpec' in req.req_body['TaskTemplate']:
            if 'Mounts' in req.req_body['TaskTemplate']['ContainerSpec']:
                for mount in req.req_body['TaskTemplate']['ContainerSpec']['Mounts']:
                    if mount.get('Type', '').lower() == 'bind':
                        return 'You cannot bind mount.'

    # Stop port bindings to maybe important ports
    if not req.opts['bind_ports'] and req.req_body and 'EndpointSpec' in req.req_body:
        if 'Ports' in req.req_body['EndpointSpec']:
            for port in req.req_body['EndpointSpec']['Ports']:
                if 'PublishedPort' in port:
                    if port['PublishedPort'] < 30000 or port['PublishedPort'] > 61000:
                        return 'You cannot publish ports below the ephemeral range.'

    if req.req_body and 'TaskTemplate' in req.req_body:
        if 'ContainerSpec' in req.req_body['TaskTemplate']:
            if 'Secrets' in req.req_body['TaskTemplate']['ContainerSpec']:
                for secret in req.req_body['TaskTemplate']['ContainerSpec']['Secrets']:
                    if not secret.get('SecretName', '').startswith(req.OU_prefix):
                        return 'You cannot bind another namespace secret.'
            if 'Configs' in req.req_body['TaskTemplate']['ContainerSpec']:
                for config in req.req_body['TaskTemplate']['ContainerSpec']['Configs']:
                    if not config.get('ConfigName', '').startswith(req.OU_prefix):
                        return 'You cannot bind another namespace config.'

    # If the req is in the OU and has no bind mounts we're good
    return True


@handles.post('services', '*', 'update')
async def validate_request_update(req):
    '''Allow updating of services in our OU without binds'''
    url_parts = req.req_target.split('/')
    if url_parts[2].startswith(req.OU_prefix):
        return await check_task(req)

    # Resolve ID based service updates
    r_svc = await req.resolve_service(url_parts[2])
    if r_svc and r_svc.startswith(req.OU_prefix):
        return await check_task(req)

    return f'That service is outside your OU prefix. {req.OU_prefix}'


@handles.post('services', 'create')
async def validate_request(req):
    '''Allow creation of services in our OU without binds'''
    return await check_task(req)
