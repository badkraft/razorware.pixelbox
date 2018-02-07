from . import load_binder
from .controller import Controller
from .. import TargetInfo
from ..framework import package, \
    make_func, \
    add_imports


class Application:
    @property
    def name(self):
        return self.__app_name

    @property
    def controller(self):
        return self.__controller

    @property
    def imports(self):
        return dict(self.__imports)

    @property
    def has_binder(self):
        return load_binder(self.__app_cnf) is not None

    def __init__(self, app_cnf):
        """
        Application reads the json 'markup' to bootstrap the application
        framework.

        :param app_cnf:
        :return:
        """
        self.__app_cnf = app_cnf

        markup = load_binder(self.__app_cnf)

        for k, v in markup.items():
            if k == 'application':
                self.__app_name = v

            elif k == 'imports':
                # {'tkinter': <module>}
                v.append(self.__app_cnf.module.__name__)
                self.__imports = add_imports(v)

            elif k == 'startup':
                self.__module = package(self.__app_cnf.module.__name__, v)
                self.__startup_info = TargetInfo(self.__module, '{file}.json'.format(file=v.split('.')[-1]))
            else:
                if ':' in k:
                    t, n = k.split(':')
                    if t in ['f']:  # function
                        self.__add_member(t, n, v)

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

    def __add_member(self, m_type, m_name, body):
        if m_type == 'f':
            # body is a return
            func = make_func(body)
            self.__dict__.update({m_name: func})

    def __getitem__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
