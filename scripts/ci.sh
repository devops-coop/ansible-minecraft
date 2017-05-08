#!/usr/bin/env bash
set -euxo pipefail
IFS=$'\n\t'

declare -r OS=${1:-${OS}}
declare -r PROCESS_CONTROL=${2:-${PROCESS_CONTROL}}
declare -r SERVER=${3:-${SERVER}}
declare -r WORKSPACE=${WORKSPACE:-/tmp/ansible-minecraft}

function cleanup() {
  docker-compose stop "${OS}"
  docker-compose rm -f "${OS}"
}

function debug() {
  local container="$(docker-compose ps -q "${OS}")"
  docker exec -it "${container}" /bin/bash
}

function main() {
  docker-compose up -d "${OS}"

  local container="$(docker-compose ps -q "${OS}")"

  # Install role.
  docker cp . "${container}:${WORKSPACE}"

  docker exec -t "${container}" mkdir "${WORKSPACE}/tests/roles" 
  docker exec -t "${container}" ln -s "${WORKSPACE}/" "${WORKSPACE}/tests/roles/devops-coop.minecraft" 
  
  # Validate syntax
  docker exec -t "${container}" ansible-playbook \
              -i "${WORKSPACE}/tests/inventory" \
              --syntax-check \
              -v \
              --extra-vars="minecraft_process_control=${PROCESS_CONTROL} minecraft_server=${SERVER}" \
              "${WORKSPACE}/tests/${SERVER}.yml"

  # Install Minecraft.
  docker exec -t "${container}" ansible-playbook \
              -i "${WORKSPACE}/tests/inventory" \
              -c local \
              -v \
              --extra-vars="minecraft_process_control=${PROCESS_CONTROL} minecraft_server=${SERVER}" \
              "${WORKSPACE}/tests/${SERVER}.yml"

  # Sleep to allow Minecraft to boot.
  # FIXME: A retry loop checking if it has launched yet would be better.
  sleep 30

  # Run tests.
  docker exec -t "${container}" rspec "${WORKSPACE}/tests/spec/${SERVER}_spec.rb"
}

[[ -z "${CI:-}" ]] && trap debug ERR
trap cleanup EXIT

main "${@}"
