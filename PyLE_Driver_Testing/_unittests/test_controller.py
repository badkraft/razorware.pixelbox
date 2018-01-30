import unittest

from PyLE_Driver_Testing import load_binder
from PyLE_Driver_Testing.test_app import test_app_module

from PyLE_Driver import TargetInfo
from PyLE_Driver.framework import Controller


class TestControllerMethods(unittest.TestCase):

    def test_binder(self):
        view_info = TargetInfo(test_app_module, 'views.main')

        markup = load_binder(view_info)

        self.assertIsNotNone(markup)

    def test_initialization(self):
        view_info = TargetInfo(test_app_module, 'views.main')
        exp_name = "Main"
        exp_base = "Frame"

        controller = Controller(view_info)

        self.assertTrue(controller is not None)
        self.assertTrue(controller.has_binder)
        self.assertEqual(exp_name, controller.name)
        self.assertEqual(exp_base, controller.base_name)

if __name__ == '__main__':
    unittest.main()
