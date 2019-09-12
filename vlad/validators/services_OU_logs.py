# handles: /services/{id}/logs:get


async def validate_request(req):
    '''Allow reading OU specific service logs'''
    url_parts = req.req_target.split('/')
    if (
        req.req_method == 'GET'
        and len(url_parts) == 4
        and url_parts[0] == ''
        and url_parts[1] == 'services'
        and url_parts[2].startswith(req.OU_prefix)
        and url_parts[3] == 'logs'
    ):
        return True
