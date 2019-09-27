# Vlad *the validator* 🧛

PoC at implementing TLS Certificate `CN=` and `OU=` access to resources via an authz plugin


/!\ Super early days, we live in master.


Request/Response *vladidators* all come from `validators/` and are responsible for:

- explicitly allowing a request with a `True` value
- explicitly denying a request with a `str` denial message to be passed to the client
- doing absolutely nothing (`None`)

Requests are **default deny**, Response is default allow.


Each validator implements either/both the following function templates
```python
@handles('POST', '', 'configs', 'create')
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

```bash
docker plugin install c45y/vlad --alias vlad
```

And add `vlad` to your `authorization-plugins` configuration in `daemon.json`.

At the moment there are no fancy toggle or configuration for you to worry about, yay?


### Development Installation

From your command line:

```bash
docker build -t rootfsimage .
docker create --name vlad_container rootfsimage true
mkdir -p rootfs
docker export vlad_container | tar -x -C rootfs
docker plugin create vlad .
docker plugin enable vlad:latest  # Enable our dev plugin
sudo ./scripts/deploy.sh  # Generate docker CA/Node/Client certificates and deploy daemon.json
sudo ./scripts/docker.sh info  # Uses the client certificate via TLS + vlad authz
sudo docker info  # Uses existing unix socket (which is blanket allowed by vlad)
```


#### todo

- [ ] test suite
- [ ] work more vampire jokes to work into readme
- [ ] echo OUs back to clients when bad prefix
    > standardize response messages
- [ ] certificate revocation for clients
    > decline via `CN=` & `OU=` as docker doesn't handle revocation?
- [ ] configuration options
    > enable port binding / bind mounts / toggle random allow/block features



### Handler Index:

- [delete:/networks/*](vlad/validators/networks_OU_delete.py)
- [delete:/services/*](vlad/validators/services_OU_delete.py)
- [get:/secrets/*](vlad/validators/secrets_OU_get.py)
- [get:/configs/*](vlad/validators/configs_OU_get.py)
- [get:/plugins](vlad/validators/plugins.py)
- [get:/plugins/privileges](vlad/validators/plugins.py)
- [post:/plugins/pull](vlad/validators/plugins.py)
- [get:/plugins/*/json](vlad/validators/plugins.py)
- [delete:/plugins/*](vlad/validators/plugins.py)
- [post:/plugins/*/enable](vlad/validators/plugins.py)
- [post:/plugins/*/disable](vlad/validators/plugins.py)
- [post:/plugins/*/upgrade](vlad/validators/plugins.py)
- [post:/plugins/create](vlad/validators/plugins.py)
- [post:/plugins/*/push](vlad/validators/plugins.py)
- [post:/plugins/*/set](vlad/validators/plugins.py)
- [get:/secrets](vlad/validators/secrets.py)
- [get:/images/json](vlad/validators/images.py)
- [post:/images/create](vlad/validators/images.py)
- [get:/images/*/json](vlad/validators/images.py)
- [get:/images/*/history](vlad/validators/images.py)
- [post:/images/*/push](vlad/validators/images.py)
- [post:/images/*/tag](vlad/validators/images.py)
- [delete:/images/*](vlad/validators/images.py)
- [get:/images/search](vlad/validators/images.py)
- [post:/images/prune](vlad/validators/images.py)
- [get:/images/*/get](vlad/validators/images.py)
- [get:/images/get](vlad/validators/images.py)
- [post:/images/load](vlad/validators/images.py)
- [post:/commit](vlad/validators/commit.py)
- [head:/_ping](vlad/validators/ping.py)
- [get:/_ping](vlad/validators/ping.py)
- [get:/volumes/*](vlad/validators/volumes_OU_get.py)
- [post:/secrets/create](vlad/validators/secrets_create.py)
- [get:/configs](vlad/validators/configs.py)
- [post:/configs/create](vlad/validators/configs_create.py)
- [get:/networks/*](vlad/validators/networks_OU_get.py)
- [get:/services/*](vlad/validators/services_OU_get.py)
- [delete:/secrets/*](vlad/validators/secrets_OU_delete.py)
- [get:/tasks/*](vlad/validators/tasks_get.py)
- [post:/configs/*/update](vlad/validators/configs_OU_update.py)
- [get:/containers/json](vlad/validators/containers.py)
- [post:/containers/create](vlad/validators/containers.py)
- [get:/containers/*/json](vlad/validators/containers.py)
- [get:/containers/*/top](vlad/validators/containers.py)
- [get:/containers/*/logs](vlad/validators/containers.py)
- [get:/containers/*/changes](vlad/validators/containers.py)
- [get:/containers/*/export](vlad/validators/containers.py)
- [get:/containers/*/stats](vlad/validators/containers.py)
- [post:/containers/*/resize](vlad/validators/containers.py)
- [post:/containers/*/start](vlad/validators/containers.py)
- [post:/containers/*/stop](vlad/validators/containers.py)
- [post:/containers/*/restart](vlad/validators/containers.py)
- [post:/containers/*/kill](vlad/validators/containers.py)
- [post:/containers/*/update](vlad/validators/containers.py)
- [post:/containers/*/rename](vlad/validators/containers.py)
- [post:/containers/*/pause](vlad/validators/containers.py)
- [post:/containers/*/unpause](vlad/validators/containers.py)
- [post:/containers/*/attach](vlad/validators/containers.py)
- [get:/containers/*/attach/ws](vlad/validators/containers.py)
- [post:/containers/*/wait](vlad/validators/containers.py)
- [delete:/containers/*](vlad/validators/containers.py)
- [head:/containers/*/archive](vlad/validators/containers.py)
- [put:/containers/*/archive](vlad/validators/containers.py)
- [get:/containers/*/archive](vlad/validators/containers.py)
- [post:/containers/prune](vlad/validators/containers.py)
- [post:/containers/*/exec](vlad/validators/containers.py)
- [post:/exec/*/start](vlad/validators/exec.py)
- [post:/exec/*/resize](vlad/validators/exec.py)
- [get:/exec/*/json](vlad/validators/exec.py)
- [get:/info](vlad/validators/info.py)
- [get:/networks](vlad/validators/networks.py)
- [post:/networks/create](vlad/validators/networks_create.py)
- [get:/nodes](vlad/validators/nodes.py)
- [delete:/nodes/*](vlad/validators/nodes_delete.py)
- [get:/nodes/*](vlad/validators/nodes_get.py)
- [get:/services](vlad/validators/services.py)
- [get:/tasks](vlad/validators/tasks.py)
- [get:/version](vlad/validators/version.py)
- [get:/volumes](vlad/validators/volumes.py)
- [post:/volumes/create](vlad/validators/volumes_create.py)
- [post:/volumes/prune](vlad/validators/volumes_prune.py)
- [post:/nodes/*/update](vlad/validators/nodes_update.py)
- [get:/swarm](vlad/validators/swarm.py)
- [post:/swarm/init](vlad/validators/swarm.py)
- [post:/swarm/join](vlad/validators/swarm.py)
- [post:/swarm/leave](vlad/validators/swarm.py)
- [post:/swarm/update](vlad/validators/swarm.py)
- [get:/swarm/unlockkey](vlad/validators/swarm.py)
- [post:/swarm/unlock](vlad/validators/swarm.py)
- [post:/services/create](vlad/validators/services_create.py)
- [post:/auth](vlad/validators/auth.py)
- [post:/build](vlad/validators/build.py)
- [post:/build/prune](vlad/validators/build.py)
- [post:/networks/prune](vlad/validators/networks_prune.py)
- [get:/services/*/logs](vlad/validators/services_OU_logs.py)
- [delete:/volumes/*](vlad/validators/volumes_OU_delete.py)
- [post:/secrets/*/update](vlad/validators/secrets_OU_update.py)
- [delete:/configs/*](vlad/validators/configs_OU_delete.py)
- [post:/services/*/update](vlad/validators/services_OU_update.py)

### We are missing handlers for:

 - get:/events
 - post:/networks/*/connect
 - post:/session
 - get:/system/df
 - get:/distribution/*/json
 - post:/networks/*/disconnect
 - get:/tasks/*/logs
