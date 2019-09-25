#!/bin/bash
docker --tlsverify \
  --tlscacert=/etc/docker/certs/ca.crt \
  --tlscert=/etc/docker/certs/user.crt \
  --tlskey=/etc/docker/certs/user.key \
  -H=tcp://127.0.0.1:2376 "$@"
