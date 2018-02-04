from . import load_binder
from .controller import Controller
from .. import TargetInfo
from ..framework import package


class Application:
    @property
    def name(self):
        return self.__app_name

    @property
    def controller(self):
        return self.__controller

    @property
    def imports(self):
        return list(self.__imports)

    @property
    def has_binder(self):
        return load_binder(self.__app_info) is not None

    def __init__(self, app_info):
        """
        Application reads the json 'markup' to bootstrap the application
        framework.

        :param app_info:
        :return:
        """
        self.__app_info = app_info

        markup = load_binder(self.__app_info)
        self.__app_name = markup['application']
        self.__imports = markup['imports']
        self.__module = package(self.__app_info.module.__name__, markup['startup'])
        self.__startup_info = TargetInfo(self.__module, '{file}.json'.format(file=markup['startup'].split('.')[-1]))
        self.__controller = None

        self.mainloop = self.__run

    def __run(self):
        self.__initialize()
        self.__controller.view.mainloop()

    def __initialize(self):
        # TODO: try-catch
        self.__controller = Controller(self.__startup_info)

        if self.__controller is None:
            raise Exception('unknown error parsing config; controller could not be instantiated')
