import importlib

try:
    from PyLE_Driver import TargetInfo
except:
    import sys
    # is there a better way to do this?
    sys.path.insert(1, '/home/pi/RzWare.Pixelbox')
    
    print(sys.path)

from PyLE_Driver import TargetInfo
from PyLE_Driver.bootstrap import Bootstrap


_mod_info = TargetInfo(importlib.import_module('PyDE_Pyper'),
                       'application')


class Application(Bootstrap):

    def __init__(self):
        Bootstrap.__init__(self, _mod_info)


app = Application()
app.mainloop()
