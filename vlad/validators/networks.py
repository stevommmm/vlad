# handles: /networks:get

from vlad.validators import handles


@handles.get('networks')
async def validate_request(req):
    '''Allow indexing networks'''
    return True
