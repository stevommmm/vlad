# Vlad *the validator* 🧛

:warning: Super early days, we live in master. Vlad is still young and subject to change.

Vlad forces client interactions to be limited to the resources prefixed with the same `OU=` as the user TLS certificate. With `OU=tst` I could interact with service `tst_thing` and `tstthing` but not `different_service`. The same principle holds for networks, volumes and every other resource type. A *public* OU is automatically added for all clients.

Because we can't mutate the response to the client, global indexing is allowed, but deletion, inspection, update, etc is restricted to the client OU prefix.

[Installation](#installation) | [Development](#development-installation) | [Docker Hub](https://hub.docker.com/r/c45y/vlad)


### Certificate requirements

Following along with <https://docs.docker.com/engine/security/https/> we need to make a slight modification to the client certificate signing request.

The line
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

To complete, add `vlad` to your `authorization-plugins` configuration in `daemon.json`.

A small number of plugin configuration options can be toggled:

- `VLAD_BIND_MOUNT` sets the ability to perform host bind mounts, default **false**
- `VLAD_BIND_PORTS` toggles port binding outside the 30000-61000 range, default **false**

Current configuration can be seen using:

```bash
docker plugin inspect -f {{.Settings.Env}} vlad
```


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

### Tests

A small test harness based on the [docker-bench-security](https://github.com/docker/docker-bench-security) setup to run through known valid/invalid operations. Runs a docker daemon with vlad under a `mktemp` directory which is destroyed at the end of testing.

```bash
systemctl stop docker  # Can't have another one running
cd test && sudo ./test
```

Output looks something like

```
Calling check_tls_volume_bad_bind
> docker volume create --opt=type=bind --opt=device=/tmp testgroup_4711accf0672
Error response from daemon: authorization denied by plugin c45y/vlad:latest: You cannot bind mount.
[PASS][check_tls_volume_bad_bind]

Calling check_tls_volume_bad_ou
> docker volume create badgroup_29d63f46fa7f
Error response from daemon: authorization denied by plugin c45y/vlad:latest: That volume is outside your OU prefix. ('public', 'testgroup')
[PASS][check_tls_volume_bad_ou]

Calling check_tls_volume_ou
> docker volume create testgroup_3c2739947c82
testgroup_3c2739947c82
[PASS][check_tls_volume_ou]


===================
Completed tests: 11
Passed tests:    11
```


### Todo

- [ ] work more vampire jokes into readme
- [x] echo OUs back to clients when bad prefix
    > standardize response messages
- [ ] certificate revocation for clients
    > decline via `CN=` & `OU=` as docker doesn't handle revocation?
- [x] configuration options
    > enable port binding / bind mounts / toggle random allow/block features


### Validators

Default Request/Response *vladidators* all come from `vlad.validators`, though the list can be mutated at startup if required.

To implemnent custom functionality you can override/append async functions to the list of handlers indexed by `make_app`.

```python
app = make_app()
app['validators']['request'] = [my_custom_async_func]
```

Validators have the choice of:

- explicitly allowing a request with a `True` value
- explicitly denying a request with a `str` denial message to be passed to the client
- doing absolutely nothing (`None`)

Requests are **default deny**, Response is default allow.

Each validator implements either/both the following function templates
```python
@handles.post('configs', 'create')
async def validate_request(req: DockerRequest) -> Union[None, str, bool]:
    pass

async def validate_response(res: DockerResponse) -> Union[None, str]:
    pass
```

The `handles` decorator implements structured filtering to the validation functions. Check [vlad/validators/](vlad/validators/) for extensive usage examples.


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
