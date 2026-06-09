# Infra Backup

## Overview

Mirror edge stack runtime data from each host to your Mac under `MANAGED_INFRA_BACKUP_DEST`.

## Host parameter

- **No parameter** → backup all hosts in inventory
- **One hostname** → add `--limit <hostname>` (inventory name from `./bin/infra-list-hosts`, not DNS)

Examples in this repo use template names (`edge-node-1`, `edge-node-2`, `edge-node-3`). Live inventory comes from `MANAGED_INFRA_CONFIG_SRC`.

## Steps

1. **Confirm repo** — run from managed-infra root
2. **Set backup root** — ensure `MANAGED_INFRA_BACKUP_DEST` is set in gitignored `.env`
3. **List hosts** — `./bin/infra-list-hosts`
4. **Run backup** — `./bin/infra-backup-edge-stack` (or `./bin/infra-backup-edge-stack --limit <host>`)
5. **Check mirror** — `ls -la "$MANAGED_INFRA_BACKUP_DEST/<host>"`

## Rules

- Do not read or print secret values from `.env` files
- Do not commit backup data or mirrored `.env` files
- Keep `MANAGED_INFRA_BACKUP_DEST` outside git-tracked directories

## Output

Per host mirror at `MANAGED_INFRA_BACKUP_DEST/<host>/` with `.env` (if present), `manifest.json`, mirrored `data/` folders, and `dumps/postgresql.sql` on database hosts.
