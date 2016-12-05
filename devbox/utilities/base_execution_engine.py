import abc

class BaseExecutionEngine(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def execute(self, manifest, deployment_results):
        raise NotImplementedError('execute method must be implemented')
