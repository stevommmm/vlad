#!/bin/bash
vers=${1:-v1.39}
ec=0
for path in $(curl -s "https://docs.docker.com/engine/api/${vers}/swagger.yaml" | grep -A1 '^  /' | tr -d ' \n' | tr '\-\-' '\n'); do
	foundin=$(grep -Rl --exclude=\*.pyc "^# handles: ${path::-1}\$" vlad/validators/)
	if [[ -z "$foundin" ]]; then
		echo "- [ ] ${path::-1}"
		ec=1
	else
		for x in $foundin; do
			echo "- [x] [${path::-1}](${x})"
		done
	fi
done

exit $ec
