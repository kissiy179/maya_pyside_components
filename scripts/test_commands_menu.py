#encoding: utf-8

import maya.cmds as cmds

def show_message(message):
    print(message)
    cmds.inViewMessage(assistMessage=message,
                        position='midCenter',
                        fade=True,
                        # fadeStayTime=3000,
                        )

def create_menu():
    cmds.setParent('MayaWindow')
    cmds.menu(label='maya_pyside_components', tearOff=True)
    cmds.menuItem(label='Test Window', command='import maya_pyside_components.cmds as pyside_cmds; reload(pyside_cmds); pyside_cmds.show_test_window()')

