from vlad.validators import handles


@handles.many(
    ['GET', 'distribution', '*', 'json'],
    ['GET', 'distribution', '*', '*', 'json'],
    ['GET', 'distribution', '*', '*', '*', 'json'],
)
async def validate_request(req):
    '''Allow upstream registry'''
    return True
