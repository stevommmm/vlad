# handles: /nodes/{id}/update:post

from vlad.validators import handles


@handles.post('nodes', '*', 'update')
async def validate_request(req):
    '''Prevent node updates over TLS'''
    return 'You cannot interact with nodes over a TLS connection.'
