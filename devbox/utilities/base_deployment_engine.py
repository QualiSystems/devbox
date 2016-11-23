import abc


class BaseDeploymentEngine(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def deploy(self, manifest):
        raise NotImplementedError('deploy method must be implemented')

    @abc.abstractmethod
    def destroy(self, manifest):
        raise NotImplementedError('destroy method must be implemented')

    @abc.abstractmethod
    def copy(self, manifest):
        raise NotImplementedError('copy method must be implemented')

    @abc.abstractmethod
    def get_node_details(self, manifest):
        raise NotImplementedError('get_node_details method must be implemented')

