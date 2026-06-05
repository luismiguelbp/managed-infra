# managed-infra

Infrastructure-as-code for a small Raspberry Pi fleet. Ansible and Docker Compose on the devices; wrapper scripts on your Mac.

## Contents

- Ansible inventory and `site` playbook: [docs/ansible.md](docs/ansible.md)
- Edge stack (Mosquitto + Node-RED): [docker/README.md](docker/README.md)
- Helper scripts in `bin/` (`ansible-*`, `infra-*` prefixes)

## Prerequisites

- Python 3.10+ (for contract tests)
- Ansible on the control machine (`brew install ansible`)
- SSH key access to each Pi

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Test

```bash
pytest
```

## Ansible (fleet bootstrap)

```bash
./bin/infra-list-hosts
./bin/infra-ping
./bin/infra-bootstrap --check
./bin/infra-bootstrap
./bin/infra-deploy-edge-stack
```

See [docs/ansible.md](docs/ansible.md) for all helper scripts, limits, and options.

Install Ansible collections once: `ansible-galaxy collection install -r ansible/requirements.yml`

Edge stack credentials are set manually on each Pi. See [docker/README.md](docker/README.md#credentials).

## Workflow

1. Cursor helps write playbooks, Compose files, and configs in this repo.
2. You review the changes.
3. You run Ansible via `bin/` helper scripts from your Mac.
