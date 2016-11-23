import os

import click
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.inventory import Inventory
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager

from devbox.utilities.base_provisioning_engine import BaseProvisioningEngine


class Options(object):
    def __init__(self, verbosity=None, inventory=None, listhosts=None, subset=None, module_paths=None, extra_vars=None,
                 forks=None, ask_vault_pass=None, vault_password_files=None, new_vault_password_file=None,
                 output_file=None, tags=None, skip_tags=None, one_line=None, tree=None, ask_sudo_pass=None, ask_su_pass=None,
                 sudo=None, sudo_user=None, become=None, become_method=None, become_user=None, become_ask_pass=None,
                 ask_pass=None, private_key_file=None, remote_user=None, connection=None, timeout=None, ssh_common_args=None,
                 sftp_extra_args=None, scp_extra_args=None, ssh_extra_args=None, poll_interval=None, seconds=None, check=None,
                 syntax=None, diff=None, force_handlers=None, flush_cache=None, listtasks=None, listtags=None, module_path=None):
        self.verbosity = verbosity
        self.inventory = inventory
        self.listhosts = listhosts
        self.subset = subset
        self.module_paths = module_paths
        self.extra_vars = extra_vars
        self.forks = forks
        self.ask_vault_pass = ask_vault_pass
        self.vault_password_files = vault_password_files
        self.new_vault_password_file = new_vault_password_file
        self.output_file = output_file
        self.tags = tags
        self.skip_tags = skip_tags
        self.one_line = one_line
        self.tree = tree
        self.ask_sudo_pass = ask_sudo_pass
        self.ask_su_pass = ask_su_pass
        self.sudo = sudo
        self.sudo_user = sudo_user
        self.become = become
        self.become_method = become_method
        self.become_user = become_user
        self.become_ask_pass = become_ask_pass
        self.ask_pass = ask_pass
        self.private_key_file = private_key_file
        self.remote_user = remote_user
        self.connection = connection
        self.timeout = timeout
        self.ssh_common_args = ssh_common_args
        self.sftp_extra_args = sftp_extra_args
        self.scp_extra_args = scp_extra_args
        self.ssh_extra_args = ssh_extra_args
        self.poll_interval = poll_interval
        self.seconds = seconds
        self.check = check
        self.syntax = syntax
        self.diff = diff
        self.force_handlers = force_handlers
        self.flush_cache = flush_cache
        self.listtasks = listtasks
        self.listtags = listtags
        self.module_path = module_path


class NewAnsibleProvisioningEngine(BaseProvisioningEngine):
    def provision(self, nodes, deployment_results):
        for node in nodes:
            playbook = node.properties['provisioning_instruction']
            click.echo('Provisioning {0}'.format(node.name))
            self._provision_node(node.name, deployment_results[node.name].ip_address, playbook)

    def _provision_node(self, node_name, ip_address, playbook_name):
        # playbook_path = '/etc/ansible/install_git.yml'
        user = None
        password = None
        playbook_path = playbook_name
        host_name = ip_address

        # if not os.path.exists(playbook_path):
        #     raise Exception('The playbook does not exist')

        variable_manager = VariableManager()
        loader = DataLoader()
        inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list=[host_name])
        variable_manager.set_inventory(inventory)
        options = Options(connection='smart', become_user=user)
        passwords = {}

        host = inventory.get_host(host_name)
        variable_manager.set_host_variable(host, 'connection', 'ssh')
        variable_manager.set_host_variable(host, 'ansible_ssh_user', user)
        variable_manager.set_host_variable(host, 'ansible_ssh_pass', password)

        pbex = PlaybookExecutor(
            playbooks=[playbook_path],
            inventory=inventory,
            variable_manager=variable_manager,
            loader=loader,
            options=options,
            passwords=passwords)

        try:
            pbex.run()
        except Exception as ex:
            click.echo(ex.message)

