# handles: /commit:post
from vlad.validators import handles


@handles.post('commit')
async def validate_request(req):
    '''Deny image interaction over tls'''
    return 'You cannot interact with images over TLS.'
