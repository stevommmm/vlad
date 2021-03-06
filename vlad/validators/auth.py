# handles: /auth:post
from vlad.validators import handles


@handles.post('auth')
async def validate_request(req):
    '''Don't auth the remote daemon'''
    return 'You cannot login over a TLS connection. Use --with-registry-auth when deploying stacks'
