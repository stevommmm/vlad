# handles: /services:get

from vlad.validators import handles


@handles.get('services')
async def validate_request(req):
    '''Allow indexing services'''
    return True
