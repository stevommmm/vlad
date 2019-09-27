# handles: /build:post
# handles: /build/prune:post

from vlad.validators import handles


@handles.many(['POST', 'build'], ['POST', 'build', 'prune'])
async def validate_request(req):
    '''Disable image building over TLS'''
    return 'You cannot build images over a TLS connection.'
