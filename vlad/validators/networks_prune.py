# handles: /networks/prune:post


async def validate_request(req):
    '''Allow indexing networks'''
    if req.req_method == 'POST' and req.req_target == '/networks/prune':
        return 'You cannot globally prune networks.'
