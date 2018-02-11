from PyLE_Driver.framework import Presenter
from PyLE_Driver.framework.command import Command


class Sample_2(Presenter):
    @property
    def quit(self):
        return self.__quit_command

    def __init__(self):
        Presenter.__init__(self)

        self.__quit_command = Command(lambda o: True, lambda v: v.quit())

        # def __can_quit(self, param):
        #     return True
        #
        # def __quit(self, view_master):
        #     view_master.quit()
