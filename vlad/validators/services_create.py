# handles: /services/create:post

from vlad.validators import handles


@handles.post('services', 'create')
async def validate_request(req):
    '''Allow creation of services in our OU without binds'''
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

    # If the req is in the OU and has no bind mounts we're good
    return True
