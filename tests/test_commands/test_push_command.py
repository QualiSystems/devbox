import os

from pyfakefs import fake_filesystem_unittest
from commands.push_command import PushCommandExecutor


class TestPushCommand(fake_filesystem_unittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_build_package_package_created(self):
        # Arrange
        self.fs.CreateFile('my-app/devbox.yaml', contents="""
tosca_definitions_version: tosca_simple_yaml_1_0

metadata:
  template_name: Python Client Server
  template_author: DevBox
  template_version: 1.0.0

topology_template:
  node_templates:
    python_server1:
      type: tosca.nodes.Python
    python_client1:
      type: tosca.nodes.Python

node_types:
  tosca.nodes.Python:
    derived_from: tosca.nodes.SoftwareComponent
    properties:
      ansible_playbook:
        type: string
        default: meantheory.python
      docker_image:
        type: string
        default: rastasheep/ubuntu-sshd
      ports:
        type: list
        default: []
""")

        os.chdir('my-app')

        command_executor = PushCommandExecutor()

        # Act
        command_executor.push('devbox.yaml', 'docker', 'ansible')
