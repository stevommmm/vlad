# handles: /plugins
# handles: /plugins/privileges
# handles: /plugins/pull
# handles: /plugins/{name}/json
# handles: /plugins/{name}
# handles: /plugins/{name}/enable
# handles: /plugins/{name}/disable
# handles: /plugins/{name}/upgrade
# handles: /plugins/create
# handles: /plugins/{name}/push
# handles: /plugins/{name}/set


async def validate_request(req):
    '''Deny all plugin interaction over TLS'''
    if req.req_target.startswith('/plugins'):
        return 'You cannot interact with swarm over this connection.'
