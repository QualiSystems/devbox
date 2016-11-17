from devbox.utilities.base_deployment_engine import BaseDeploymentEngine
from devbox.exceptions.deployment_error import DeploymentError
from docker import Client
from toscaparser.tosca_template import ToscaTemplate

DEPLOYMENT_IMAGE = 'deployment_image'
DEPLOYMENT_COMMAND = 'deployment_command'


class DockerDeploymentEngine(BaseDeploymentEngine):
    def deploy(self, manifest):
        """

        :param manifest:
        :type manifest: ToscaTemplate
        :return:
        """
        cli = Client(base_url='tcp://127.0.0.1:2375')
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
        image = self._get_property_value(properties, DEPLOYMENT_IMAGE)
        deployment_command = self._get_property_value(properties, DEPLOYMENT_COMMAND)
        if not image:
            return
        container_id = cli.create_container(name=node.name,
                                            image=image,
                                            command=deployment_command,
                                            ports=[])

    @staticmethod
    def _get_property_value(properties, property_name):
        if property_name not in properties:
            raise DeploymentError('Property {0} is not set', property_name)
        return properties[property_name].default
