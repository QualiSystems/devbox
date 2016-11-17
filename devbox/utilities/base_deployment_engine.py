import abc


class BaseDeploymentEngine(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def deploy(self, manifest):
        raise NotImplementedError('deploy method must be implemented')
