import paramiko


class SSHExecutionEngine(object):
    def execute(self, nodes, deployment_results):
        """
        :param nodes:
        :type nodes: Node[]
        """
        for node in nodes:
            host_address = deployment_results[node.name].ip_address
            command = node.properties['execution_command']
            if command:
                self._execute_remote(host_address, 'root', 'root', command)


    @staticmethod
    def _execute_remote(host_address, user, password, command):
        client = paramiko.client.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host_address, 22, user, password)
        client.exec_command(command)
