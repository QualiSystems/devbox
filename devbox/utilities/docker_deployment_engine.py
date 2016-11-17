from devbox.utilities.base_deployment_engine import BaseDeploymentEngine
from docker import Client
from toscaparser.tosca_template import ToscaTemplate


class DockerDeploymentEngine(BaseDeploymentEngine):
    def deploy(self, manifest):
        """

        :param manifest:
        :type manifest: ToscaTemplate
        :return:
        """
        cli = Client(base_url='tcp://192.168.11.1:2375')
        # node : NodeTemplate
        for node in manifest.topology_template.nodetemplates:
            self._deploy_node(node, cli)

    def _deploy_node(self, node, cli):
        """

        :param node:
        :type node: toscaparser.nodetemplate.NodeTemplate
        :param cli
        :type cli: docker.Client
        :return:
        """
        properties = node.get_properties()
        if 'docker_image' not in properties:
            return
        image = properties['docker_image'].default
        if not image:
            return
        container_id = cli.create_container(image=image,
                                            command='/bin/sh',
                                            ports=[])



