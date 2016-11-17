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
def push():
    """
    Deploy the app
    """
    PushCommandExecutor().push()
