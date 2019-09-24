# handles: /version:get

from vlad.validators import handles


@handles.get('version')
async def validate_request(req):
    '''Allow version requests'''
    return True
