import importlib

try:
    from PyLE_Driver import TargetInfo
except ImportError:
    import sys

    # is there a better way to do this?
    sys.path.insert(1, '/home/pi/RzWare.Pixelbox')
    from PyLE_Driver import TargetInfo

    print(sys.path)

from PyLE_Driver.bootstrap import Bootstrap


class Application(Bootstrap):
    def __init__(self, file):
        mod_info = TargetInfo(importlib.import_module('PyLE_Driver_Testing'), file)
        Bootstrap.__init__(self, mod_info)
