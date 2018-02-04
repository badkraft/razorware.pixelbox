from PyLE_Driver.framework import Presenter


class Main(Presenter):

    @property
    def quit(self):
        return self.__quit_command

    def __init__(self):
        Presenter.__init__(self)

        pass

    def __quit_command(self, view_master):
        view_master.quit()
