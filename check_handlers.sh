#!/bin/bash
for path in $(curl -s https://docs.docker.com/engine/api/v1.39/swagger.yaml | grep '^  /'); do
	if ! grep --silent -R --exclude=\*.pyc "handles: ${path::-1}" vlad/validators/; then
		echo "- [ ] Missing handler for ${path::-1}"
	else
		echo "- [x] Found hadler for ${path::-1}"
	fi
done
