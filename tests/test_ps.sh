function check_tls_ps() {
	tls_docker ps -a
	[ $? -gt 0 ] && pass || fail "TLS accepted 'ps -a' which it shouldn't."
}

function check_sock_ps() {
	sock_docker ps -a
	[ $? -eq 0 ] && pass || fail "Socket failed 'ps -a' which it shouldn't."
}
