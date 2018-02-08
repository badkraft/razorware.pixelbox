import importlib
import tkinter as tk
import unittest

from PyLE_Driver import TargetInfo
from PyLE_Driver.framework import get_import
from PyLE_Driver.framework.application import Application


class TestApplicationMethods(unittest.TestCase):

    def test_initialization(self):
        target_module = importlib.import_module('PyLE_Driver_Testing')
        app_cnf = TargetInfo(target_module, 'sample_1_app.json')

        exp_name = "App"
        application = Application(app_cnf)

        self.assertTrue(application is not None)
        self.assertEqual(exp_name, application.name)
        self.assertTrue(application.has_binder)

    def test_application_import(self):
        target_module = importlib.import_module('PyLE_Driver_Testing')
        app_cnf = TargetInfo(target_module, 'sample_1_app.json')

        application = Application(app_cnf)
        app_mod_name = app_cnf.module.__name__
        app_module = get_import(app_mod_name)

        self.assertEqual(app_cnf.module, app_module)

    def test_imports(self):
        target_module = importlib.import_module('PyLE_Driver_Testing')
        app_cnf = TargetInfo(target_module, 'sample_1_app.json')

        exp_key = 'tkinter'
        exp_name = exp_key
        exp_imports = {
            exp_key: importlib.import_module(exp_name)
        }

        application = Application(app_cnf)

        self.assertTrue(exp_key in application.imports)
        self.assertEqual(exp_imports[exp_key], application.imports[exp_key])

    def test_aliased_import(self):
        target_module = importlib.import_module('PyLE_Driver_Testing')
        app_cnf = TargetInfo(target_module, 'sample_1a_app.json')

        exp_key = 'tk'
        exp_name = 'tkinter'
        exp_imports = {
            exp_key: importlib.import_module(exp_name)
        }

        application = Application(app_cnf)

        self.assertTrue(exp_key in application.imports)
        self.assertEqual(exp_imports[exp_key], application.imports[exp_key])

    def test_member_root(self):
        member = 'root'
        target_module = importlib.import_module('PyLE_Driver_Testing')
        app_cnf = TargetInfo(target_module, 'sample_1_app.json')

        application = Application(app_cnf)

        members = application.extensions
        self.assertTrue(member in members)

        root = application[member]
        self.assertIsNotNone(application[member])
        self.assertTrue(isinstance(root(), tk.Tk))

    def test_member_from_aliased_root(self):
        member = 'root'
        target_module = importlib.import_module('PyLE_Driver_Testing')
        app_cnf = TargetInfo(target_module, 'sample_1a_app.json')

        application = Application(app_cnf)

        members = application.extensions
        self.assertTrue(member in members)

if __name__ == '__main__':
    unittest.main()
