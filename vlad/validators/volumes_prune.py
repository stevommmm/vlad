# handles: /volumes/prune:post

from vlad.validators import handles


@handles.post('volumes', 'prune')
async def validate_request(req):
    '''explicit block `docker volume prune`'''
    return 'You cannot globally prune volumes.'
