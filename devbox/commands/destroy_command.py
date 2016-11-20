import click

from devbox.utilities.manifest_parser import ManifestParser
from devbox.utilities.deployment_engine_factory import DeploymentEngineFactory


class DestroyCommandExecutor(object):
    def __init__(self, manifest_parser=None, deployment_engine_factory=None):
        self._deployment_engine_factory = deployment_engine_factory or DeploymentEngineFactory()
        self._manifest_parser = manifest_parser or ManifestParser()

    def destroy(self, manifest_path, deployment_type):
        click.echo(u'Parsing manifest {}'.format(manifest_path))
        manifest = self._manifest_parser.parse(manifest_path)

        click.echo(u'Destroying using {}'.format(deployment_type))
        deployment_engine = self._deployment_engine_factory.get_deployment_engine(deployment_type)
        deployment_engine.destroy(manifest)
