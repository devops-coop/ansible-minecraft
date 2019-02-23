import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_minecraft_spigot_service(host):
    service = host.service("spigot")
    assert service.is_running
    assert service.is_enabled


def test_plugins_dir_exists(host):
    f = host.file("/opt/minecraft/plugins/current")
    assert f.exists
    assert f.is_directory
    assert f.is_symlink
    assert f.linked_to == "/opt/minecraft/plugins/releases/minimal"


def test_plugins_shared_dir_exists(host):
    f = host.file("/opt/minecraft/plugins/shared")
    assert f.exists
    assert f.is_directory


def test_plugins_jar_exists(host):
    f = host.file("/opt/minecraft/plugins/shared/Vault.jar")
    assert f.exists
    assert f.is_file
    assert f.is_symlink
    assert f.linked_to == "/opt/minecraft/plugins/releases/minimal/Vault.jar"


def test_plugins_jar_in_server_exists(host):
    f = host.file("/opt/minecraft/server/shared/plugins/Vault.jar")
    assert f.exists
    assert f.is_file
    assert f.is_symlink
    assert f.linked_to == "/opt/minecraft/plugins/releases/minimal/Vault.jar"
