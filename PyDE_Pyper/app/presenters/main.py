from PyLE_Driver.framework import Director


class Main(Director):

    @property
    def quit(self):
        return self.__quit_command

    def __init__(self):
        Director.__init__(self)

        pass

    def __quit_command(self, view_master):
        view_master.quit()
