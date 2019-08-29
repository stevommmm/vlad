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


##### @todo
vampire jokes to work into readme

- [ ] invited in with a key (TLS Cert)
- [ ] validators == spawn
- [ ] mi*stake* jokes
