# handles: /tasks:get

from vlad.validators import handles


@handles.get('tasks')
async def validate_request(req):
    '''Allow indexing tasks'''
    return True
