# handles: /configs:get
from vlad.validators import handles


@handles.get('configs')
async def validate_request(req):
    '''Allow indexing configs'''
    return True
