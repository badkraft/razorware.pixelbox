import unittest

from PyLE_Driver_Testing.test_app import test_app_module

from PyLE_Driver import TargetInfo
from PyLE_Driver.bootstrap import Bootstrap


class TestBootstrapMethods(unittest.TestCase):

    def test_initialization(self):
        target_info = TargetInfo(test_app_module, 'test_app')

        class AppTest(Bootstrap):
            def __init__(self):
                Bootstrap.__init__(self, target_info)

        app_test = AppTest()

        self.assertIsNotNone(app_test)
