from devbox.utilities.ssh_execution_engine import SSHExecutionEngine


class ExecutionEngineFactory(object):
    def __init__(self):
        self._execution_engines = {'SSH': SSHExecutionEngine()}

    def get_execution_engine(self, execution_type):
        """
        :param execution_type:
        :return: execution engine
        :rtype BaseExecutionEngine
        """
        return self._execution_engines[execution_type]

    def get_engine_names(self):
        return self._execution_engines.keys()
