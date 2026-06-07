"""Structural tests for per-host edge stack profiles in template inventory."""

from contract_helpers import DOCKER_DIR, TEMPLATE_HOST_VARS_DIR, parse_host_var_list


def test_template_host_vars_compose_files_exist() -> None:
    """Every compose file in template host_vars exists under docker/."""
    for host_vars_file in sorted(TEMPLATE_HOST_VARS_DIR.glob("*.yml")):
        compose_files = parse_host_var_list(host_vars_file, "edge_stack_compose_files")
        if compose_files is None:
            continue
        for compose_file in compose_files:
            assert (DOCKER_DIR / compose_file).is_file(), (
                f"{host_vars_file.name}: missing {compose_file}"
            )


def test_template_host_vars_include_base_compose_file() -> None:
    """Hosts with an edge stack profile always include compose.yml."""
    for host_vars_file in sorted(TEMPLATE_HOST_VARS_DIR.glob("*.yml")):
        compose_files = parse_host_var_list(host_vars_file, "edge_stack_compose_files")
        if compose_files is None:
            continue
        assert "compose.yml" in compose_files, host_vars_file.name
