# handles: /nodes:get

from vlad.validators import handles


@handles.get('nodes')
async def validate_request(req):
    '''Allow indexing nodes in the cluster'''
    return True
