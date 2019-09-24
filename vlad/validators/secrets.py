# handles: /secrets:get

from vlad.validators import handles


@handles.get('secrets')
async def validate_request(req):
    '''Allow indexing secrets'''
    return True
