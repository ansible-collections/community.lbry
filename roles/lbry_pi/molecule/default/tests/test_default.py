import os
import yaml

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def include_vars(host):
    ansible = host.ansible("include_vars",
                           'file="../../defaults/main.yml"',
                           False,
                           False)
    return ansible


def test_lbry_user(host):
    lbry = include_vars(host)["ansible_facts"].get("lbry_user", "lbry")
    assert host.user(lbry)


def test_lbry_user_group(host):
    lbry = include_vars(host)["ansible_facts"].get("lbry_user", "lbry")
    lbry_group = include_vars(host)["ansible_facts"].get("lbry_group", "lbry")
    assert lbry_group in host.user(lbry).groups


def test_python37(host):
    f = host.file("/usr/local/bin/python3.7")
    assert f.exists


def test_lbry_exec_files(host):
    files = ['/usr/bin/lbrycrdd',
             '/usr/bin/lbrycrd-tx',
             '/usr/bin/lbrycrd-cli',
             '/usr/local/bin/lbrynet']
    file_exists = []
    for exec in files:
        f = host.file(exec)
        file_exists.append(f.exists)
    assert all(file_exists)


def test_lbrycrdd_service(host):
    s = host.service("lbrycrdd")
    assert s.is_running
    assert s.is_enabled


def test_lbrynet_service(host):
    s = host.service("lbrynet")
    assert s.is_running
    assert s.is_enabled


def test_lbrycrdd_port(host):
    s = host.socket("tcp://0.0.0.0:{0}".format(29245))
    assert s.is_listening


def test_docker_service(host):
    s = host.service("docker")
    assert s.is_running
    assert s.is_enabled


def test_elastic_port(host):
    s = host.socket("tcp://127.0.0.1:{0}".format(9200))
    assert s.is_listening


def test_wallet_port(host):
    s = host.socket("tcp://127.0.0.1:{0}".format(50001))
    assert s.is_listening


def test_lbrynet_ports(host):
    s = host.socket("tcp://127.0.0.1:{0}".format(5279))
    assert s.is_listening
    s = host.socket("tcp://127.0.0.1:{0}".format(5280))
    assert s.is_listening
