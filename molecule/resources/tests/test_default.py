import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_java_package_exists(host):
    if host.system_info.distribution == "centos":
        java = "java-1.8.0-openjdk"
    elif host.system_info.distribution == "debian":
        java = "openjdk-8-jdk"
    else:
        java = "default-jdk"

    host.package(java).is_installed


def test_gameport_is_open(host):
    host.socket("tcp://0.0.0.0:25565").is_listening


def test_rconport_is_open(host):
    host.socket("tcp://0.0.0.0:25564").is_listening

def test_eula_exists_exists(host):
    f = host.file("/opt/minecraft/server/shared/eula.txt")
    assert "eula=true" in f.content_string
    assert f.user == "spigot"
    assert f.group == "spigot"
