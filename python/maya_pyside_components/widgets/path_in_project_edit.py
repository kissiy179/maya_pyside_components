# -*- coding: utf-8 -*-
import os
from xml.etree.ElementInclude import include
from mayaqt import QtWidgets, QtCore
import qtawesome as qta
import maya.cmds as cmds
from .. import util
from pyside_components.widgets import path_edit

class FilePathInProjectEdit(path_edit.FilePathEdit):
    '''
    Mayaプロジェクト内の場合相対パスとして記憶するファイルパス用ウィジェット
    '''

    def __init__(self, *args, **kwargs):
        super(FilePathInProjectEdit, self).__init__(*args, **kwargs)
        self.__raw_mode = False
        self.editingFinished.connect(self.resolve_path)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MidButton:
            self.__raw_mode = not self.__raw_mode

        self.resolve_path()
        super(FilePathInProjectEdit, self).mouseReleaseEvent(event)

    def text(self, include_project_sep=True):
        text = self.line_edit.text()
        text = util.get_absolute_path_in_maya_project(text, include_project_sep=include_project_sep)
        return text

    def raw_text(self):
        return super(FilePathInProjectEdit, self).text()

    def resolve_path(self, text=''):
        text = text if text else self.raw_text()
        text = util.get_relatvie_path_in_maya_project(text, force=False)

        if self.__raw_mode:
            text = util.get_absolute_path_in_maya_project(text, include_project_sep=True)

        super(FilePathInProjectEdit, self).setText(text)

        # abs_path = util.get_absolute_path_in_maya_project(text)
        # if os.path.exists(abs_path):
        #     self.line_edit.setStyleSheet('color: lightgray;')

        # else:
        #     self.line_edit.setStyleSheet('color: indianred;')

    def setText(self, text):
        self.resolve_path(text)

class DirectoryPathInProjectEdit(FilePathInProjectEdit):
    '''
    Mayaプロジェクト内の場合相対パスとして記憶するファイルパス用ディレクトリパス用ウィジェット
    '''
    open_method = path_edit.getExistingDirectory

class MayaSceneEdit(FilePathInProjectEdit):
    '''
    Mayaシーンパス用ウィジェット
    .ma, .mb, .fbxが有効
    '''
    filter = 'Maya scene files (*.ma *.mb);;FBX files (*.fbx)'

