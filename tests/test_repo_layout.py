"""Structural tests for repository layout and Ansible/Docker alignment."""

from contract_helpers import (
    DOCKER_DIR,
    MANUAL_EDGE_STACK_DATA_FILES,
    PROJECT_ROOT,
    parse_ansible_list,
    parse_env_example_var,
)


def test_edge_stack_compose_files_exist() -> None:
    """Every compose file referenced by Ansible exists under docker/."""
    for compose_file in parse_ansible_list("edge_stack_compose_files"):
        assert (DOCKER_DIR / compose_file).is_file(), compose_file


def test_compose_file_list_matches_env_example() -> None:
    """docker/env.example COMPOSE_FILE matches Ansible edge_stack_compose_files."""
    ansible_files = parse_ansible_list("edge_stack_compose_files")
    env_files = parse_env_example_var("COMPOSE_FILE").split(",")
    assert env_files == ansible_files


def test_edge_stack_data_files_exist_in_repo() -> None:
    """Shipped edge stack data files exist under docker/ (manual files excluded)."""
    for data_file in parse_ansible_list("edge_stack_data_files"):
        if data_file in MANUAL_EDGE_STACK_DATA_FILES:
            continue
        assert (DOCKER_DIR / data_file).is_file(), data_file


def test_manual_edge_stack_data_files_are_gitignored() -> None:
    """Files created on each Pi are excluded from version control."""
    gitignore = (PROJECT_ROOT / ".gitignore").read_text()
    for data_file in MANUAL_EDGE_STACK_DATA_FILES:
        assert f"docker/{data_file}" in gitignore, data_file
