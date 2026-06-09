# Infra Deploy

## Overview

Run a full fleet bootstrap on all configured Linux hosts, or on one host when a hostname is passed (e.g. `/infra-deploy edge-node-1`).

Uses `./bin/infra-bootstrap` from the managed-infra repo root (OS update, packages, Docker, UFW, edge stack).

## Host parameter

- **No parameter** → deploy all hosts in inventory
- **One hostname** → add `--limit <hostname>` (inventory name from `./bin/infra-list-hosts`, not DNS)

Examples in this repo use template names (`edge-node-1`, `edge-node-2`, `edge-node-3`). Live inventory comes from `MANAGED_INFRA_CONFIG_SRC` (see `.cursor/rules/templates-only.mdc`).

## Steps

1. **Confirm repo** — run from managed-infra root; read `.cursor/skills/infra-deploy/SKILL.md` for two-repo rules
2. **List hosts** — `./bin/infra-list-hosts`
3. **Ping** — `./bin/infra-ping` or `./bin/infra-ping --limit <host>`
4. **Deploy** — `./bin/infra-bootstrap` or `./bin/infra-bootstrap --limit <host>`
5. **Verify** — `./bin/infra-docker-status` (add `--limit <host>` when scoped to one host)

## Rules

- Do not read or print secrets from `MANAGED_INFRA_CONFIG_SRC`
- If ping fails, stop and report; do not run bootstrap
- For Compose-only updates after initial bootstrap, suggest `./bin/infra-deploy-edge-stack` instead

## Output

Summarize: hosts targeted, bootstrap result (ok/changed/failed), container status per host.
