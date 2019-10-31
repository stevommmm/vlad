function check_stack_deploy() {
	local here=$(dirname "${BASH_SOURCE[0]}")
	tls_docker stack deploy -c "${here}/stack.yml" testgroup_n
	[ $? -eq 0 ] && pass || fail "TLS 'stack deploy' failed within namespace"
}

function check_stack_deploy_outside_ou() {
	local here=$(dirname "${BASH_SOURCE[0]}")
	tls_docker stack deploy -c "${here}/stack.yml" badou_n
	[ $? -eq 0 ] && fail "TLS 'stack deploy' success outside namespace." || pass
}
