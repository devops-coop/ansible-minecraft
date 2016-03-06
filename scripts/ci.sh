#!/usr/bin/env bash
set -euxo pipefail
IFS=$'\n\t'

declare -r WORKSPACE="${WORKSPACE:-/tmp/ansible-minecraft}"

function cleanup() {
  #docker-compose down --rmi all
  docker-compose down
}

function main() {
  docker-compose up -d

  for container in $(docker-compose ps -q); do
    # Install role.
    docker cp . "${container}:${WORKSPACE}"

    # Validate syntax
    docker exec -t "${container}" ansible-playbook \
                -i "${WORKSPACE}/tests/inventory" \
                --syntax-check \
                "${WORKSPACE}/tests/site.yml"

    # Install Minecraft.
    docker exec -t "${container}" ansible-playbook \
                -i "${WORKSPACE}/tests/inventory" \
                -c local \
                "${WORKSPACE}/tests/site.yml"

    # Sleep to allow Minecraft to boot.
    sleep 5

    # Run tests.
    docker exec -t "${container}" rspec "${WORKSPACE}/tests/spec/minecraft_spec.rb"
  done
}

trap cleanup EXIT

main "${@}"
