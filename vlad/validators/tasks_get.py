# handles: /tasks/{id}:get


async def validate_request(req):
    '''Allow task query but deny on response below'''
    url_parts = req.req_target.split('/')
    if (
        req.req_method == 'GET'
        and len(url_parts) == 3
        and url_parts[0] == ''
        and url_parts[1] == 'tasks'
    ):
        return True


async def validate_response(res):
    '''Restrict task inspection to service/network/etc names'''
    if await validate_request(res):
        if not res.res_body:
            return

        # @todo
        print(res.res_body)

        # Check ServiceID in task for allowing OU service log lookups
        if 'ServiceID' in res.res_body:
            r_svc = await res.resolve_service(res.res_body['ServiceID'])
            if r_svc and r_svc.startswith(res.OU_prefix):
                return

        return 'This task is outside your OU.'
