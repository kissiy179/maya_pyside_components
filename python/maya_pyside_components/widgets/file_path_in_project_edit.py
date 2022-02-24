# -*- coding: utf-8 -*-
import os
from mayaqt import QtWidgets, QtCore
import qtawesome as qta
import maya.cmds as cmds
from ... import util
from pyside_components.widgets import file_path_edit, directory_path_edit

class FilePathInMayaProjectEdit(file_path_edit.FilePathEdit):
    '''
    Mayaプロジェクト内の場合相対パスとして記憶するファイルパス用ウィジェット
    '''

    def text(self):
        text = self.line_edit.text()
        text = util.get_absolute_path_in_maya_project(text)
        return text

    def row_text(self):
        return super(FilePathInMayaProjectEdit, self).text()

    def setText(self, text):
        text = util.get_relatvie_path_in_maya_project(text)
        super(FilePathInMayaProjectEdit, self).setText(text)
