import os
import sys
import json
import importlib

from abc import ABC

from .framework import Application
from .framework import load_binder


def _load_root_markup(info):
    module = importlib.import_module('test_app.models')
    model = getattr(module, str)

    app_file = os.path.join(info.path, '{test_app}.json'.format(app=info.app))
    markup = {}

    if os.path.exists(app_file):
        with open(app_file) as jconfig:
            markup = json.load(jconfig)

    return markup


# bootstrapper
class Bootstrap(ABC):

    @property
    def mainloop(self):
        return self.__run_application

    @property
    def module(self):
        return self.__target_info.module

    @property
    def application(self):
        return self.__app_binder

    def __init__(self, module_info):
        """
        :rtype: Bootstrap
        """
        print('Python    : {ver}'.format(ver=sys.hexversion))
        print('PyLEDriver: 0.02.0000')
        #print('Tk ver: {ver}'.format(ver=tk.TkVersion))

        self.__target_info = module_info
        self.__app_binder = load_binder(self.__target_info)
        self.__app = Application(self.__target_info)

    def __run_application(self):

        if self.__app is not None:
            self.__app.mainloop()
        else:
            print("exiting PyLE Driver bootstrap")
