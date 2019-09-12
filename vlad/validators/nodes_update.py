# handles: /nodes/{id}/update:post


async def validate_request(req):
    '''Prevent node updates over TLS'''
    url_parts = req.req_target.split('/')
    if (
        req.req_method == 'POST'
        and len(url_parts) == 4
        and url_parts[0] == ''
        and url_parts[1] == 'nodes'
        and url_parts[3] == 'update'
    ):
        return 'You cannot interact with nodes over TLS.'
