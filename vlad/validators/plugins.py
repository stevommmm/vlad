# handles: /plugins:get
# handles: /plugins/privileges:get
# handles: /plugins/pull:post
# handles: /plugins/{name}/json:get
# handles: /plugins/{name}:delete
# handles: /plugins/{name}/enable:post
# handles: /plugins/{name}/disable:post
# handles: /plugins/{name}/upgrade:post
# handles: /plugins/create:post
# handles: /plugins/{name}/push:post
# handles: /plugins/{name}/set:post


async def validate_request(req):
    '''Deny all plugin interaction over TLS'''
    if req.req_target.startswith('/plugins'):
        return 'You cannot interact with swarm over this connection.'
