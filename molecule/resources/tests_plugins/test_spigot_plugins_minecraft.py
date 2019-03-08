import os

import pytest
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


@pytest.mark.parametrize(
    "pluginJarFilename", ["permissionsEx", "vault", "tne","LuckPerms"]
)
def test_plugins_install_report_exists(host, pluginJarFilename):
    f = host.file(
        "/opt/minecraft/plugins/releases/minimal/report-" + pluginJarFilename + ".yml"
    )
    assert f.exists
    assert f.is_file


@pytest.mark.parametrize(
    "pluginJarFilename", ["Vault.jar", "PermissionsEx.jar","TNE.jar","LuckPerms.jar"]
)
def test_plugins_jar_exists(host, pluginJarFilename):
    f = host.file("/opt/minecraft/plugins/shared/" + pluginJarFilename)
    assert f.exists
    assert f.is_file
    assert f.is_symlink
    assert f.linked_to == "/opt/minecraft/plugins/releases/minimal/" + pluginJarFilename


@pytest.mark.parametrize(
    "pluginJarFilename", ["Vault.jar", "PermissionsEx.jar","TNE.jar","LuckPerms.jar"]
)
def test_plugins_jar_in_server_exists(host, pluginJarFilename):
    f = host.file("/opt/minecraft/server/shared/plugins/" + pluginJarFilename)
    assert f.exists
    assert f.is_file
    assert f.is_symlink
    assert f.linked_to == "/opt/minecraft/plugins/releases/minimal/" + pluginJarFilename


@pytest.mark.parametrize(
    "configfile", ["PermissionsEx/config.yml","LuckPerms/yaml-storage/groups/config.yml"]
)
def test_plugins_check_plugins_configs(host, configfile):
    f = host.file(
        "/opt/minecraft/plugins/shared/" + configfile
    )
    assert f.exists
    assert f.is_file
