# handles: /tasks

async def validate_request(req):
    '''Allow indexing tasks'''
    if req.req_method == 'GET' and req.req_target == '/tasks':
        return True
