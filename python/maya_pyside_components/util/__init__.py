import os
import maya.cmds as cmds

def get_relatvie_path_in_maya_project(abs_path):
    pj_path = cmds.workspace(query=True, rootDirectory=True)
    pj_path = pj_path.replace(os.altsep, os.sep)
    abs_path = abs_path.replace(os.altsep, os.sep)
    path_elems = abs_path.split(os.sep)
    path_elems_len = len(path_elems)

    for i in range(path_elems_len -1):
        path_elems_ = path_elems[path_elems_len-(i+1):]
        path_elems_.insert(0, pj_path)
        rel_path = os.path.join(*path_elems_)
        
        if os.path.exists(rel_path):
            rel_path = rel_path.replace(os.sep, os.altsep)
            return rel_path

    return abs_path

def get_absolute_path_in_maya_project(rel_path):
    if os.path.isabs(rel_path):
        return rel_path

    pj_path = cmds.workspace(query=True, rootDirectory=True)
    abs_path = os.path.join(pj_path, rel_path)
    return abs_path.replace(os.sep, os.altsep)
    