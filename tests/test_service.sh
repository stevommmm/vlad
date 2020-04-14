function check_tls_service_ou() {
	local rand=$(r6)
	tls_docker service create --name "testgroup_${rand}" nginx:latest
	[ $? -eq 0 ] && pass || fail "TLS failed 'service create' in OU, which it shouldn't."
}

function check_tls_service_bad_ou() {
	local rand=$(r6)
	tls_docker service create --name "badgroup_${rand}" nginx:latest
	[ $? -gt 0 ] && pass || fail "TLS success 'service create' outside OU, which it shouldn't."
}

function check_tls_service_bad_mount() {
	local rand=$(r6)
	tls_docker service create --name "testgroup_${rand}" --mount "type=bind,source=/tmp,destination=/mnt" nginx:latest
	[ $? -gt 0 ] && pass || fail "TLS success 'service create' with a bind mount, which it shouldn't."
}

function check_tls_service_bad_port() {
	local rand=$(r6)
	tls_docker service create --name "testgroup_${rand}" --publish "80:80" nginx:latest
	[ $? -gt 0 ] && pass || fail "TLS success 'service create' non-ephemeral port, which it shouldn't."
}
function check_tls_service_bad_secret() {
	local rand=$(r6)
	tls_docker service create --name "testgroup_${rand}" --secret invld_invalid_d nginx:latest
	[ $? -gt 0 ] && pass || fail "TLS success 'service create' external namespace secret, which it shouldn't."
}
function check_tls_service_bad_config() {
	local rand=$(r6)
	tls_docker service create --name "testgroup_${rand}" --config invld_invalid_c nginx:latest
	[ $? -gt 0 ] && pass || fail "TLS success 'service create' external namespace config, which it shouldn't."
}
