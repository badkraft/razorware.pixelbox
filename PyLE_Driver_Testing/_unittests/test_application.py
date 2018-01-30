import unittest

from PyLE_Driver_Testing import load_binder
from PyLE_Driver_Testing.test_app import test_app_module

from PyLE_Driver import TargetInfo
from PyLE_Driver.framework import Application


class TestApplicationMethods(unittest.TestCase):

    def test_binder(self):
        app_info = TargetInfo(test_app_module, 'test_app')

        markup = load_binder(app_info)

        self.assertTrue('application' in markup)
        self.assertEqual('App', markup['application'])
        self.assertTrue('imports' in markup)
        self.assertEqual([], markup['imports'])
        self.assertTrue('startup' in markup)
        self.assertEqual('test_app.views.main', markup['startup'])

    def test_initialization(self):
        app_info = TargetInfo(test_app_module, 'test_app')
        exp_name = "App"
        application = Application(app_info)

        self.assertTrue(application is not None)
        self.assertEqual(exp_name, application.name)
        self.assertEqual([], application.imports)
        self.assertTrue(application.has_binder)

if __name__ == '__main__':
    unittest.main()
