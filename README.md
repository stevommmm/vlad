# Vlad *the validator* 🧛

PoC at implementing TLS Certificate `CN=` and `OU=` access to resources via an authz plugin


*vladidators* all go in `validators/` and are responsible for:

- explicitly allowing a request with a `True` value
- explicitly denying a request with a message with a `str` denial message to be passed to the client
- doing absolutely nothing `None`


Each validator implements the following function template
```python
async def validate_request(req: DockerRequest) -> Union[None, str, bool]:
    pass
```


### Certificate requirements

Following along with <https://docs.docker.com/engine/security/https/> we need to make a slight modification to the client certificate signing request.

At the line
```bash
openssl req -subj '/CN=client' -new -key key.pem -out client.csr
```

Becomes the following (where `groupname` is set)

```bash
openssl req -subj '/CN=client/OU=groupname' -new -key key.pem -out client.csr
```


##### todo
vampire jokes to work into readme

- [ ] invited in with a key (TLS Cert)
- [ ] validators == spawn
- [ ] mi*stake* jokes


### Handler index

- [x] [/containers/json](vlad/validators/containers.py)
- [x] [/containers/create](vlad/validators/containers.py)
- [x] [/containers/{id}/json](vlad/validators/containers.py)
- [x] [/containers/{id}/top](vlad/validators/containers.py)
- [x] [/containers/{id}/logs](vlad/validators/containers.py)
- [x] [/containers/{id}/changes](vlad/validators/containers.py)
- [x] [/containers/{id}/export](vlad/validators/containers.py)
- [x] [/containers/{id}/stats](vlad/validators/containers.py)
- [x] [/containers/{id}/resize](vlad/validators/containers.py)
- [x] [/containers/{id}/start](vlad/validators/containers.py)
- [x] [/containers/{id}/stop](vlad/validators/containers.py)
- [x] [/containers/{id}/restart](vlad/validators/containers.py)
- [x] [/containers/{id}/kill](vlad/validators/containers.py)
- [x] [/containers/{id}/update](vlad/validators/containers.py)
- [x] [/containers/{id}/rename](vlad/validators/containers.py)
- [x] [/containers/{id}/pause](vlad/validators/containers.py)
- [x] [/containers/{id}/unpause](vlad/validators/containers.py)
- [x] [/containers/{id}/attach](vlad/validators/containers.py)
- [x] [/containers/{id}/attach/ws](vlad/validators/containers.py)
- [x] [/containers/{id}/wait](vlad/validators/containers.py)
- [x] [/containers/{id}](vlad/validators/containers.py)
- [x] [/containers/{id}/archive](vlad/validators/containers.py)
- [x] [/containers/prune](vlad/validators/containers.py)
- [ ] /images/json
- [ ] /build
- [ ] /build/prune
- [ ] /images/create
- [ ] /images/{name}/json
- [ ] /images/{name}/history
- [ ] /images/{name}/push
- [ ] /images/{name}/tag
- [ ] /images/{name}
- [ ] /images/search
- [ ] /images/prune
- [ ] /auth
- [x] [/info](vlad/validators/info.py)
- [x] [/version](vlad/validators/version.py)
- [x] [/_ping](vlad/validators/ping.py)
- [ ] /commit
- [ ] /events
- [ ] /system/df
- [ ] /images/{name}/get
- [ ] /images/get
- [ ] /images/load
- [x] [/containers/{id}/exec](vlad/validators/containers.py)
- [x] [/exec/{id}/start](vlad/validators/exec.py)
- [x] [/exec/{id}/resize](vlad/validators/exec.py)
- [x] [/exec/{id}/json](vlad/validators/exec.py)
- [x] [/volumes](vlad/validators/volumes.py)
- [x] [/volumes/create](vlad/validators/volumes_create.py)
- [x] [/volumes/{name}](vlad/validators/volumes_OU_delete.py)
- [x] [/volumes/{name}](vlad/validators/volumes_OU_get.py)
- [x] [/volumes/prune](vlad/validators/volumes_prune.py)
- [x] [/networks](vlad/validators/networks.py)
- [x] [/networks/{id}](vlad/validators/networks_OU_get.py)
- [x] [/networks/{id}](vlad/validators/networks_OU_delete.py)
- [x] [/networks/create](vlad/validators/networks_create.py)
- [ ] /networks/{id}/connect
- [ ] /networks/{id}/disconnect
- [ ] /networks/prune
- [x] [/plugins](vlad/validators/plugins.py)
- [x] [/plugins/privileges](vlad/validators/plugins.py)
- [x] [/plugins/pull](vlad/validators/plugins.py)
- [x] [/plugins/{name}/json](vlad/validators/plugins.py)
- [x] [/plugins/{name}](vlad/validators/plugins.py)
- [x] [/plugins/{name}/enable](vlad/validators/plugins.py)
- [x] [/plugins/{name}/disable](vlad/validators/plugins.py)
- [x] [/plugins/{name}/upgrade](vlad/validators/plugins.py)
- [x] [/plugins/create](vlad/validators/plugins.py)
- [x] [/plugins/{name}/push](vlad/validators/plugins.py)
- [x] [/plugins/{name}/set](vlad/validators/plugins.py)
- [x] [/nodes](vlad/validators/nodes.py)
- [x] [/nodes/{id}](vlad/validators/nodes_get.py)
- [x] [/nodes/{id}](vlad/validators/nodes_delete.py)
- [x] [/nodes/{id}/update](vlad/validators/nodes_update.py)
- [x] [/swarm](vlad/validators/swarm.py)
- [x] [/swarm/init](vlad/validators/swarm.py)
- [x] [/swarm/join](vlad/validators/swarm.py)
- [x] [/swarm/leave](vlad/validators/swarm.py)
- [x] [/swarm/update](vlad/validators/swarm.py)
- [x] [/swarm/unlockkey](vlad/validators/swarm.py)
- [x] [/swarm/unlock](vlad/validators/swarm.py)
- [x] [/services](vlad/validators/services.py)
- [x] [/services/create](vlad/validators/services_create.py)
- [x] [/services/{id}](vlad/validators/services_OU_delete.py)
- [x] [/services/{id}](vlad/validators/services_OU_get.py)
- [x] [/services/{id}/update](vlad/validators/services_OU_update.py)
- [x] [/services/{id}/logs](vlad/validators/services_OU_logs.py)
- [x] [/tasks](vlad/validators/tasks.py)
- [ ] /tasks/{id}
- [ ] /tasks/{id}/logs
- [x] [/secrets](vlad/validators/secrets.py)
- [ ] /secrets/create
- [ ] /secrets/{id}
- [ ] /secrets/{id}/update
- [x] [/configs](vlad/validators/configs.py)
- [ ] /configs/create
- [ ] /configs/{id}
- [ ] /configs/{id}/update
- [ ] /distribution/{name}/json
- [ ] /session
