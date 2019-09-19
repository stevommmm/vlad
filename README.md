# Vlad *the validator* 🧛

PoC at implementing TLS Certificate `CN=` and `OU=` access to resources via an authz plugin


Request/Response *vladidators* all come from `validators/` and are responsible for:

- explicitly allowing a request with a `True` value
- explicitly denying a request with a `str` denial message to be passed to the client
- doing absolutely nothing (`None`)

Requests are **default deny**, Response is default allow.


Each validator implements eithor/both the following function templates
```python
async def validate_request(req: DockerRequest) -> Union[None, str, bool]:
    pass

async def validate_response(res: DockerResponse) -> Union[None, str]:
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

### Installation

From your command line:

```bash
pushd plugin/
make plugin  # Build the plugin on the local daemon, no push
docker plugin enable vlad:latest  # Enable our dev plugin
popd
sudo ./deploy.sh  # Generate docker CA/Node/Client certificates and deploy daemon.json
sudo ./docker.sh info  # Uses the client certificate via TLS + vlad authz
sudo docker info  # Uses existing unix socket (which is blanket allowed by vlad)
```


#### todo

- [ ] work more vampire jokes to work into readme
- [ ] echo OUs back to clients when bad prefix
    > standardise response messages
- [ ] certificate revocation for clients
    > decline via `CN=` & `OU=` as docker doesn't handle revocation?


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
- [x] [/commit:post](vlad/validators/commit.py)
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
- [x] [/networks/prune:post](vlad/validators/networks_prune.py)
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
- [x] [/tasks/{id}:get](vlad/validators/tasks_get.py)
- [ ] /tasks/{id}/logs:get
- [x] [/secrets:get](vlad/validators/secrets.py)
- [x] [/secrets/create:post](vlad/validators/secrets_create.py)
- [x] [/secrets/{id}:get](vlad/validators/secrets_OU_get.py)
- [x] [/secrets/{id}/update:post](vlad/validators/secrets_OU_update.py)
- [x] [/configs:get](vlad/validators/configs.py)
- [x] [/configs/create:post](vlad/validators/configs_create.py)
- [x] [/configs/{id}:get](vlad/validators/configs_OU_get.py)
- [x] [/configs/{id}/update:post](vlad/validators/configs_OU_update.py)
- [ ] /distribution/{name}/json:get
- [ ] /session:post
