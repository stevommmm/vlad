# handles: /swarm
# handles: /swarm/init
# handles: /swarm/join
# handles: /swarm/leave
# handles: /swarm/update
# handles: /swarm/unlockkey
# handles: /swarm/unlock

async def validate_request(req):
    '''Deny all swarm modifications over TLS'''
    if req.req_target.startswith('/swarm'):
        return 'You cannot interact with swarm over this connection.'
