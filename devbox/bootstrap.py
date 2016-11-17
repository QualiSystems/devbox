import click
import pkg_resources
from commands.push_command import PushCommandExecutor


@click.group()
def cli():
    pass


@cli.command()
def version():
    """
    Displays the devbox version
    """
    distribution = pkg_resources.get_distribution(u'devbox')
    click.echo(u'{} {} from {}'.format(distribution.project_name, distribution.version, distribution.location))


@cli.command()
@click.option('--path', default='devbox.yaml', help='Path to manifest file')
@click.option('--deploy', default='docker', help='Deployment to use', type=click.Choice(['docker']))
@click.option('--provision', default='ansible', help='Provisioning to use', type=click.Choice(['ansible']))
def push(path, deploy, provision):
    """
    Deploy the app
    """
    PushCommandExecutor().push(path, deploy, provision)
