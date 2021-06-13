import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_gameport_is_open(host):
    host.socket("tcp://0.0.0.0:25565").is_listening


def test_rconport_is_open(host):
    host.socket("tcp://0.0.0.0:25564").is_listening


def test_eula_exists_exists(host):
    f = host.file("/opt/minecraft/server/shared/eula.txt")
    assert "eula=true" in f.content_string
