import unittest
from utilities.provisioning_engine_factory import ProvisioningEngineFactory


class TestProvisioningEngineFactory(unittest.TestCase):
    def test_get_engine_names(self):
        names = ProvisioningEngineFactory().get_engine_names()

        self.assertItemsEqual(names, ['ansible'])

