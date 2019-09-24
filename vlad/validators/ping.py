# handles: /_ping:get
# handles: /_ping:head

from vlad.validators import handles


@handles.many(['HEAD', '_ping'], ['GET', '_ping'])
async def validate_request(req):
    '''Allow ping activity'''
    return True
