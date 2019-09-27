# handles: /tasks/{id}:get

from vlad.validators import handles


@handles.get('tasks', '*')
async def validate_request(req):
    '''Allow task query but deny on response below'''
    return True


@handles.get('tasks', '*')
async def validate_response(res):
    '''Restrict task inspection to service/network/etc names'''
    if not res.res_body:
        return

    # @todo
    print(res.res_body)

    # Check ServiceID in task for allowing OU service log lookups
    if 'ServiceID' in res.res_body:
        r_svc = await res.resolve_service(res.res_body['ServiceID'])
        if r_svc and r_svc.startswith(res.OU_prefix):
            return

    return f'That task is outside your OU prefix. {res.OU_prefix}'
