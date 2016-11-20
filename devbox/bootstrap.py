import click
import pkg_resources

from devbox.commands.destroy_command import DestroyCommandExecutor
from devbox.commands.push_command import PushCommandExecutor
from utilities.deployment_engine_factory import DeploymentEngineFactory
from utilities.provisioning_engine_factory import ProvisioningEngineFactory


@click.group()
def cli():
    """
    Run 'devbox COMMAND --help' for more information on a command.
    """
    pass


def get_deployment_engine_names():
    return DeploymentEngineFactory().get_engine_names()


def get_provisioning_engine_names():
    return ProvisioningEngineFactory().get_engine_names()


@cli.command()
def templates():
    """
    Display available templates
    """
    click.echo('This should retrieve templates from github.com/QualiSystems/devbox-templates')


@cli.command()
@click.argument('name')
@click.argument('template')
def init():
    """
    Initialize an app based on a template
    :return:
    """
    click.echo('This should clone a template from github.com/QualiSystems/devbox-templates to local directory')


@cli.command()
def version():
    """
    Display the current version
    """
    distribution = pkg_resources.get_distribution(u'devbox')
    click.echo(u'{} {} from {}'.format(distribution.project_name, distribution.version, distribution.location))


@cli.command()
@click.option('--path', default='devbox.yaml', help='Path to manifest file')
@click.option('--deploy', default='docker', help='Deployment to use',
              type=click.Choice(get_deployment_engine_names()))
@click.option('--provision', default='ansible', help='Provisioning to use',
              type=click.Choice(get_provisioning_engine_names()))
def push(path, deploy, provision):
    """
    Deploy the app
    """
    PushCommandExecutor().push(path, deploy, provision)


@cli.command()
@click.option('--path', default='devbox.yaml', help='Path to manifest file')
@click.option('--deploy', default='docker', help='Deployment to use', type=click.Choice(get_deployment_engine_names()))
def destroy(path, deploy):
    """
    Destroy the app
    """
    DestroyCommandExecutor().destroy(path, deploy)
