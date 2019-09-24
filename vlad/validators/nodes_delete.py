# handles: /nodes/{id}:delete

from vlad.validators import handles


@handles.delete('nodes', '*')
async def validate_request(req):
    '''Allow indexing nodes in the cluster'''
    return 'You cannot interact with nodes over TLS.'
