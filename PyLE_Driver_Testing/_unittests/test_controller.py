import importlib
import unittest

from PyLE_Driver import TargetInfo
from PyLE_Driver.framework import add_imports
from PyLE_Driver.framework.controller import Controller


class TestControllerMethods(unittest.TestCase):

    def test_initialization(self):
        target_module = importlib.import_module('PyLE_Driver_Testing.test_app.views')
        add_imports([target_module.__name__, 'tkinter@tk'])

        view_cnf = TargetInfo(target_module, 'sample_1.json')

        exp_class = "Main"
        exp_base = "Frame"

        controller = Controller(view_cnf)

        self.assertTrue(controller is not None)
        self.assertTrue(controller.has_binder)
        self.assertEqual(exp_class, controller.name)
        self.assertEqual(exp_base, controller.base_name)

if __name__ == '__main__':
    unittest.main()
