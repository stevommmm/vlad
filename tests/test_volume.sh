function check_tls_volume_ou() {
	local rand=$(r6)
	tls_docker volume create "testgroup_${rand}"
	[ $? -eq 0 ] && pass || fail "TLS failed 'volume create' in OU, which it shouldn't."
}

function check_tls_volume_bad_ou() {
	local rand=$(r6)
	tls_docker volume create "badgroup_${rand}"
	[ $? -gt 0 ] && pass || fail "TLS success 'volume create' outside OU, which it shouldn't."
}

function check_tls_volume_bad_bind() {
	local rand=$(r6)
	tls_docker volume create --opt="type=bind" --opt="device=/tmp" "testgroup_${rand}"
	[ $? -gt 0 ] && pass || fail "TLS success 'volume create' with a bind mount, which it shouldn't."
}
