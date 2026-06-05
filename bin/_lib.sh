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
