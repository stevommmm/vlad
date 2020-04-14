#!/bin/bash

__here=$(dirname "$(readlink -f "$0")")
__dockerd_pid=0
__docker_dir=$(mktemp -d)

function r6() {
	openssl rand -hex 6
}

function log() {
	echo -e "$@" 1>&2
}

function pass() {
	log "\e[92m[PASS][${FUNCNAME[1]}] $@\e[0m"
	return 0
}
function fail() {
	log "\e[91m[FAIL][${FUNCNAME[1]}] $@\e[0m"
	return 1
}

function gen_certs() {
	[ -f ./crt_ca.key ] || openssl genrsa -out ./crt_ca.key 4096
	[ -f ./crt_ca.crt ] || openssl req -x509 -new -nodes -key ./crt_ca.key \
	    -sha512 -days 365 -out ./crt_ca.crt \
	    -subj "/CN=localhost"
	[ -f ./crt_node.key ] || openssl genrsa -out ./crt_node.key 4096
	[ -f ./crt_node.csr ] || openssl req -new -key ./crt_node.key \
	    -out ./crt_node.csr \
	    -subj "/CN=localhost"
	[ -f ./crt_node.crt ] || openssl x509 -req -in ./crt_node.csr \
	    -CA ./crt_ca.crt \
	    -CAkey ./crt_ca.key \
	    -CAcreateserial \
	    -out ./crt_node.crt -days 500 -sha512 \
	    -extfile <(printf "subjectAltName=DNS:localhost,IP:127.0.0.1")
	[ -f ./crt_user.key ] || openssl req -subj '/CN=testuser/OU=testgroup' -new \
	    -keyout ./crt_user.key \
	    -out ./crt_user.csr -nodes
	[ -f ./crt_user.crt ] || openssl x509 -req -days 365 -sha256 \
	    -in ./crt_user.csr \
	    -CA ./crt_ca.crt \
	    -CAkey ./crt_ca.key \
	    -CAcreateserial \
	    -out ./crt_user.crt \
	    -extfile <(printf "extendedKeyUsage=clientAuth")
}

function build_plugin() {
	local IMG=$(r6)
	local CONT=$(r6)
	sock_docker build -t "vld${IMG}" .
	sock_docker create --name "vld${CONT}" "vld${IMG}" true
	mkdir -p rootfs
	sock_docker export "vld${CONT}" | tar -x -C rootfs
	sock_docker plugin create c45y/vlad .
	rm -r rootfs
}

function deploy_invalid_stack() {
	local stackstr=$(cat <<-END
version: "3.7"
services:
  web:
    image: nginx:latest
    deploy:
      mode: replicated
      replicas: 1
    volumes:
      - "invalid_b:/lala"
    configs:
      - invalid_c
    networks:
      - invalid_a
    secrets:
      - invalid_d
networks:
  invalid_a:
    driver: overlay
volumes:
  invalid_b:
    driver: local
configs:
  invalid_c:
    file: /etc/os-release
secrets:
  invalid_d:
    file: /etc/os-release

END
)
	sock_docker stack deploy -c  <(printf "$stackstr") invld
}


function background_docker() {
	local PORT=8888
	local SOCK=$(readlink -f "${__docker_dir}/sock")
	# Vlad is expecting to mount this in, must be a better way
	ln -sf $SOCK /var/run/docker.sock
	local LOG=$(readlink -f "${__docker_dir}/daemon.log")
	echo "{}" > "${__docker_dir}/daemon.json"
	log "Starting docker daemon on port ${PORT} and sock ${SOCK}, sending logs to ${LOG}"

	# Run daemon for setup with no TLS
	/usr/bin/dockerd --data-root="${__docker_dir}" --config-file="${__docker_dir}/daemon.json" --iptables=false --pidfile="${__docker_dir}/docker.pid" \
	  -H "unix://${SOCK}" &>> $LOG &
	__dockerd_pid=$!
	sleep 3

	log "Building docker plugin..."
	pushd .. >/dev/null
	build_plugin >/dev/null
	popd

	log "Enabling plugin..."
	sock_docker plugin install c45y/vlad --grant-all-permissions
	sock_docker plugin enable c45y/vlad
	sock_docker swarm init --listen-addr="127.0.0.1:${RANDOM}" --advertise-addr="127.0.0.1:${RANDOM}"
	deploy_invalid_stack

	kill $__dockerd_pid
	wait $__dockerd_pid
	sleep 3

	log "Beginning docker daemon with vlad..."
	# Open up unix/TLS daemon for testing
	/usr/bin/dockerd --data-root="${__docker_dir}" --config-file="${__docker_dir}/daemon.json" --iptables=false --pidfile="${__docker_dir}/docker.pid" \
	  --authorization-plugin="c45y/vlad" -H "tcp://127.0.0.1:${PORT}" -H "unix://${SOCK}" \
	  --tlsverify --tlscacert=./crt_ca.crt --tlscert=./crt_node.crt --tlskey=./crt_node.key &>> $LOG &
	__dockerd_pid=$!
}

function tls_docker() {
	log "\e[90m> docker ${@}\e[0m"
	docker --tlsverify \
	  --tlscacert=./crt_ca.crt \
	  --tlscert=./crt_user.crt \
	  --tlskey=./crt_user.key \
	  -H=tcp://127.0.0.1:8888 "$@"
}

function sock_docker() {
	log "\e[90m> docker ${@}\e[0m"
	local SOCK=$(readlink -f "${__docker_dir}/sock")
	docker -H="unix://${SOCK}" "$@"
}
