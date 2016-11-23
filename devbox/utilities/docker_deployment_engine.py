import os
import tarfile
import click
import docker
from io import BytesIO
import time
from toscaparser.tosca_template import ToscaTemplate
import collections
from devbox.utilities.base_deployment_engine import BaseDeploymentEngine
from devbox.exceptions.deployment_error import DeploymentError


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
        cli = docker.from_env()
        containers = self._get_containers(cli)
        results = {}
        for node in manifest.topology_template.nodetemplates:
            if node.name in containers:
                raise DeploymentError('Node ' + node.name + ' already exists')
            results[node.name] = self._deploy_node(node, cli)
        return results

    def get_node_details(self, manifest):
        cli = docker.from_env()
        containers_dict = self._get_containers(cli)
        all_container_details = []
        for node in manifest.topology_template.nodetemplates:
            if node.name in containers_dict:
                container_details = self._get_container_details(cli, containers_dict[node.name])
                all_container_details.append(container_details)
        return all_container_details

    def destroy(self, manifest):
        cli = docker.from_env()
        containers_dict = self._get_containers(cli)
        for node in manifest.topology_template.nodetemplates:
            if node.name in containers_dict:
                container_details = self._get_container_details(cli, containers_dict[node.name])
                if container_details.running:
                    click.echo('Stopping node {0}'.format(node.name))
                    cli.stop(containers_dict[node.name])
                click.echo('Destroying node {0}'.format(node.name))
                cli.remove_container(containers_dict[node.name])

    def copy(self, manifest):
        results = {}
        cli = docker.from_env()
        containers_dict = self._get_containers(cli)
        for node in manifest.topology_template.nodetemplates:
            if node.name not in containers_dict:
                raise DeploymentError('Node ' + node.name + ' does not exists. Deploy it first')
            if 'artifacts' in node.entity_tpl and node.entity_tpl['artifacts']:
                artifacts = node.entity_tpl['artifacts']
                for artifact in artifacts:
                    artifact_file = artifacts[artifact]['file']
                    if not os.path.exists(artifact_file):
                        raise DeploymentError('Artifacts file {} is missing'.format(artifact_file))
                    click.echo('Copying artifact {0} to {1}'.format(node.name, node.name))
                    with self._create_archive(artifact_file) as archive:
                        cli.put_archive(container=containers_dict[node.name],
                                        path='/tmp',
                                        data=archive)
            # results[node.name] = self._copy(node, cli, containers_dict[node.name])
        return results

    @staticmethod
    def _get_containers(cli):
        """
        Returns dictionary of all the containers
        :param cli:
        :return:
        :rtype dict
        """
        containers = cli.containers(all=True)
        containers_dict = {container['Names'][0].strip('/'): container['Id'] for container in containers}
        return containers_dict

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
        ports = self._get_property_value(properties, DEPLOYMENT_PORTS)
        images = cli.images(name=image, quiet=False,all=True)
        if not images:
            if ':' not in image:
                image += ':latest'
            click.echo('Downloading image {0}'.format(image))
            for line in cli.pull(repository=image, stream=True):
                click.echo(line)
        click.echo('Creating node {0}'.format(node.name))
        container_id = cli.create_container(name=node.name,
                                            image=image,
                                            command=deployment_command,
                                            ports=ports,
                                            tty=True,
                                            stdin_open=True)
        click.echo('Starting node {0}'.format(node.name))
        cli.start(container_id)
        return self._get_container_details(cli, container_id)

    @staticmethod
    def _get_container_details(cli, container_id):
        container = cli.inspect_container(container=container_id)
        container_details = collections.namedtuple('DeployResult',
                                                   ['name', 'ip_address', 'running', 'image', 'command', 'ports',
                                                    'status'])
        container_details.name = container[u'Name']
        container_details.ip_address = container[u'NetworkSettings'][u'IPAddress']
        container_details.running = container[u'State'][u'Running']
        container_details.image = container[u'Config'][u'Image']
        container_details.command = container[u'Config'][u'Cmd']
        container_details.ports = container[u'NetworkSettings'][u'Ports']
        container_details.status = container[u'State'][u'Status']
        return container_details

    @staticmethod
    def _get_property_value(properties, property_name):
        if property_name not in properties:
            raise DeploymentError('Property {0} is not set', property_name)
        return properties[property_name].default

    @staticmethod
    def _create_archive(artifact_file):
        pw_tarstream = BytesIO()
        pw_tar = tarfile.TarFile(fileobj=pw_tarstream, mode='w')
        file_data = open(artifact_file, 'r').read()
        tarinfo = tarfile.TarInfo(name=artifact_file)
        tarinfo.size = len(file_data)
        tarinfo.mtime = time.time()
        # tarinfo.mode = 0600
        pw_tar.addfile(tarinfo, BytesIO(file_data))
        pw_tar.close()
        pw_tarstream.seek(0)
        return pw_tarstream
