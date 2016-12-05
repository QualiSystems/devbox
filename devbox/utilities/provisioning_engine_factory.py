from devbox.utilities.ansible_provisioning_engine import AnsibleProvisioningEngine


class ProvisioningEngineFactory(object):
    def __init__(self):
        # noinspection SpellCheckingInspection
        self._provisioning_engines = {'ansible': AnsibleProvisioningEngine()}

    def get_provisioning_engine(self, provisioning_type):
        return self._provisioning_engines[provisioning_type]

    def get_engine_names(self):
        return self._provisioning_engines.keys()
