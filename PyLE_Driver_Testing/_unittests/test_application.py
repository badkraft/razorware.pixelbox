import importlib
import unittest

from PyLE_Driver import TargetInfo
from PyLE_Driver.framework.application import Application


class TestApplicationMethods(unittest.TestCase):

    def test_initialization(self):
        target_module = importlib.import_module('PyLE_Driver_Testing')
        app_info = TargetInfo(target_module, 'sample_1_app.json')

        exp_name = "App"
        application = Application(app_info)

        self.assertTrue(application is not None)
        self.assertEqual(exp_name, application.name)
        self.assertEqual(['tkinter'], application.imports)
        self.assertTrue(application.has_binder)

if __name__ == '__main__':
    unittest.main()
