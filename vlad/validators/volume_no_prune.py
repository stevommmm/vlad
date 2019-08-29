async def validate_request(req):
    '''explicit block `docker volume prune`'''
    if req.req_method == 'POST' and req.req_target == '/volumes/prune':
        return 'You cannot globally prune volumes.'
