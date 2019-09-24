# handles: /info:get

from vlad.validators import handles


@handles.get('info')
async def validate_request(req):
    '''Allow informational swarm requests'''
    return True
