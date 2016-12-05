import unittest
from devbox.utilities.ansible_provisioning_engine import NewAnsibleProvisioningEngine


class TestAnsibleProvisioningEngine(unittest.TestCase):
    def test_new_provision(self):
        NewAnsibleProvisioningEngine()._provision_node('python_server1','172.17.0.3', '/home/ronen-a/work/templatetest/template1/playbook.yaml')

