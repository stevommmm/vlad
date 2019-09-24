# handles: /volumes:get

from vlad.validators import handles


@handles.get('volumes')
async def validate_request(req):
    '''Allow indexing volumes'''
    return True
