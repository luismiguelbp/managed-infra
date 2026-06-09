# Infra Status

## Overview

Check fleet health on all configured Linux hosts, or on one host when a hostname is passed (e.g. `/infra-status edge-node-1`).

## Host parameter

- **No parameter** → status for all hosts in inventory
- **One hostname** → add `--limit <hostname>` (inventory name from `./bin/infra-list-hosts`, not DNS)

Examples in this repo use template names (`edge-node-1`, `edge-node-2`, `edge-node-3`). Live inventory comes from `MANAGED_INFRA_CONFIG_SRC` (see `.cursor/rules/templates-only.mdc`).

## Steps

1. **Confirm repo** — run from managed-infra root
2. **List hosts** — `./bin/infra-list-hosts`
3. **Ping** — `./bin/infra-ping` or `./bin/infra-ping --limit <host>`
4. **Docker + system status** — `./bin/infra-docker-status` (or `./bin/infra-docker-status --limit <host>`)

## Rules

- Do not read or print secrets from `MANAGED_INFRA_CONFIG_SRC`
- If ping fails for a host, report it separately from container status

## Output

Per host: ping ok/fail, Docker daemon state, edge stack present or not, container names/status/health, compose version, uptime, root and edge stack path disk usage.
