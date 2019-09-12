# Vlad *the validator* 🧛

PoC at implementing TLS Certificate `CN=` and `OU=` access to resources via an authz plugin


*vladidators* all go in `validators/` and are responsible for:

- explicitly allowing a request with a `True` value
- explicitly denying a request with a `str` denial message to be passed to the client
- doing absolutely nothing (`None`)


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

- [x] [/containers/json:get](vlad/validators/containers.py)
- [x] [/containers/create:post](vlad/validators/containers.py)
- [x] [/containers/{id}/json:get](vlad/validators/containers.py)
- [x] [/containers/{id}/top:get](vlad/validators/containers.py)
- [x] [/containers/{id}/logs:get](vlad/validators/containers.py)
- [x] [/containers/{id}/changes:get](vlad/validators/containers.py)
- [x] [/containers/{id}/export:get](vlad/validators/containers.py)
- [x] [/containers/{id}/stats:get](vlad/validators/containers.py)
- [x] [/containers/{id}/resize:post](vlad/validators/containers.py)
- [x] [/containers/{id}/start:post](vlad/validators/containers.py)
- [x] [/containers/{id}/stop:post](vlad/validators/containers.py)
- [x] [/containers/{id}/restart:post](vlad/validators/containers.py)
- [x] [/containers/{id}/kill:post](vlad/validators/containers.py)
- [x] [/containers/{id}/update:post](vlad/validators/containers.py)
- [x] [/containers/{id}/rename:post](vlad/validators/containers.py)
- [x] [/containers/{id}/pause:post](vlad/validators/containers.py)
- [x] [/containers/{id}/unpause:post](vlad/validators/containers.py)
- [x] [/containers/{id}/attach:post](vlad/validators/containers.py)
- [x] [/containers/{id}/attach/ws:get](vlad/validators/containers.py)
- [x] [/containers/{id}/wait:post](vlad/validators/containers.py)
- [x] [/containers/{id}:delete](vlad/validators/containers.py)
- [x] [/containers/{id}/archive:head](vlad/validators/containers.py)
- [x] [/containers/prune:post](vlad/validators/containers.py)
- [x] [/images/json:get](vlad/validators/images.py)
- [x] [/build:post](vlad/validators/build.py)
- [x] [/build/prune:post](vlad/validators/build.py)
- [x] [/images/create:post](vlad/validators/images.py)
- [x] [/images/{name}/json:get](vlad/validators/images.py)
- [x] [/images/{name}/history:get](vlad/validators/images.py)
- [x] [/images/{name}/push:post](vlad/validators/images.py)
- [x] [/images/{name}/tag:post](vlad/validators/images.py)
- [x] [/images/{name}:delete](vlad/validators/images.py)
- [x] [/images/search:get](vlad/validators/images.py)
- [x] [/images/prune:post](vlad/validators/images.py)
- [x] [/auth:post](vlad/validators/auth.py)
- [x] [/info:get](vlad/validators/info.py)
- [x] [/version:get](vlad/validators/version.py)
- [x] [/_ping:get](vlad/validators/ping.py)
- [ ] /commit:post
- [ ] /events:get
- [ ] /system/df:get
- [x] [/images/{name}/get:get](vlad/validators/images.py)
- [x] [/images/get:get](vlad/validators/images.py)
- [x] [/images/load:post](vlad/validators/images.py)
- [x] [/containers/{id}/exec:post](vlad/validators/containers.py)
- [x] [/exec/{id}/start:post](vlad/validators/exec.py)
- [x] [/exec/{id}/resize:post](vlad/validators/exec.py)
- [x] [/exec/{id}/json:get](vlad/validators/exec.py)
- [x] [/volumes:get](vlad/validators/volumes.py)
- [x] [/volumes/create:post](vlad/validators/volumes_create.py)
- [x] [/volumes/{name}:get](vlad/validators/volumes_OU_get.py)
- [x] [/volumes/prune:post](vlad/validators/volumes_prune.py)
- [x] [/networks:get](vlad/validators/networks.py)
- [x] [/networks/{id}:get](vlad/validators/networks_OU_get.py)
- [x] [/networks/create:post](vlad/validators/networks_create.py)
- [ ] /networks/{id}/connect:post
- [ ] /networks/{id}/disconnect:post
- [ ] /networks/prune:post
- [x] [/plugins:get](vlad/validators/plugins.py)
- [x] [/plugins/privileges:get](vlad/validators/plugins.py)
- [x] [/plugins/pull:post](vlad/validators/plugins.py)
- [x] [/plugins/{name}/json:get](vlad/validators/plugins.py)
- [x] [/plugins/{name}:delete](vlad/validators/plugins.py)
- [x] [/plugins/{name}/enable:post](vlad/validators/plugins.py)
- [x] [/plugins/{name}/disable:post](vlad/validators/plugins.py)
- [x] [/plugins/{name}/upgrade:post](vlad/validators/plugins.py)
- [x] [/plugins/create:post](vlad/validators/plugins.py)
- [x] [/plugins/{name}/push:post](vlad/validators/plugins.py)
- [x] [/plugins/{name}/set:post](vlad/validators/plugins.py)
- [x] [/nodes:get](vlad/validators/nodes.py)
- [x] [/nodes/{id}:get](vlad/validators/nodes_get.py)
- [x] [/nodes/{id}/update:post](vlad/validators/nodes_update.py)
- [x] [/swarm:get](vlad/validators/swarm.py)
- [x] [/swarm/init:post](vlad/validators/swarm.py)
- [x] [/swarm/join:post](vlad/validators/swarm.py)
- [x] [/swarm/leave:post](vlad/validators/swarm.py)
- [x] [/swarm/update:post](vlad/validators/swarm.py)
- [x] [/swarm/unlockkey:get](vlad/validators/swarm.py)
- [x] [/swarm/unlock:post](vlad/validators/swarm.py)
- [x] [/services:get](vlad/validators/services.py)
- [x] [/services/create:post](vlad/validators/services_create.py)
- [x] [/services/{id}:get](vlad/validators/services_OU_get.py)
- [x] [/services/{id}/update:post](vlad/validators/services_OU_update.py)
- [x] [/services/{id}/logs:get](vlad/validators/services_OU_logs.py)
- [x] [/tasks:get](vlad/validators/tasks.py)
- [ ] /tasks/{id}:get
- [ ] /tasks/{id}/logs:get
- [x] [/secrets:get](vlad/validators/secrets.py)
- [ ] /secrets/create:post
- [ ] /secrets/{id}:get
- [ ] /secrets/{id}/update:post
- [x] [/configs:get](vlad/validators/configs.py)
- [ ] /configs/create:post
- [ ] /configs/{id}:get
- [ ] /configs/{id}/update:post
- [ ] /distribution/{name}/json:get
- [ ] /session:post
- [x] [/containers/json:get](vlad/validators/containers.py)
- [x] [/containers/create:post](vlad/validators/containers.py)
- [x] [/containers/{id}/json:get](vlad/validators/containers.py)
- [x] [/containers/{id}/top:get](vlad/validators/containers.py)
- [x] [/containers/{id}/logs:get](vlad/validators/containers.py)
- [x] [/containers/{id}/changes:get](vlad/validators/containers.py)
- [x] [/containers/{id}/export:get](vlad/validators/containers.py)
- [x] [/containers/{id}/stats:get](vlad/validators/containers.py)
- [x] [/containers/{id}/resize:post](vlad/validators/containers.py)
- [x] [/containers/{id}/start:post](vlad/validators/containers.py)
- [x] [/containers/{id}/stop:post](vlad/validators/containers.py)
- [x] [/containers/{id}/restart:post](vlad/validators/containers.py)
- [x] [/containers/{id}/kill:post](vlad/validators/containers.py)
- [x] [/containers/{id}/update:post](vlad/validators/containers.py)
- [x] [/containers/{id}/rename:post](vlad/validators/containers.py)
- [x] [/containers/{id}/pause:post](vlad/validators/containers.py)
- [x] [/containers/{id}/unpause:post](vlad/validators/containers.py)
- [x] [/containers/{id}/attach:post](vlad/validators/containers.py)
- [x] [/containers/{id}/attach/ws:get](vlad/validators/containers.py)
- [x] [/containers/{id}/wait:post](vlad/validators/containers.py)
- [x] [/containers/{id}:delete](vlad/validators/containers.py)
- [x] [/containers/{id}/archive:head](vlad/validators/containers.py)
- [x] [/containers/prune:post](vlad/validators/containers.py)
- [x] [/images/json:get](vlad/validators/images.py)
- [x] [/build:post](vlad/validators/build.py)
- [x] [/build/prune:post](vlad/validators/build.py)
- [x] [/images/create:post](vlad/validators/images.py)
- [x] [/images/{name}/json:get](vlad/validators/images.py)
- [x] [/images/{name}/history:get](vlad/validators/images.py)
- [x] [/images/{name}/push:post](vlad/validators/images.py)
- [x] [/images/{name}/tag:post](vlad/validators/images.py)
- [x] [/images/{name}:delete](vlad/validators/images.py)
- [x] [/images/search:get](vlad/validators/images.py)
- [x] [/images/prune:post](vlad/validators/images.py)
- [x] [/auth:post](vlad/validators/auth.py)
- [x] [/info:get](vlad/validators/info.py)
- [x] [/version:get](vlad/validators/version.py)
- [x] [/_ping:get](vlad/validators/ping.py)
- [ ] /commit:post
- [ ] /events:get
- [ ] /system/df:get
- [x] [/images/{name}/get:get](vlad/validators/images.py)
- [x] [/images/get:get](vlad/validators/images.py)
- [x] [/images/load:post](vlad/validators/images.py)
- [x] [/containers/{id}/exec:post](vlad/validators/containers.py)
- [x] [/exec/{id}/start:post](vlad/validators/exec.py)
- [x] [/exec/{id}/resize:post](vlad/validators/exec.py)
- [x] [/exec/{id}/json:get](vlad/validators/exec.py)
- [x] [/volumes:get](vlad/validators/volumes.py)
- [x] [/volumes/create:post](vlad/validators/volumes_create.py)
- [x] [/volumes/{name}:get](vlad/validators/volumes_OU_get.py)
- [x] [/volumes/prune:post](vlad/validators/volumes_prune.py)
- [x] [/networks:get](vlad/validators/networks.py)
- [x] [/networks/{id}:get](vlad/validators/networks_OU_get.py)
- [x] [/networks/create:post](vlad/validators/networks_create.py)
- [ ] /networks/{id}/connect:post
- [ ] /networks/{id}/disconnect:post
- [ ] /networks/prune:post
- [x] [/plugins:get](vlad/validators/plugins.py)
- [x] [/plugins/privileges:get](vlad/validators/plugins.py)
- [x] [/plugins/pull:post](vlad/validators/plugins.py)
- [x] [/plugins/{name}/json:get](vlad/validators/plugins.py)
- [x] [/plugins/{name}:delete](vlad/validators/plugins.py)
- [x] [/plugins/{name}/enable:post](vlad/validators/plugins.py)
- [x] [/plugins/{name}/disable:post](vlad/validators/plugins.py)
- [x] [/plugins/{name}/upgrade:post](vlad/validators/plugins.py)
- [x] [/plugins/create:post](vlad/validators/plugins.py)
- [x] [/plugins/{name}/push:post](vlad/validators/plugins.py)
- [x] [/plugins/{name}/set:post](vlad/validators/plugins.py)
- [x] [/nodes:get](vlad/validators/nodes.py)
- [x] [/nodes/{id}:get](vlad/validators/nodes_get.py)
- [x] [/nodes/{id}/update:post](vlad/validators/nodes_update.py)
- [x] [/swarm:get](vlad/validators/swarm.py)
- [x] [/swarm/init:post](vlad/validators/swarm.py)
- [x] [/swarm/join:post](vlad/validators/swarm.py)
- [x] [/swarm/leave:post](vlad/validators/swarm.py)
- [x] [/swarm/update:post](vlad/validators/swarm.py)
- [x] [/swarm/unlockkey:get](vlad/validators/swarm.py)
- [x] [/swarm/unlock:post](vlad/validators/swarm.py)
- [x] [/services:get](vlad/validators/services.py)
- [x] [/services/create:post](vlad/validators/services_create.py)
- [x] [/services/{id}:get](vlad/validators/services_OU_get.py)
- [x] [/services/{id}/update:post](vlad/validators/services_OU_update.py)
- [x] [/services/{id}/logs:get](vlad/validators/services_OU_logs.py)
- [x] [/tasks:get](vlad/validators/tasks.py)
- [ ] /tasks/{id}:get
- [ ] /tasks/{id}/logs:get
- [x] [/secrets:get](vlad/validators/secrets.py)
- [ ] /secrets/create:post
- [ ] /secrets/{id}:get
- [ ] /secrets/{id}/update:post
- [x] [/configs:get](vlad/validators/configs.py)
- [ ] /configs/create:post
- [ ] /configs/{id}:get
- [ ] /configs/{id}/update:post
- [ ] /distribution/{name}/json:get
- [ ] /session:post
