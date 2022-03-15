# encoding: UTF-8
from mayaqt import QtWidgets, QtGui, QtCore, maya_base_mixin
from ..widgets import path_in_project_edit

class TestWindow(maya_base_mixin, QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)
        self.resize(1000, 200)
        main_lo = QtWidgets.QFormLayout()
        self.setLayout(main_lo)

        file_edit = path_in_project_edit.FilePathInProjectEdit()
        main_lo.addRow(file_edit.__class__.__name__, file_edit)


def show_test_window():
    win = TestWindow()
    win.show()