import click

from devbox.utilities.base_deployment_engine import BaseDeploymentEngine
from devbox.exceptions.deployment_error import DeploymentError
from docker import Client
from toscaparser.tosca_template import ToscaTemplate

# BASE_URL = 'tcp://127.0.0.1:2375'
BASE_URL = 'unix://var/run/docker.sock'

DEPLOYMENT_IMAGE = 'deployment_image'
DEPLOYMENT_COMMAND = 'deployment_command'
DEPLOYMENT_PORTS = 'deployment_ports'


class DockerDeploymentEngine(BaseDeploymentEngine):
    def deploy(self, manifest):
        """

        :param manifest:
        :type manifest: ToscaTemplate
        :return:
        """
        cli = Client(base_url=BASE_URL)
        for node in manifest.topology_template.nodetemplates:
            self._deploy_node(node, cli)

    def destroy(self, manifest):
        cli = Client(base_url=BASE_URL)
        containers = cli.containers(all=True)
        containers_dict = {container['Names'][0].strip('/'): container['Id'] for container in containers}
        for node in manifest.topology_template.nodetemplates:
            if node.name in containers_dict:
                click.echo('Destroying {0}'.format(node.name))
                cli.remove_container(containers_dict[node.name])

    def _deploy_node(self, node, cli):
        """

        :param node:
        :type node: toscaparser.nodetemplate.NodeTemplate
        :param cli
        :type cli: docker.Client
        :return:
        """
        click.echo('Deploying {0}'.format(node.name))
        properties = node.get_properties()
        image = self._get_property_value(properties, DEPLOYMENT_IMAGE)
        deployment_command = self._get_property_value(properties, DEPLOYMENT_COMMAND)
        ports = self._get_property_value(properties, DEPLOYMENT_PORTS)
        images = cli.images(name=image, quiet=False,all=True)
        if not images:
            if ':' not in image:
                image += ':latest'
            for line in cli.pull(image, stream=True):
                click.echo(line)
        container_id = cli.create_container(name=node.name,
                                            image=image,
                                            command=deployment_command,
                                            ports=ports)
        cli.start(container_id)

    @staticmethod
    def _get_property_value(properties, property_name):
        if property_name not in properties:
            raise DeploymentError('Property {0} is not set', property_name)
        return properties[property_name].default
