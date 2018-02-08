import os
# TODO: remove this reference (decouple)
import tkinter as tk

from . import reference, \
    tupleize, \
    is_label, \
    label_ref, \
    dir_path, \
    Grid, \
    ImageSource


def _build_menu(view, tk_menu, mnu_cnf, imports):
    for k, v in mnu_cnf:
        if k == '|':  # add separator
            tk_menu.add_separator()
            continue

        # k is menu button label if v is dict
        if isinstance(v, dict):
            command = _build_command(view, v)
            tk_menu.add_command(label=k, command=command)
        elif isinstance(v, list):
            menu_class = reference(tk_menu.__class__.__name__, imports)
            cascade = _build_menu(view, menu_class(master=tk_menu, tearoff=0), tupleize(v, 2), imports)

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


def _get_image_source(cnf):
    source = cnf['source']
    label, file = is_label(source)
    if label:
        source = os.path.join(label_ref(label), file)

    path = os.path.join(dir_path, source)
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
        tk_class = reference('PhotoImage', imports)
    elif img_type == 'bitmap':
        tk_class = reference('BitmapImage', imports)
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
    3. What are other viable options to decouple? Maybe a map of some sort???
    """

    def __init__(self, view, content, imports):
        self.__imports = imports
        self.__view = view
        self.__init_layout_manager(content)

    def __init_layout_manager(self, content):
        layout = {}
        children = []

        for d in content:
            if d == 'Grid':
                print("grid layout")

                layout.update({'type': d})
                layout.update({'manager': LayoutManager})
                layout.update({'content': content[d]})

            elif d == 'Menu':
                print("menu layout")

                tk_menu = reference(d, self.__imports)
                menu = _build_menu(self.__view, tk_menu(master=self.__view.master), content[d], self.__imports)
                self.__view.master.config(menu=menu)

        self.__initialize_content(layout)

    def __initialize_content(self, layout):
        self.__geometry = layout['type']
        self.__children = self.__build_controls(self.__view.master, layout['content'])

    def __build_controls(self, master, controls):
        container = []

        for cls_name, cls_cnf in controls:
            # valid comment
            if cls_name.startswith('<!--') and cls_name.endswith('-->'):
                continue
            elif (cls_name.startswith('<!--') and not cls_name.endswith('-->')) or \
                    (cls_name.endswith('-->') and not cls_name.startswith('<!--')):
                raise Exception('improper comment')

            tk_class = reference(cls_name)
            grid = None

            if 'grid' in cls_cnf:
                grid = _grid_cnf(cls_cnf['grid'])
                del cls_cnf['grid']
            if 'borderstyle' in cls_cnf:
                # RAISED='raised'
                # SUNKEN='sunken'
                # FLAT='flat'
                # RIDGE='ridge'
                # GROOVE='groove'
                # SOLID = 'solid'
                setting = cls_cnf['borderstyle']
                del cls_cnf['borderstyle']
                cls_cnf.update({'relief': setting})

            child = None

            # handle class corner cases
            if tk_class is tk.Image:
                child = _get_image_container(cls_cnf, self.__imports, master)
            if 'content' in cls_cnf:
                # recursive iteration to build child controls
                ch_cnf = cls_cnf['content']
                del cls_cnf['content']

                child = tk_class(master=master, cnf=cls_cnf)
                content = self.__build_controls(child, tupleize(ch_cnf, 2))

                if tk_class is tk.PanedWindow:
                    for c in content:
                        child.add(c)
            else:
                child = tk_class(master=master, cnf=cls_cnf)

            if self.__geometry == 'Grid' and grid is not None:
                child.grid({'row': grid.row,
                            'column': grid.col,
                            'sticky': grid.align,
                            'rowspan': grid.row_span,
                            'columnspan': grid.col_span})

            container.append(child)

        return container
