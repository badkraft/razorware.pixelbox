import importlib
import unittest

from PyLE_Driver import TargetInfo
from PyLE_Driver.bootstrap import Bootstrap


class TestBootstrapMethods(unittest.TestCase):

    def test_initialization(self):
        expected_dict = {
            "application": "App",
            "imports": ["tkinter"],
            "root": "Tk",
            "startup": "test_app.views.sample_1"
        }

        target_module = importlib.import_module('PyLE_Driver_Testing')
        target_info = TargetInfo(target_module, 'sample_1_app.json')

        class AppTest(Bootstrap):
            def __init__(self):
                Bootstrap.__init__(self, target_info)

        app_test = AppTest()

        self.assertEqual(expected_dict, app_test.binder)
        self.assertIsNotNone(app_test)
