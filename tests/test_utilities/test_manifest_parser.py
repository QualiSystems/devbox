import os
from pyfakefs import fake_filesystem_unittest

from devbox.utilities.manifest_parser import ManifestParser


class TestManifestParser(fake_filesystem_unittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_manifest_parser(self):
        # Arrange
        self.fs.CreateFile('my-app/devbox.yaml', contents="""
    tosca_definitions_version: tosca_simple_yaml_1_0

    topology_template:
      node_templates:
        python_server1:
          type: tosca.nodes.Python
          properties:
            ports_bindings:
              type: string
              default: "{1234:80}"
          artifacts:
            binaries:
              file: binaries.zip
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
            default: [22, 1234]
          ports_bindings:
            type: string
            required: false
          provisioning_instruction:
            type: string
            default: playbook.yaml
    """)

        nodes = ManifestParser().parse('my-app/devbox.yaml')

        self.assertEqual(nodes[0].properties['deployment_ports'], [22, 1234])
        self.assertEqual(nodes[0].properties['ports_bindings'], "{1234:80}")

        self.assertTrue('ports_bindings' not in nodes[1].properties)


    def test_manifest_parser_deployment_path(self):
        # Arrange
        self.fs.CreateFile('my-app/devbox.yaml', contents="""
    tosca_definitions_version: tosca_simple_yaml_1_0

    topology_template:
      node_templates:
        python_server1:
          type: tosca.nodes.Python
          properties:
            ports_bindings:
              type: string
              default: "{1234:80}"
          artifacts:
            binaries:
              file: binaries.zip
              deploy_path: mybin
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
            default: [22, 1234]
          ports_bindings:
            type: string
            required: false
          provisioning_instruction:
            type: string
            default: playbook.yaml
    """)

        nodes = ManifestParser().parse('my-app/devbox.yaml')

        self.assertEqual(nodes[0].properties['deployment_ports'], [22, 1234])
        self.assertEqual(nodes[0].properties['ports_bindings'], "{1234:80}")
        self.assertEqual(nodes[0].artifacts['binaries']['deploy_path'], "mybin")

        self.assertTrue('ports_bindings' not in nodes[1].properties)


