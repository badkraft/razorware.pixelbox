import os
import sys
import json
import importlib
import tkinter as tk

from abc import ABC
from collections import namedtuple
from functools import reduce,\
                      partial

from PyLE_Driver import TargetInfo

__markup = 'markup'
__modules = {}
__dir_path = os.path.dirname(__file__)
__labels = {}

Grid = namedtuple('Grid', 'row col align row_span col_span')
ImageSource = namedtuple('ImageSource', 'path')


def binder(target_info):
    mod_name = target_info.module.__name__
    namespace = '{mod_name}.{target}_binder'.format(mod_name=mod_name,
                                                    target=target_info.target)

    return importlib.import_module(namespace)


def load_binder(target_info):
    module = binder(target_info)

    return getattr(module, __markup)


def _check_labels(pre_markup):
    for k, v in pre_markup.items():
        if 'l:' in k:
            label = k.split(':')[1]
            if 'mod-' in v:
                # handle module switch
                path = v.split('-')[1]
                v = importlib.import_module(path)
            elif 'dir-' in v:       # NOTE: default behavior
                # handle directory path
                path = v.split('-')[1]
                v = path

            __labels.update({label: v})


def _is_label(tag):
    label = None
    value = None

    if ':' in tag:
        parts = tag.split(':')
        label = parts[0]
        value = parts[1]

    return label, value


def _locate(control, sources):
    cls = None

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


def _tupleize(iterable, step):
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


def _grid_cnf(cnf):
    row = cnf['row'] if 'row' in cnf else None
    col = cnf['col'] if 'col' in cnf else None
    align = None

    if 'align' in cnf:
        align = []
        for anchor in cnf['align'].split(" "):
            if anchor == 'left':
                align.append('W')
            elif anchor == 'right':
                align.append('E')
            elif anchor == 'top':
                align.append('N')
            elif anchor == 'bottom':
                align.append('S')

        align = " ".join(align)

    row_span = cnf['row-span'] if 'row-span' in cnf else None
    col_span = cnf['col-span'] if 'col-span' in cnf else None

    return Grid(row, col, align, row_span, col_span)


def _get_image_source(cnf):
    source = cnf['source']
    label, file = _is_label(source)
    if label:
        source = os.path.join(__labels[label], file)

    path = os.path.join(__dir_path, source)
    if not os.path.isfile(path):
        print('file not found: {file}'.format(file=cnf['source']))

    return ImageSource(path)


def _get_image_container(tk_cnf, imports, master):
    # default image type
    img_type = 'photo'
    if 'type' in tk_cnf:
        img_type = tk_cnf['type']
        del tk_cnf['type']

    if img_type == 'photo':
        tk_class = _locate('PhotoImage', imports)
    elif img_type == 'bitmap':
        tk_class = _locate('BitmapImage', imports)
    else:
        raise Exception('Unknown image type: {imgtype}'.format(imgtype=img_type))

    # manipulate source/file path
    source = _get_image_source(tk_cnf)
    del tk_cnf['source']
    image_cnf = {'file': source.path}
    image = tk_class(master=master, cnf=image_cnf)

    # if tk.Label then:
    tk_cnf.update({'image': image})
    # we could use our own image container (or extensible view controller)
    # here to decouple dependency on tk
    child = tk.Label(master=master, cnf=tk_cnf)
    # replicate reference to image
    child.image = image

    return child


def _build_menu(view, tk_menu, mnu_cnf, imports):
    for k, v in mnu_cnf:
        if k == '|':        # add separator
            tk_menu.add_separator()
            continue

        # k is menu button label if v is dict
        if isinstance(v, dict):
            command = _build_command(view, v)
            tk_menu.add_command(label=k, command=command)
        elif isinstance(v, list):
            menu_class = _locate(tk_menu.__class__.__name__, imports)
            cascade = _build_menu(view, menu_class(master=tk_menu, tearoff=0), _tupleize(v, 2), imports)

            tk_menu.add_cascade(label=k, menu=cascade)

    return tk_menu


def _build_command(view, cmd_cnf):
    command = None if cmd_cnf['command'] == "" else cmd_cnf['command']
    parameter = None if ('parameter' not in cmd_cnf or cmd_cnf['parameter'] == "") else cmd_cnf['parameter']

    if parameter is not None:
        if 'view' in parameter:
            parameter = view.master

    if command is not None:
        if 'binding' in command:
            command = getattr(view.context, 'quit')

    print("bind command: {command}({parameter})"
          .format(command=command,
                  parameter="" if parameter is None else parameter))

    return lambda: command(parameter)


def _configure_resources(res_cnf):
    resources = {}

    for k, v in res_cnf.items():
        print("\tlocate {k}".format(k=k))

        if k == 'context':
            # locate the view director and instantiate
            if ':' in v:        # check for label
                label = _is_label(v)
                path = label[1].split('.')
                presenter = path[1]
                path = '{base}.{mod}'.format(base=__labels[label[0]].__name__, mod=path[0])

                # assumption: context is working from an imported module
                module = importlib.import_module(path)
                print("\t -- in {module}".format(module=module.__name__))

                presenter = getattr(module, presenter)
                if presenter is not None:
                    print("\t -- found: {presenter}".format(presenter=presenter.__name__))
                    resources.update({'context': presenter()})

    return resources


