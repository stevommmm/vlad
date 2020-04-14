HOST='localhost'


mkdir -p /etc/docker/certs
# CA
openssl genrsa -out /etc/docker/certs/ca.key 4096
openssl req -x509 -new -nodes -key /etc/docker/certs/ca.key \
    -sha512 -days 365 -out /etc/docker/certs/ca.crt \
    -subj "/CN=${HOST}"
# Node
openssl genrsa -out /etc/docker/certs/node.key 4096
openssl req -new -key /etc/docker/certs/node.key \
    -out /etc/docker/certs/node.csr \
    -subj "/CN=${HOST}"
openssl x509 -req -in /etc/docker/certs/node.csr \
    -CA /etc/docker/certs/ca.crt \
    -CAkey /etc/docker/certs/ca.key \
    -CAcreateserial \
    -out /etc/docker/certs/node.crt -days 500 -sha512 \
    -extfile <(printf "subjectAltName=DNS:${HOST},IP:127.0.0.1")

# Test Client
openssl req -subj '/CN=testuser/OU=testgroup' -new \
    -keyout /etc/docker/certs/user.key \
    -out /etc/docker/certs/user.csr -nodes
openssl x509 -req -days 365 -sha256 \
    -in /etc/docker/certs/user.csr \
    -CA /etc/docker/certs/ca.crt \
    -CAkey /etc/docker/certs/ca.key \
    -CAcreateserial \
    -out /etc/docker/certs/user.crt \
    -extfile <(printf "extendedKeyUsage=clientAuth")


cat >/etc/docker/daemon.json <<EOF
{
    "hosts": [
        "unix:///var/run/docker.sock",
        "tcp://127.0.0.1:2376"
    ],
    "tlsverify": true,
    "tlscacert": "/etc/docker/certs/ca.crt",
    "tlscert": "/etc/docker/certs/node.crt",
    "tlskey": "/etc/docker/certs/node.key",
    "authorization-plugins": [
        "c45y/vlad"
    ]
}
EOF
