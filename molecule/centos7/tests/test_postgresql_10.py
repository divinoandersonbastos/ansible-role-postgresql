import testinfra.utils.ansible_runner
import os
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('postgresql-10-*')


@pytest.mark.parametrize("name,expected_roles", [
    ('alice', 'alice|f|t|f|f|t|f|-1|********||f||'),
    ('bob', 'bob|f|t|f|t|t|f|-1|********||f||'),
])
def test_user_roles(host, name, expected_roles):
    sql = "SELECT * FROM pg_roles WHERE rolname='%s'" % name
    with host.sudo('postgres'):
        out = host.check_output('psql postgres -c "%s" -At' % sql)
    # Everything except the UID at the end
    assert out.startswith(expected_roles)


def test_version(host):
    out1 = host.check_output('psql --version')
    assert out1.startswith('psql (PostgreSQL) 10.')
