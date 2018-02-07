import importlib
from collections import namedtuple

from . import binder, \
    load_binder, \
    add_label, \
    is_label, \
    label_ref, \
    reference
from .layout_manager import LayoutManager

ViewInfo = namedtuple('ViewInfo', 'reference class_name')


def _configure_header(view_cnf, hdr_cnf):
    """
    Builds a more useful header for internal use

    :param hdr_cnf: Example json:
        "header": {
            "class": "Main:Frame",
            "namespace": "test_app.views.main",
            "import": [...],
            "title": "Sample 1",
            ...
        }

    :return:
        "header": {
            "class": ClassInfo
            "namespace": "test_app.views.main",
            "import": [...],
            "title": "Sample 1",
            ...
        }
    """
    hdr = {}

    for k, v in dict(hdr_cnf).items():
        if k == 'class':
            mod, cls = v.split('.')
            module = importlib.import_module('{root}.{module}'
                                             .format(root=view_cnf.module.__name__,
                                                     module=mod))
            ref = getattr(module, cls)
            info = ViewInfo(ref, cls)

            hdr.update({'class': info})

        else:
            if 'l:' in k:
                add_label(k.split(':')[1])

            hdr.update({k: v})

    return hdr


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
        return binder(self.__view_cnf) is not None

    @property
    def has_master(self):
        return self.__master is not None

    @property
    def has_view(self):
        return self.__view is not None

    @property
    def view(self):
        return self.__view()

    def __init__(self, view_cnf):
        """
        Controller reads the markup binder to build forms and bind widgets to
        model values.

        :param view_cnf: module path info and target view
        :return:
        """
        self.__view_cnf = view_cnf
        self.__cnf = {}
        self.__name = ''
        self.__base = ''
        self.__header = {}
        self.__content = None
        self.__resources = None

        self._initialize(self.__view_cnf)

    def _initialize(self, view_cnf):
        markup = load_binder(view_cnf)
        header = {}
        resources = {}
        content = None

        for k, v in dict(markup).items():
            if k == 'header':
                header = v

            elif k == 'resources':
                resources = v

            elif k == 'content':
                content = v

        # 1. configure header (also checks for labels)
        print("configure header")
        self.__header = _configure_header(self.__view_cnf, header)

        # 2. configure resources (if applicable)
        print("configure resources")
        self.__resources = _configure_resources(resources)

        if content is None:
            # what if it is empty...
            pass

        else:
            self.__content = content

        self.__manager = None
        # self.__master = reference(self.__header['master'], self.__header['import'])
        self.__view = reference(self.__name)

        if 'title' in self.__header:
            self.__cnf.update({'title': self.__header['title']})

    def __view(self):
        master = lambda: ""  # self.__master
        cnf = dict(self.__cnf)
        title = None

        if 'title' in cnf:
            title = cnf['title']
            del cnf['title']

        view = self.__view(master=master(), **cnf)
        view.set_context(self.__resources['context'])

        if title is not None:
            view.master.title(title)

        self.__manager = LayoutManager(view, self.__content, self.__header['import'])

        return view
