import abc


class BaseProvisioningEngine(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def provision(self, manifest, deployment_results):
        raise NotImplementedError('provision method must be implemented')
