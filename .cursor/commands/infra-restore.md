# Infra Restore

## Overview

Push a backup mirror from `MANAGED_INFRA_BACKUP_DEST` onto a **single** deployed host. Manual operation only — not part of bootstrap or deploy flows.

## Host parameter

- **Required** — `--limit <hostname>` (inventory name from `./bin/infra-list-hosts`, not DNS)
- **Optional source override** — `-e edge_stack_restore_source=<backup-folder-name>` when the mirror folder name differs from the target host

Examples in this repo use template names (`edge-node-1`, `edge-node-2`, `edge-node-3`). Live inventory comes from `MANAGED_INFRA_CONFIG_SRC`.

## Steps

1. **Confirm repo** — run from managed-infra root
2. **Set backup root** — ensure `MANAGED_INFRA_BACKUP_DEST` is set in gitignored `.env`
3. **Confirm mirror exists** — `ls -la "$MANAGED_INFRA_BACKUP_DEST/<source-host>"`
4. **Bootstrap target** (new host only) — `./bin/infra-bootstrap --limit <host>`
5. **Ping** — `./bin/infra-ping --limit <host>`
6. **Run restore** — `./bin/infra-restore-edge-stack --limit <host>`
7. **Verify** — `./bin/infra-docker-status --limit <host>`

## Options

```bash
# Restore edge-node-1 mirror onto edge-node-1 (hardware replacement)
./bin/infra-restore-edge-stack --limit edge-node-1

# Restore edge-node-1 mirror onto edge-node-2 (new host, same role)
./bin/infra-restore-edge-stack --limit edge-node-2 -e edge_stack_restore_source=edge-node-1

# Also copy mirrored .env and reconcile COMPOSE_* for the target
./bin/infra-restore-edge-stack --limit edge-node-1 -e edge_stack_restore_env=true

# Keep services running during file restore (not recommended for stateful services)
./bin/infra-restore-edge-stack --limit edge-node-3 -e edge_stack_restore_stop_services=false
```

## Rules

- Do not read or print secret values from `.env` files
- Do not commit backup data or mirrored `.env` files
- Restore overwrites target `data/` directories and imports dumps under `dumps/` when present in the mirror
- Default restores data only; `.env` stays on the target unless `edge_stack_restore_env=true`
- If restoring encrypted application data without `.env`, ensure credential secrets on the target match the backup

## Output

Restored runtime data under `/opt/docker/data/` on the target and optional imports from `dumps/` per host profile.
