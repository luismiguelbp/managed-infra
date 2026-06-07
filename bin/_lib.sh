#!/usr/bin/env bash
# Shared helpers for bin/ scripts. Source from other scripts; do not run directly.

project_root() {
  cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd
}

ansible_cd() {
  cd "$(project_root)/ansible"
}

ensure_ansible() {
  if ! command -v ansible-playbook >/dev/null 2>&1; then
    echo "ansible-playbook not found. Install with: brew install ansible" >&2
    exit 1
  fi
}

load_project_env() {
  local env_file
  env_file="$(project_root)/.env"
  if [[ -f "$env_file" ]]; then
    set -a
    # shellcheck source=/dev/null
    source "$env_file"
    set +a
  fi
}

# Set by verify_managed_infra_config_src for ansible wrappers.
MANAGED_INFRA_INVENTORY_FILE=""
MANAGED_INFRA_DOCKER_SRC=""

# Required deploy files under MANAGED_INFRA_CONFIG_SRC/docker (must not be repo templates).
EDGE_STACK_REQUIRED_FILES=(
  compose.yml
  compose-mosquitto.yml
  compose-node-red.yml
  env.example
)

# Verify external configs and set MANAGED_INFRA_* paths for Ansible.
# Refuses repo templates so deployments always use MANAGED_INFRA_CONFIG_SRC.
verify_managed_infra_config_src() {
  load_project_env

  if [[ -z "${MANAGED_INFRA_CONFIG_SRC:-}" ]]; then
    echo "MANAGED_INFRA_CONFIG_SRC is not set. Add it to .env (see .env.example)." >&2
    echo "Refusing to run: this repository contains templates only." >&2
    exit 1
  fi

  if [[ ! -d "$MANAGED_INFRA_CONFIG_SRC" ]]; then
    echo "MANAGED_INFRA_CONFIG_SRC not found: $MANAGED_INFRA_CONFIG_SRC" >&2
    exit 1
  fi

  local inventory_src="$MANAGED_INFRA_CONFIG_SRC/ansible/inventory/hosts.yml"
  if [[ ! -f "$inventory_src" ]]; then
    echo "MANAGED_INFRA_CONFIG_SRC is missing ansible/inventory/hosts.yml" >&2
    exit 1
  fi

  local repo_inventory
  repo_inventory="$(cd "$(project_root)/ansible/inventory" && pwd)/hosts.yml"
  if [[ "$(cd "$(dirname "$inventory_src")" && pwd)/hosts.yml" == "$repo_inventory" ]]; then
    echo "MANAGED_INFRA_CONFIG_SRC/ansible/inventory points at this repo's inventory (templates)." >&2
    exit 1
  fi

  local docker_src="$MANAGED_INFRA_CONFIG_SRC/docker"
  if [[ ! -d "$docker_src" ]]; then
    echo "MANAGED_INFRA_CONFIG_SRC has no docker/ directory: $docker_src" >&2
    exit 1
  fi

  local repo_docker
  repo_docker="$(cd "$(project_root)/docker" && pwd)"
  if [[ "$(cd "$docker_src" && pwd)" == "$repo_docker" ]]; then
    echo "MANAGED_INFRA_CONFIG_SRC/docker points at this repo's docker/ (templates)." >&2
    exit 1
  fi

  local missing=()
  local file
  for file in "${EDGE_STACK_REQUIRED_FILES[@]}"; do
    if [[ ! -f "$docker_src/$file" ]]; then
      missing+=("$file")
    fi
  done
  if [[ ${#missing[@]} -gt 0 ]]; then
    echo "MANAGED_INFRA_CONFIG_SRC/docker is missing required files: ${missing[*]}" >&2
    exit 1
  fi

  MANAGED_INFRA_INVENTORY_FILE="$inventory_src"
  MANAGED_INFRA_DOCKER_SRC="$docker_src"

  echo "Using inventory from: $(dirname "$inventory_src")" >&2
  echo "Using edge stack configs from: $docker_src" >&2
}
