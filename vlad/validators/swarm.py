# handles: /swarm:get
# handles: /swarm/init:post
# handles: /swarm/join:post
# handles: /swarm/leave:post
# handles: /swarm/update:post
# handles: /swarm/unlockkey:get
# handles: /swarm/unlock:post

async def validate_request(req):
    '''Deny all swarm modifications over TLS'''
    if req.req_target.startswith('/swarm'):
        return 'You cannot interact with swarm over this connection.'
