import importlib

from . import binder, \
    load_binder, \
    check_labels, \
    is_label, \
    label_ref, \
    reference
from .layout_manager import LayoutManager


def _configure_resources(res_cnf):
    resources = {}

    for k, v in res_cnf.items():
        print("\tlocate {k}".format(k=k))

        if k == 'context':
            # locate the view director and instantiate
            if ':' in v:  # check for label
                label = is_label(v)
                path = label[1].split('.')
                presenter = path[1]
                path = '{base}.{mod}'.format(base=label_ref(label[0]).__name__, mod=path[0])

                # assumption: context is working from an imported module
                module = importlib.import_module(path)
                print("\t -- in {module}".format(module=module.__name__))

                presenter = getattr(module, presenter)
                if presenter is not None:
                    print("\t -- found: {presenter}".format(presenter=presenter.__name__))
                    resources.update({'context': presenter()})

    return resources


class Controller:
    @property
    def name(self):
        return self.__name

    @property
    def base_name(self):
        return self.__base

    @property
    def has_binder(self):
        return binder(self.__view_info) is not None

    @property
    def has_master(self):
        return self.__master is not None

    @property
    def has_view(self):
        return self.__view is not None

    @property
    def view(self):
        return self.__view()

    def __init__(self, view_info):
        """
        Controller reads the markup binder to build forms and bind widgets to
        model values.

        :param view_info: module path info and target view
        :return:
        """
        self.__view_info = view_info
        self.__cnf = {}
        self.__name = ''
        self.__base = ''
        self.__pre = {}
        self.__content = None
        self.__resources = None

        self._initialize(self.__view_info)

    def _initialize(self, view_info):
        markup = load_binder(view_info)
        parts = None
        content = None
        resources = None

        for k, v in dict(markup).items():
            parts = k.split(':')
            content = v

        if parts is not None:
            self.__name = parts[0]
            self.__base = parts[1]

        if content is not None:
            self.__pre = content[0]
            index = 1
            resources = None if list(content[index].keys())[0] != 'resources' else content[index]
            if resources is not None:
                index += 1
            self.__content = content[index:]  # start with 2nd element and take all

        # 1. check for 'l:xxx' labels
        check_labels(self.__pre)

        # 2. configure resources (if applicable)
        if resources is not None:
            print("configure resources")
            self.__resources = _configure_resources(resources['resources'])

        self.__manager = None
        self.__master = reference(self.__pre['master'], self.__pre['import'])
        self.__view = reference(self.__name, [self.__pre['namespace']])

        if 'title' in self.__pre:
            self.__cnf.update({'title': self.__pre['title']})

    def __view(self):
        master = self.__master
        cnf = dict(self.__cnf)
        title = None

        if 'title' in cnf:
            title = cnf['title']
            del cnf['title']

        view = self.__view(master=master(), **cnf)
        view.set_context(self.__resources['context'])

        if title is not None:
            view.master.title(title)

        self.__manager = LayoutManager(view, self.__content, self.__pre['import'])

        return view
