import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_minecraft_service_group_exists(host):
    f = host.group("minecraft")
    assert f.exists


def test_minecraft_service_user_exists(host):
    f = host.user("minecraft")
    assert f.group == 'minecraft'


def test_server_jar_exists(host):
    f = host.file('/opt/minecraft/server/releases/1.9/minecraft_server.jar')
    assert f.exists
    assert f.is_file
    assert f.user == 'minecraft'
    assert f.group == 'minecraft'


def test_server_current_symlink_exists(host):
    f = host.file('/opt/minecraft/server/current')
    assert f.is_symlink
    assert f.is_directory
    assert f.linked_to == '/opt/minecraft/server/releases/1.9'


def test_server_shared_symlink_exists(host):
    f = host.file('/opt/minecraft/server/shared/minecraft_server.jar')
    assert f.is_symlink
    assert f.linked_to == '/opt/minecraft/server/releases/1.9/minecraft_server.jar'


def test_eula_exists_exists(host):
    f = host.file('/opt/minecraft/server/shared/eula.txt')
    assert f.content == "eula=true"
    assert f.user == 'minecraft'
    assert f.group == 'minecraft'
