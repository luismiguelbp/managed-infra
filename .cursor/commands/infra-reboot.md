# Infra Reboot

## Overview

Reboot all configured Pis, or on one host when a hostname is passed (e.g. `/infra-reboot edge-node-2`).

Uses `./bin/infra-reboot` (Ansible `common` role, `--tags reboot`).

## Host parameter

- **No parameter** → reboot all hosts in inventory
- **One hostname** → add `--limit <hostname>` (inventory name from `./bin/infra-list-hosts`, not DNS)

Examples in this repo use template names (`edge-node-1`, `edge-node-2`). Live inventory comes from `MANAGED_INFRA_CONFIG_SRC` (see `.cursor/rules/templates-only.mdc`).

## Steps

1. **Confirm repo** — run from managed-infra root
2. **List hosts** — `./bin/infra-list-hosts`
3. **Ping** — `./bin/infra-ping` or `./bin/infra-ping --limit <host>`
4. **Confirm targets** — state which host(s) will reboot before running (fleet-wide reboot is disruptive)
5. **Reboot** — `./bin/infra-reboot` or `./bin/infra-reboot --limit <host>`
6. **Wait and verify** — after ~60s, `./bin/infra-ping` on the same scope

## Rules

- Do not reboot without confirming the target host list with the user when more than one host is affected
- If ping fails after reboot, wait and retry once before reporting failure

## Output

Hosts rebooted, ping result after recovery, any failures.
