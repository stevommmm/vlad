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
from vlad.validators import handles


@handles.many(
    ['GET', 'images', 'json'],
    ['POST', 'images', 'create'],
    ['GET', 'images', '*', 'json'],
    ['GET', 'images', '*', 'history'],
    ['POST', 'images', '*', 'push'],
    ['POST', 'images', '*', 'tag'],
    ['DELETE', 'images', '*'],
    ['GET', 'images', 'search'],
    ['POST', 'images', 'prune'],
    ['GET', 'images', '*', 'get'],
    ['GET', 'images', 'get'],
    ['POST', 'images', 'load'],
)
async def validate_request(req):
    '''Deny image interaction over tls'''
    if req.req_target.startswith('/images/'):
        return 'You cannot interact with images over TLS.'
