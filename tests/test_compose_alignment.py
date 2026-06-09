"""Structural tests for Docker Compose and Ansible image/network alignment."""

from contract_helpers import (
    DOCKER_DIR,
    parse_ansible_scalar,
    read_compose_images,
)


def test_mosquitto_image_matches_ansible_default() -> None:
    """Mosquitto image in compose matches edge_stack_mosquitto_image."""
    expected = parse_ansible_scalar("edge_stack_mosquitto_image")
    images = read_compose_images(DOCKER_DIR / "compose-mosquitto.yml")
    assert images["mosquitto"] == expected


def test_node_red_image_matches_ansible_default() -> None:
    """Node-RED image in compose matches edge_stack_node_red_image."""
    expected = parse_ansible_scalar("edge_stack_node_red_image")
    images = read_compose_images(DOCKER_DIR / "compose-node-red.yml")
    assert images["node-red"] == expected


def test_grafana_image_matches_ansible_default() -> None:
    """Grafana image in compose matches edge_stack_grafana_image."""
    expected = parse_ansible_scalar("edge_stack_grafana_image")
    images = read_compose_images(DOCKER_DIR / "compose-grafana.yml")
    assert images["grafana"] == expected


def test_postgresql_image_matches_ansible_default() -> None:
    """PostgreSQL image in compose matches edge_stack_postgresql_image."""
    expected = parse_ansible_scalar("edge_stack_postgresql_image")
    images = read_compose_images(DOCKER_DIR / "compose-postgresql.yml")
    assert images["postgresql"] == expected


def test_service_compose_files_use_docker_bridge_network() -> None:
    """Service compose files attach to the shared docker-bridge network."""
    for compose_file in (
        "compose-mosquitto.yml",
        "compose-node-red.yml",
        "compose-postgresql.yml",
        "compose-grafana.yml",
    ):
        content = (DOCKER_DIR / compose_file).read_text()
        assert "docker-bridge" in content, compose_file
