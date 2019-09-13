HOST := 'localhost'

CA := certs/ca-key.pem certs/ca.pem
SERVER := certs/server-key.pem certs/server-cert.pem
CLIENT := certs/key.pem certs/cert.pem

certs:
	@mkdir -p certs/

certs/server.cnf:
	@echo "subjectAltName = DNS:${HOST},IP:127.0.0.1" > certs/server.cnf

certs/client.cnf:
	@echo "extendedKeyUsage = clientAuth" > certs/client.cnf

$(CA): certs
	@openssl genrsa -aes256 -out certs/ca-key.pem 4096
	@openssl req -new -x509 -days 365 -key certs/ca-key.pem -sha256 -out certs/ca.pem

$(SERVER): $(CA) certs/server.cnf
	@openssl req -subj "/CN=${HOST}" -sha256 -new -keyout certs/server-key.pem -out certs/server.csr -nodes
	@openssl x509 -req -days 365 -sha256 -in certs/server.csr -CA certs/ca.pem -CAkey certs/ca-key.pem -CAcreateserial -out certs/server-cert.pem -extfile certs/server.cnf
	@rm certs/server.csr

$(CLIENT): $(CA) certs/client.cnf
	@openssl req -subj '/CN=meowsalot/OU=meow' -new -keyout certs/key.pem -out certs/client.csr -nodes
	@openssl x509 -req -days 365 -sha256 -in certs/client.csr -CA certs/ca.pem -CAkey certs/ca-key.pem -CAcreateserial -out certs/cert.pem -extfile certs/client.cnf
	@rm certs/client.csr

all: $(SERVER) $(CLIENT)
server: $(SERVER)
client: $(CLIENT)

run_docker: $(CLIENT) $(SERVER)
	sudo dockerd --tlsverify --tlscacert=certs/ca.pem --tlscert=certs/server-cert.pem --tlskey=certs/server-key.pem -H=127.0.0.1:2376 -H unix:///var/run/docker.sock --authorization-plugin=vlad

run_server:
	sudo /usr/lib/systemd/systemd-activate -l /var/run/docker/plugins/vlad.sock env/bin/python ./main.py


route_todo:
	sed -i -e '/### Handler index\n/q' README.md
	./check_handlers.sh | tee -a README.md
