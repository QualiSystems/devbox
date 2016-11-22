import os
from pyfakefs import fake_filesystem_unittest
from devbox.commands.destroy_command import DestroyCommandExecutor


class TestDestroyCommand(fake_filesystem_unittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_app_destroyed(self):
        # Arrange
        self.fs.CreateFile('my-app/devbox.yaml', contents="""
tosca_definitions_version: tosca_simple_yaml_1_0

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
      deployment_image:
        type: string
        default: rastasheep/ubuntu-sshd
      deployment_command:
        type: string
        default: /bin/sh
      deployment_ports:
        type: list
        default: [22, 123]
      provisioning_instruction:
        type: string
        default: meantheory.python
""")

        os.chdir('my-app')

        command_executor = DestroyCommandExecutor()

        # Act
        command_executor.destroy('devbox.yaml', 'docker')
