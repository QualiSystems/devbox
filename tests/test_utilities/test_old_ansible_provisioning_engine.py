import unittest
from devbox.utilities.old_ansible_provisioning_engine import AnsibleProvisioningEngine


class TestAnsibleProvisioningEngine(unittest.TestCase):
    def test_provision(self):
        AnsibleProvisioningEngine()._provision_node('python_server1','172.17.0.3', '/home/ronen-a/work/templatetest/template1/playbook.yaml')

