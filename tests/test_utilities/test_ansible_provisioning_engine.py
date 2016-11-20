import unittest
from devbox.utilities.ansible_provisioning_engine import AnsibleProvisioningEngine


class TestAnsibleProvisioningEngine(unittest.TestCase):
    def test_provision(self):
        AnsibleProvisioningEngine()._provision_node('python_server1')

