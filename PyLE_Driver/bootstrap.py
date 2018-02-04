import sys
from abc import ABC

from .framework import load_binder
from .framework.application import Application


# bootstrapper
class Bootstrap(ABC):

    @property
    def mainloop(self):
        return self.__run_application

    @property
    def module(self):
        return self.__target_info.module

    @property
    def binder(self):
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
        self.__app = None

    def __run_application(self):
        self.__app = Application(self.__target_info)

        if self.__app is not None:
            self.__app.mainloop()
        else:
            print("exiting PyLE Driver bootstrap")
