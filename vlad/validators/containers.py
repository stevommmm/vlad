# handles: /containers/json:get
# handles: /containers/create:post
# handles: /containers/{id}/json:get
# handles: /containers/{id}/top:get
# handles: /containers/{id}/logs:get
# handles: /containers/{id}/changes:get
# handles: /containers/{id}/export:get
# handles: /containers/{id}/stats:get
# handles: /containers/{id}/resize:post
# handles: /containers/{id}/start:post
# handles: /containers/{id}/stop:post
# handles: /containers/{id}/restart:post
# handles: /containers/{id}/kill:post
# handles: /containers/{id}/update:post
# handles: /containers/{id}/rename:post
# handles: /containers/{id}/pause:post
# handles: /containers/{id}/unpause:post
# handles: /containers/{id}/attach:post
# handles: /containers/{id}/attach/ws:get
# handles: /containers/{id}/wait:post
# handles: /containers/{id}:delete
# handles: /containers/{id}/archive:head
# handles: /containers/prune:post

# handles: /containers/{id}/exec:post


async def validate_request(req):
    '''Deny all host specific containers over TLS'''
    if req.req_target.startswith('/containers/'):
        return 'You cannot interact with host containers over this connection.'
