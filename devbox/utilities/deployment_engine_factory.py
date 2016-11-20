from devbox.utilities.docker_deployment_engine import DockerDeploymentEngine


class DeploymentEngineFactory(object):
    def __init__(self):
        self._deployment_engines = {'docker': DockerDeploymentEngine()}

    def get_deployment_engine(self, deployment_type):
        """

        :param deployment_type:
        :return: Deployment engine
        :rtype BaseDeploymentEngine
        """
        return self._deployment_engines[deployment_type]

    def get_engine_names(self):
        return self._deployment_engines.keys()
