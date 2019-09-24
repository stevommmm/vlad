# handles: /networks/prune:post

from vlad.validators import handles


@handles.post('networks', 'prune')
async def validate_request(req):
    '''Allow indexing networks'''
    return 'You cannot globally prune networks.'
