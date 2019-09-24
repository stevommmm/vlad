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

from vlad.validators import handles


@handles.many(
    ['GET', 'plugins'],
    ['GET', 'plugins', 'privileges'],
    ['POST', 'plugins', 'pull'],
    ['GET', 'plugins', '*', 'json'],
    ['DELETE', 'plugins', '*'],
    ['POST', 'plugins', '*', 'enable'],
    ['POST', 'plugins', '*', 'disable'],
    ['POST', 'plugins', '*', 'upgrade'],
    ['POST', 'plugins', 'create'],
    ['POST', 'plugins', '*', 'push'],
    ['POST', 'plugins', '*', 'set'],
)
async def validate_request(req):
    '''Deny all plugin interaction over TLS'''
    return 'You cannot interact with swarm over this connection.'
