from tkinter import Frame


class Main(Frame):

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
