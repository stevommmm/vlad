# handles: /swarm:get
# handles: /swarm/init:post
# handles: /swarm/join:post
# handles: /swarm/leave:post
# handles: /swarm/update:post
# handles: /swarm/unlockkey:get
# handles: /swarm/unlock:post

from vlad.validators import handles


@handles.many(
    ['GET', 'swarm'],
    ['POST', 'swarm', 'init'],
    ['POST', 'swarm', 'join'],
    ['POST', 'swarm', 'leave'],
    ['POST', 'swarm', 'update'],
    ['GET', 'swarm', 'unlockkey'],
    ['POST', 'swarm', 'unlock'],
)
async def validate_request(req):
    '''Deny all swarm modifications over TLS'''
    return 'You cannot interact with swarm over this connection.'
