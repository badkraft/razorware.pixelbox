from PyLE_Driver.framework import View


class Main(View):
    def __init__(self, ext, cnf=None):
        View.__init__(self, master=ext['root'](), cnf=cnf)
