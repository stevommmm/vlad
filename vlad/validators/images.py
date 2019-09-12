# handles: /images/json:get
# handles: /images/create:post
# handles: /images/{name}/json:get
# handles: /images/{name}/history:get
# handles: /images/{name}/push:post
# handles: /images/{name}/tag:post
# handles: /images/{name}:delete
# handles: /images/search:get
# handles: /images/prune:post
# handles: /images/{name}/get:get
# handles: /images/get:get
# handles: /images/load:post


async def validate_request(req):
    '''Deny image interaction over tls'''
    if req.req_target.startswith('/images/'):
        return 'You cannot interact with images over TLS.'
