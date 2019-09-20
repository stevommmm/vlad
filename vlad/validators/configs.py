# handles: /configs:get
from vlad.validators import handles

@handles('GET', '', 'configs')
async def validate_request(req):
    '''Allow indexing configs'''
    print(f"Passed handles decr for {req.req_target}")
    return True
