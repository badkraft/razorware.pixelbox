import importlib

__markup = 'markup'


def binder(target_info):
    mod_name = target_info.module.__name__
    namespace = '{mod_name}.{target}_binder'.format(mod_name=mod_name,
                                                    target=target_info.target)

    return importlib.import_module(namespace)


def load_binder(target_info):
    module = binder(target_info)

    return getattr(module, __markup)
