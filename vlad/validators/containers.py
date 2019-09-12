# handles: /containers/json
# handles: /containers/create
# handles: /containers/{id}/json
# handles: /containers/{id}/top
# handles: /containers/{id}/logs
# handles: /containers/{id}/changes
# handles: /containers/{id}/export
# handles: /containers/{id}/stats
# handles: /containers/{id}/resize
# handles: /containers/{id}/start
# handles: /containers/{id}/stop
# handles: /containers/{id}/restart
# handles: /containers/{id}/kill
# handles: /containers/{id}/update
# handles: /containers/{id}/rename
# handles: /containers/{id}/pause
# handles: /containers/{id}/unpause
# handles: /containers/{id}/attach
# handles: /containers/{id}/attach/ws
# handles: /containers/{id}/wait
# handles: /containers/{id}
# handles: /containers/{id}/archive
# handles: /containers/prune

# handles: /containers/{id}/exec


async def validate_request(req):
    '''Deny all host specific containers over TLS'''
    if req.req_target.startswith('/containers/'):
        return 'You cannot interact with host containers over this connection.'
