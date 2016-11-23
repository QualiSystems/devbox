import click

from devbox.utilities.deployment_engine_factory import DeploymentEngineFactory
from devbox.utilities.manifest_parser import ManifestParser
from devbox.utilities.provisioning_engine_factory import ProvisioningEngineFactory


class PushCommandExecutor(object):
    def __init__(self, manifest_parser=None, deployment_engine_factory=None, provisioning_engine_factory=None):
        self._provisioning_engine_factory = provisioning_engine_factory or ProvisioningEngineFactory()
        self._deployment_engine_factory = deployment_engine_factory or DeploymentEngineFactory()
        self._manifest_parser = manifest_parser or ManifestParser()

    def push(self, manifest_path, deployment_type, provisioning_type):
        click.echo(u'Parsing manifest {}'.format(manifest_path))
        manifest = self._manifest_parser.parse(manifest_path)

        click.echo(u'Deploying using {}'.format(deployment_type))
        deployment_engine = self._deployment_engine_factory.get_deployment_engine(deployment_type)
        deployment_results = deployment_engine.deploy(manifest)

        click.echo(u'Provisioning using {}'.format(provisioning_type))
        provisioning_engine = self._provisioning_engine_factory.get_provisioning_engine(provisioning_type)
        provisioning_engine.provision(manifest, deployment_results)

        click.echo(u'Copying artifacts')
        deployment_engine.copy(manifest)
