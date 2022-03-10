# -*- coding: utf-8 -*-
import os
import maya.cmds as cmds

def get_relatvie_path_in_maya_project(abs_path, force=False):

    def get_resolved_path(path):
        path = path.replace(os.sep, os.altsep)
        path = '//{}'.format(path)
        return path

    # プロジェクト区切り文字(//) を含む場合はそれ以前をプロジェクトパスとして認識してそれ以降を返す
    if '//' in abs_path:
        rel_path = abs_path.split('//')[-1]
        rel_path = get_resolved_path(rel_path)
        return rel_path

    # 現在のパス情報などを取得
    pj_path = cmds.workspace(query=True, rootDirectory=True)
    pj_path = pj_path.replace(os.altsep, os.sep)
    abs_path = abs_path.replace(os.altsep, os.sep)
    abs_path = abs_path.strip(os.sep)
    path_elems = abs_path.split(os.sep)
    path_elems_len = len(path_elems)

    # プロジェクトパスから始まっていればそれ以降を返す
    abs_path_ = '{}\\'.format(abs_path)
    
    if abs_path_.startswith(pj_path):
        rel_path = abs_path[len(pj_path):]
        rel_path = get_resolved_path(rel_path)
        return rel_path

    if force:
        # 入力パスを末尾からプロジェクトパスに連結し、存在した場合それを返す
        for i in range(path_elems_len -1):
            path_elems_ = path_elems[path_elems_len-(i+1):]
            path_in_pj = os.path.join(pj_path, *path_elems_)
            
            if os.path.exists(path_in_pj):
                rel_path = os.path.join(*path_elems_)
                rel_path = get_resolved_path(rel_path)
                return rel_path

    return abs_path.replace(os.sep, os.altsep)

def get_absolute_path_in_maya_project(rel_path, include_project_sep=False):
    # プロジェクト区切り文字(//)からはじまらない場合そのまま返す
    if not rel_path.startswith('//'):
        return rel_path

    # プロジェクトパスと連結して返す
    rel_path = rel_path.strip('/')
    rel_path = get_relatvie_path_in_maya_project(rel_path)
    rel_path = rel_path.strip('/')
    pj_path = cmds.workspace(query=True, rootDirectory=True)
    abs_path = ('/' if include_project_sep else '').join([pj_path, rel_path])
    abs_path = abs_path.replace(os.sep, os.altsep)
    abs_path = abs_path.strip('/')
    return abs_path
    
