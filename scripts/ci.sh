#!/usr/bin/env bash
set -euxo pipefail
IFS=$'\n\t'

declare -r OS=${1:-${OS}}
declare -r PROCESS_CONTROL=${2:-${PROCESS_CONTROL}}
declare -r WORKSPACE=${WORKSPACE:-/tmp/ansible-minecraft}

function cleanup() {
  docker-compose stop "${OS}"
  docker-compose rm -f "${OS}"
}

function main() {
  docker-compose up -d "${OS}"

  local container="$(docker-compose ps -q "${OS}")"

  # Install role.
  docker cp . "${container}:${WORKSPACE}"

  # Validate syntax
  docker exec -t "${container}" ansible-playbook \
              -i "${WORKSPACE}/tests/inventory" \
              --syntax-check \
              --extra-vars="minecraft_process_control=${PROCESS_CONTROL}" \
              "${WORKSPACE}/tests/site.yml"

  # Install Minecraft.
  docker exec -t "${container}" ansible-playbook \
              -i "${WORKSPACE}/tests/inventory" \
              -c local \
              --extra-vars="minecraft_process_control=${PROCESS_CONTROL}" \
              "${WORKSPACE}/tests/site.yml"

  # Sleep to allow Minecraft to boot.
  # FIXME: A retry loop checking if it has launched yet would be better.
  sleep 10

  # Run tests.
  docker exec -t "${container}" rspec "${WORKSPACE}/tests/spec/minecraft_spec.rb"
}

trap cleanup EXIT

main "${@}"
