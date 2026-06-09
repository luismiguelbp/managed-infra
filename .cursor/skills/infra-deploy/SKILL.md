---
name: infra-deploy
description: Deploy and operate the managed-infra Raspberry Pi fleet via bin/ scripts and Ansible. Use when running infra-bootstrap, infra-deploy-edge-stack, infra-backup-edge-stack, infra-restore-edge-stack, infra-reboot, fleet status checks, MANAGED_INFRA_CONFIG_SRC, Ansible playbooks, or provisioning Mosquitto and Node-RED on Pis.
---

# managed-infra fleet deploy

Infrastructure-as-code for a small Raspberry Pi fleet. Run all commands from the **managed-infra repo root**.

Follow `.cursor/rules/templates-only.mdc`: examples in this repo use fictional names (`edge-node-1`, `site-a`); live deploys use inventory from `MANAGED_INFRA_CONFIG_SRC`.

## Two-repo model (critical)

| Repo | Role |
|------|------|
| `managed-infra` | Playbooks, roles, **templates** (`docker/`, `ansible/inventory/`) — never deploy as-is |
| `MANAGED_INFRA_CONFIG_SRC` | Real inventory, secrets, production Compose and data files |

Set `MANAGED_INFRA_CONFIG_SRC` in gitignored `.env` (see `.env.example`). Every `bin/ansible-*` and `bin/infra-*` script validates this path and refuses template directories.

**Never** read, echo, or commit secrets from the external config source (`.env`, `passwords_file`).

## Prerequisites

- Ansible: `brew install ansible`
- Collections (once): `ansible-galaxy collection install -r ansible/requirements.yml`
- `.env` with valid `MANAGED_INFRA_CONFIG_SRC`
- SSH key access; passwordless sudo on each Pi (`docs/ansible.md`)

## Script picker

| Goal | Script |
|------|--------|
| Full fleet provisioning (OS, Docker, UFW, edge stack) | `./bin/infra-bootstrap` |
| Edge stack only (Compose, Mosquitto, Node-RED) | `./bin/infra-deploy-edge-stack` |
| Docker + system status | `./bin/infra-docker-status` |
| Backup edge stack data to Mac | `./bin/infra-backup-edge-stack` |
| Restore backup mirror to one host | `./bin/infra-restore-edge-stack` |
| Reboot fleet | `./bin/infra-reboot` |
| Connectivity check | `./bin/infra-ping` |
| List inventory hosts | `./bin/infra-list-hosts` |

All scripts accept Ansible extras: `--limit <host>`, `--check`, `-e key=value`.

At runtime, host names come from `$MANAGED_INFRA_CONFIG_SRC/ansible/inventory/hosts.yml` (inventory name, not DNS). Template names in this repo: `edge-node-1`, `edge-node-2` (see `ansible/inventory/hosts.yml`).

## Deploy workflow

1. `./bin/infra-list-hosts` — confirm targets
2. `./bin/infra-ping` — verify SSH (add `--limit edge-node-1` for one Pi)
3. Run the chosen script (add `--limit <host>` for staged rollout)
4. Verify: `./bin/infra-docker-status`

### Full vs edge-only

- **New Pi or infra change** → `infra-bootstrap`
- **Compose/config change only** → `infra-deploy-edge-stack` (faster; skips OS/Docker/UFW)

### Safety defaults

- Prefer `--limit edge-node-1` (or another single host) for first production run or risky changes
- Do not use `--check` alone to validate UFW on fresh hosts (package install is simulated; UFW tasks may fail)
- Ansible copies `docker/.env` from config-src when present; containers start only when `.env` exists on the Pi
- Existing `mosquitto.conf`, `passwords_file`, and customized `settings.js` on the Pi are **not** overwritten

## Status checks

```bash
./bin/infra-docker-status
./bin/infra-docker-status --limit edge-node-1
```

Add `--limit edge-node-1` for a single Pi.

## Backup mirrors

Set `MANAGED_INFRA_BACKUP_DEST` in gitignored `.env`, then run:

```bash
./bin/infra-backup-edge-stack
./bin/infra-backup-edge-stack --limit edge-node-1
```

Each run mirrors runtime files into `MANAGED_INFRA_BACKUP_DEST/<host>/` (no timestamp subfolders).

## Restore backup mirrors

Manual disaster recovery only — not part of bootstrap or deploy.

```bash
./bin/infra-restore-edge-stack --limit edge-node-1
./bin/infra-restore-edge-stack --limit edge-node-2 -e edge_stack_restore_source=edge-node-1
```

Requires `--limit` with exactly one host. Default source folder matches the limited host; override with `edge_stack_restore_source`. Restores `data/` and `dumps/postgresql.sql` only unless `-e edge_stack_restore_env=true` (reconciles `COMPOSE_FILE` and `COMPOSE_PROJECT_NAME` for the target).

## Credentials (manual, not in Ansible vars)

See `docker/README.md#credentials`: per-Pi `.env`, `mosquitto_passwd`, Node-RED bcrypt hash in `settings.js`.

## Reference

- Full script table and options: `docs/ansible.md`
- Edge stack layout and credentials: `docker/README.md`
- Template inventory: `ansible/inventory/`