def __load_markup(namespace):
    parts = namespace.split('.')
    path = None

    if os.path.basename(__dir_path) == parts[0]:
        # we are in the same directory (good)
        path = os.path.join(__dir_path, parts[1], '{part}.designer.json'.format(part=parts[2]))
    else:
        # we need to see if we can find the path
        msg = 'directory location handler fault: {dir}[{part}]'
        print(msg.format(dir=__dir_path,
                         part=parts[0]))

    if path is None:
        markup = None
    else:
        with open(path) as j_markup:
            markup = json.load(j_markup)

    return markup


class Director(ABC):

    def __init__(self):
        pass


class LayoutManager:
    """
    The layout manager is the most coupled class to the specific library in use -
    in this case, Tkinter. If there is a way to decouple, this is the first place
    to look. Initial thought and conventional practice might suggest an inheritance
    chain wherein LayoutManager becomes an abstract class. To expect developers
    to write this class might be a bit much to expect.

    That said, questions to be answered:
    1. Can we decouple at LayoutManager and write different flavors (Tkinter, QT, etc)?
    2. a) Are developers willing to roll their own LayoutManager flavor?
       b) Does this requirement negate any value added by using this library?
    3. What are other viable options to decouple?
    """

    def __init__(self, view, content, imports):
        self.__imports = imports
        self.__view = view
        self.__init_layout_manager(content)

    def __init_layout_manager(self, content):
        layout = {}
        children = []

        for d in content:
            for k, v in d.items():
                if k == 'Grid':
                    print("grid layout")

                    layout.update({'type': k})
                    layout.update({'manager': LayoutManager})
                    layout.update({'content': v})
                elif k == 'Menu':
                    print("menu layout")

                    tk_menu = _locate(k, self.__imports)
                    menu = _build_menu(self.__view, tk_menu(master=self.__view.master), _tupleize(v, 2), self.__imports)
                    self.__view.master.config(menu=menu)
                else:
                    break

        if layout.keys():
            self.__layout_type = layout['type']
        if 'content' in layout:
            children = _tupleize(layout['content'], 2)

        self.__initialize_content(children)

    def __initialize_content(self, children):
        self.__children = self.__build_controls(self.__view.master, children)

    def __build_controls(self, master, controls):
        container = []

        for ch in controls:
            tk_class = _locate(ch[0], self.__imports)
            tk_cnf = ch[1]
            grid = None

            if 'grid' in tk_cnf:
                grid = _grid_cnf(tk_cnf['grid'])
                del tk_cnf['grid']
            if 'borderstyle' in tk_cnf:
                # RAISED='raised'
                # SUNKEN='sunken'
                # FLAT='flat'
                # RIDGE='ridge'
                # GROOVE='groove'
                # SOLID = 'solid'
                setting = tk_cnf['borderstyle']
                del tk_cnf['borderstyle']
                tk_cnf.update({'relief': setting})

            child = None

            # handle class corner cases
            if tk_class is tk.Image:
                child = _get_image_container(tk_cnf, self.__imports, master)
            if 'content' in tk_cnf:
                # recursive iteration to build child controls
                ch_cnf = tk_cnf['content']
                del tk_cnf['content']

                child = tk_class(master=master, cnf=tk_cnf)
                content = self.__build_controls(child, _tupleize(ch_cnf, 2))

                if tk_class is tk.PanedWindow:
                    for c in content:
                        child.add(c)
            else:
                child = tk_class(master=master, cnf=tk_cnf)

            if self.__layout_type == 'Grid' and grid is not None:
                child.grid({'row': grid.row,
                            'column': grid.col,
                            'sticky': grid.align,
                            'rowspan': grid.row_span,
                            'columnspan': grid.col_span})

            container.append(child)

        return container


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
        return self.__init_view()

    def __init__(self, view_info):
        """
        Controller reads the markup binder to build forms and bind widgets to
        model values.

        :param markup: JSON string containing configuration, modelling and binding parameters.
        :return:
        """
        self.__view_info = view_info
        self.__cnf = {}

        self._initialize()

    def _initialize(self):
        markup = load_binder(self.__view_info)
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
            # TODO: decouple from sample 'main_binder.py', need to make checks
            index = 1
            resources = None if list(content[index].keys())[0] != 'resources' else content[index]
            if resources is not None:
                index += 1
            self.__content = content[index:]    # start with 2nd element and take all

        # 1. check for 'l:xxx' labels
        _check_labels(self.__pre)

        # 2. configure resources (if applicable)
        if resources is not None:
            print("configure resources")
            self.__resources = _configure_resources(resources['resources'])

        self.__manager = None
        self.__master = _locate(self.__pre['master'], self.__pre['import'])
        self.__view = _locate(self.__name, [self.__pre['namespace']])

        if 'title' in self.__pre:
            self.__cnf.update({'title': self.__pre['title']})

    def __init_view(self):
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
        return binder(self.__app_info) is not None

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
        self.__startup_info = TargetInfo(self.__app_info.module, markup['startup'])

        # TODO: Controller should __init__ with path to _binder (namespace) --
        #       i.e., _load_markup(...) from Controller initializer
        #
        # self.__markup = load_binder(self.__startup)

        self.__controller = None

        self.mainloop = self.__run
        self.__app = None
        self.__initialize()

    def __run(self):
        self.__app = self.__controller.view
        self.__app.mainloop()

    def __initialize(self):
        # TODO: try-catch
        self.__controller = Controller(self.__startup_info)

        if self.__controller is None:
            raise Exception('unknown error parsing config; controller could not be instantiated')
