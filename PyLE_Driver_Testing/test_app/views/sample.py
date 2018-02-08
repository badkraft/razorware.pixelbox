from PyLE_Driver.framework import View


class Sample(View):
    def __init__(self, **kwargs):
        View.__init__(self, master=kwargs['master'], cnf=kwargs['cnf'])
