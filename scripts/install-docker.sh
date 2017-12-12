#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

apt-get install --force-yes -y docker-ce

curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" > /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

docker version

docker-compose version
