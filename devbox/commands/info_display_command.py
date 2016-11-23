import click
from devbox.utilities.deployment_engine_factory import DeploymentEngineFactory
from devbox.utilities.manifest_parser import ManifestParser
from terminaltables import AsciiTable


class InfoDisplayCommandExecutor(object):

    def __init__(self, manifest_parser=None, deployment_engine_factory=None):
        self._deployment_engine_factory = deployment_engine_factory or DeploymentEngineFactory()
        self._manifest_parser = manifest_parser or ManifestParser()

    def display_info(self, path, deploy):
        click.echo(u'Parsing manifest {}'.format(path))
        manifest = self._manifest_parser.parse(path)

        deployment_engine = self._deployment_engine_factory.get_deployment_engine(deploy)
        nodes = deployment_engine.get_node_details(manifest)

        table = AsciiTable([['Name', 'Image', 'IP Address', 'Ports', 'Status', 'Command']])
        table.outer_border = False
        table.inner_column_border = False
        for node in nodes:
            row = [node.name, node.image, node.ip_address, node.ports, node.status, node.command]
            table.table_data.append(row)

        click.echo(table.table)
