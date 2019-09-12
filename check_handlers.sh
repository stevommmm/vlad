#!/bin/bash
ec=0
for path in $(curl -s https://docs.docker.com/engine/api/v1.39/swagger.yaml | grep '^  /'); do
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
