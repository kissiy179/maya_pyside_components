# -*- coding: utf-8 -*-
import os
import re
from functools import partial
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
from mayaqt import maya_win, maya_base_mixin, QtCore, QtWidgets, QtGui
import qtawesome as qta

NODE_TYPE_PATTERN = re.compile('^(?P<node_type>\w+)(?P<exact>\+?)$')
MAYA_ICONS = cmds.resourceManager(nameFilter='*.png')
ICON_TABLE = {
    re.compile(r'^\w*[lL]ight$'): 'out_ambientLight.png',
    re.compile(r'^\w*[sS]hape$'): 'out_mesh.png',
}

class NodesByTypeMenu(QtWidgets.QMenu):
       
    def __init__(self, node_type, exact=True, parent=None):
        super(NodesByTypeMenu, self).__init__(parent)
        self.node_type = node_type
        self.exact = exact
        self.init_actions()
        
    def init_actions(self, node_type='', exact=None, set_is_in_outliner=True):
        node_type = node_type if node_type else self.node_type
        exact = exact if exact is not None else self.exact
        self.clear()
        items = pm.ls(exactType=self.node_type) if self.exact else pm.ls(type=self.node_type)
        items.sort(key=lambda item: item.nodeType())
                    
        if items:
            for item in items:
                # オブジェクトセットの場合アウトライナに表示されるもののみに絞る
                if set_is_in_outliner and item.nodeType() == 'objectSet':
                    is_in_outliner = bool(mel.eval('setFilterScript {}'.format(item.name())))

                    if not is_in_outliner:
                        continue

                name = item.name()
                # nodeName = item.nodeName()
                node_type = item.nodeType()
                pixmap = QtGui.QPixmap(':/out_{}.png'.format(node_type))
                action = self.addAction(pixmap, name, parent=self)

        else:
            action = self.addAction('--- No items ---')
            action.setEnabled(False)

class NodeNameEdit(QtWidgets.QWidget):

    textChanged = QtCore.Signal(str)
    
    def __init__(self, node_type, button_img='', parent=None):
        super(NodeNameEdit, self).__init__(parent)
        self.node_type = node_type
        self.exact = True
        
        # ノードタイプを厳格に判定するかどうかをnode_typeから決定
        # <nodeType> = 指定したノードタイプのノードのみを判定
        # <nodeType>+ = 指定したノードタイプを継承したノードを判定
        m = NODE_TYPE_PATTERN.match(self.node_type)
        
        if m and m.group('exact'):
            self.node_type = m.group('node_type')
            self.exact = False

        # ボタン画像を取得
        button_img = button_img if button_img else self.node_type
        button_img = 'out_{}.png'.format(button_img)

        if not button_img in MAYA_ICONS:
            for ptn, img in ICON_TABLE.items():
                if not ptn.match(self.node_type):
                    continue

                button_img = img

        self.button_img = ':/{}'.format(button_img)

        # UI初期化
        self.init_ui()
        
    def init_ui(self):
        hlo = QtWidgets.QHBoxLayout()
        hlo.setSpacing(0)
        hlo.setContentsMargins(0,0,0,0)
        self.setLayout(hlo)
        
        # Line edit
        self.line_edit = QtWidgets.QLineEdit()
        self.line_edit.setClearButtonEnabled(True)
        #icon = QtGui.QIcon(self.button_img)
        #self.line_edit.addAction(icon, QtWidgets.QLineEdit.LeadingPosition);
        self.line_edit.textChanged.connect(self.set_stylesheet)
        self.line_edit.textChanged.connect(self.textChanged)
        node_name = self.line_edit.text()
        hlo.addWidget(self.line_edit)
        
        # Menu button
        self.button = QtWidgets.QPushButton()
        pixmap = QtGui.QPixmap(self.button_img)
        self.button.setIcon(pixmap)
        self.button.clicked.connect(self.show_menu)
        hlo.addWidget(self.button)
        self.set_stylesheet()
        
    def text(self):
        return self.line_edit.text()

    def setText(self, text):
        self.line_edit.setText(str(text))

    def show_menu(self):
        menu = NodesByTypeMenu(self.node_type, self.exact)
        menu.triggered.connect(self.set_text)
        menu.exec_(QtGui.QCursor.pos())
        
    def set_text(self, action):
        self.setText(action.text())
        
    def set_stylesheet(self):
        items = pm.ls(exactType=self.node_type) if self.exact else pm.ls(type=self.node_type)
        node_name = self.line_edit.text()
        
        if node_name and not node_name in items:
            self.line_edit.setStyleSheet('color: indianred;')
            
        else:
            self.line_edit.setStyleSheet('')
            
        self.button.setStyleSheet('background-color: transparent; border-style: solid; border-width:0px;')

class TestWindow(maya_base_mixin, QtWidgets.QWidget):    
    
    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)
        layout = QtWidgets.QFormLayout()
        self.setLayout(layout)
        
        infos = [
            ['transform', ''],
            ['transform+', ''],
            ['joint', ''],
            ['joint+', ''],
            ['objectSet', ''],
            ['objectSet+', ''],
            ['locator', ''],
            ['camera', ''],
            ['light+', 'ambientLight'],
            ['mesh', ''],
            ['displayLayer', ''],
            ['dagNode+', ''],
        ]
        
        for node_type, button_img in infos:
            node_name_edit = NodeNameEdit(node_type, button_img)
            layout.addRow(node_type, node_name_edit)
                    
    def log(self, s):
        item = pm.PyNode(s.text())
        print(item)
        
if __name__ == '__main__':
    t = TestWindow()
    t.show()