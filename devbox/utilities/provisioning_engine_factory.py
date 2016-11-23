from devbox.utilities.new_ansible_provisioning_engine import NewAnsibleProvisioningEngine


class ProvisioningEngineFactory(object):
    def __init__(self):
        # noinspection SpellCheckingInspection
        self._provisioning_engines = {'ansible': NewAnsibleProvisioningEngine()}

    def get_provisioning_engine(self, provisioning_type):
        return self._provisioning_engines[provisioning_type]

    def get_engine_names(self):
        return self._provisioning_engines.keys()
