import importlib
import json
import os
import sys
from abc import ABC
from collections import namedtuple
from functools import reduce

dir_path = os.path.dirname(__file__)

__markup = 'markup'
__modules = {}
__imports = {}
__labels = {}

Grid = namedtuple('Grid', 'row col align row_span col_span')
ImageSource = namedtuple('ImageSource', 'path')


def binder(target_info):
    mod_name = target_info.module.__name__
    namespace = '{mod_name}.{target}'.format(mod_name=mod_name,
                                             target=target_info.target)

    return load_markup(namespace=namespace)


def load_binder(target_info):
    mod_path = os.path.dirname(target_info.module.__file__)
    binder_path = os.path.join(mod_path, target_info.target)

    return load_markup(path=binder_path)


def add_label(label):
    name, value = label

    if 'mod-' in value:
        # handle module switch
        path = value.split('-')[1]
        value = importlib.import_module(path)
    elif 'dir-' in value:  # NOTE: default behavior
        # handle directory path
        path = value.split('-')[1]
        value = path

    __labels.update({name: value})


def is_label(tag):
    label = None
    value = None

    if ':' in tag:
        parts = tag.split(':')
        label = parts[0]
        value = parts[1]

    return label, value


def label_ref(key):
    return __labels[key]


def reference(control, sources=None):
    cls = None

    if sources is None:
        sources = [i.__name__ for i in __imports.values()]

    if not isinstance(sources, list):
        sources = [sources]

    for src in sources:
        if '.' in src:
            if src not in __modules:
                __modules.update({src: importlib.import_module(src)})

            module = __modules[src]
            cls = getattr(module, control)
        else:
            if src not in __modules:
                __modules.update({src: sys.modules[src]})

            module = __modules[src]
            cls = reduce(getattr, [control], module)

        if cls is not None:
            break

    return cls


def tupleize(iterable, step):
    # len(iterable) should be evenly divisible by step
    if (len(iterable) % step) != 0:
        raise Exception('iterable length [{len}] not evenly divisible by step [{step}]'
                        .format(len=len(iterable),
                                step=step))

    x = 0
    tuples = []
    while x < len(iterable):
        y = 0
        item = ()
        while y < step:
            value = iterable[x + y]

            # ignores anything surrounded with XML comment markup: <!-- ... -->
            if y == 0 and isinstance(value, str):
                if value.startswith('<!-- ') and value.endswith(' -->'):
                    while y < step:
                        y += 1

                    continue

            item += (value, )

            y += 1

        if item != ():
            tuples.append(item)

        x += y

    return tuples


def __load_markup_from_file(path):
    markup = None

    with open(path) as j_markup:
        markup = json.load(j_markup)

    return markup


def __load_markup_from_namespace(namespace):
    parts = namespace.split('.')
    path = None

    if os.path.basename(dir_path) == parts[0]:
        # we are in the same directory (good)
        path = os.path.join(dir_path, parts[1], '{part}.designer.json'.format(part=parts[2]))
    else:
        # we need to see if we can find the path
        msg = 'directory location handler fault: {dir}[{part}]'
        print(msg.format(dir=dir_path,
                         part=parts[0]))

    if path is None:
        markup = None
    else:
        markup = __load_markup_from_file(path)

    return markup


def load_markup(**kwargs):
    if 'namespace' in kwargs:
        return __load_markup_from_namespace(kwargs['namespace'])
    elif 'path' in kwargs:
        return __load_markup_from_file(kwargs['path'])
    else:
        # arg unknown
        return None


def make_func(body_cnf):
    if '-' in body_cnf:
        typ, ref = body_cnf.split('-')

        if typ == 'cls':
            if '.' in ref:
                # lib.obj
                namespace = ref.split('.')
                mod_path, cls = ('.'.join(namespace[:-1]), namespace[-1])
                module = __imports[mod_path]
                ref = getattr(module, cls)

                return lambda: ref()


def package(top_module, namespace):
    # split on '.': namespace.split('.')
    # join excluding last element of the list: [:-1]
    parent_module = '{top}.{ns}'.format(top=top_module,
                                        ns='.'.join(namespace.split('.')[:-1]))

    return importlib.import_module(parent_module)


def add_imports(imports_cnf):
    for imp in imports_cnf:
        if '@' in imp:
            name, alias = imp.split('@')
            __imports.update({alias: importlib.import_module(name)})
        else:
            __imports.update({imp: importlib.import_module(imp)})

    return __imports


def get_import(name):
    return __imports[name]


class Presenter(ABC):
    def __init__(self):
        pass


# apparently we can make View accept a generic 'Frame' or whatever the base is
from tkinter import Frame


class View(ABC, Frame):
    @property
    def context(self):
        return self.__context

    def __init__(self, master, cnf=None):
        Frame.__init__(self, master, cnf)

        self.master = master
        self.__context = None

    def set_context(self, value):
        self.__context = value

        print("[View:{self}] set data context <Presenter:{context}>"
              .format(self=self.__class__.__name__,
                      context=value.__class__.__name__))
