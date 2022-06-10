# -*- coding: utf-8 -*-
import os
import maya.cmds as cmds


def get_relatvie_path_in_maya_project(abs_path, force=False, pj_path=''):

    def format_to_relative_path(path):
        path = path.replace(os.sep, os.altsep)
        path = path.strip('/')
        path = '//{}'.format(path)
        return path

    # プロジェクト区切り文字(//) を含む場合はそれ以前をプロジェクトパスとして認識してそれ以降を返す
    # parent_dir//child_dir -> //child_dir
    if '//' in abs_path:
        rel_path = abs_path.split('//')[-1]
        rel_path = format_to_relative_path(rel_path)
        return rel_path

    # 現在のパス情報などを取得
    pj_path = pj_path if pj_path else cmds.workspace(query=True, rootDirectory=True)
    abs_path = abs_path.replace(os.sep, os.altsep)
    abs_path = abs_path.strip(os.altsep)

    # プロジェクトパスから始まっていればそれ以降を返す
    # (プロジェクトパスは末尾にパス区切り文字を含むのでそれに合わせる)
    # {プロジェクトパス}/child_dir -> //child_dir
    abs_path_ = '{}/'.format(abs_path)
    
    if abs_path.startswith(pj_path):
        rel_path = abs_path[len(pj_path):]
        rel_path = format_to_relative_path(rel_path)
        return rel_path

    ## force=Trueでがんばって相対パスに仕様とする
    # 入力パスを末尾からプロジェクトパスに連結し、存在した場合それを返す
    # parent_dir/Animations/Characters
    # を入力した場合に、
    # {プロジェクトパス}/Characters
    # が存在した場合にそれが帰ってしまうので注意
    # 本来{プロジェクトパス}/Animations/Charactersが正しい
    if force:
        path_elems = abs_path.split(os.altsep)
        path_elems_len = len(path_elems)

        for i in range(path_elems_len -1):
            path_elems_ = path_elems[path_elems_len-(i+1):]
            path_in_pj = os.path.join(pj_path, *path_elems_)
            
            if os.path.exists(path_in_pj):
                rel_path = os.path.join(*path_elems_)
                rel_path = format_to_relative_path(rel_path)
                return rel_path

    return abs_path#.replace(os.sep, os.altsep)

def get_absolute_path_in_maya_project(rel_path, force=False, include_project_sep=True, pj_path=''):
    # プロジェクト区切り文字(//)を含まない場合そのまま返す
    if not force and not '//' in rel_path:
        return rel_path

    # プロジェクトパスと連結して返す
    rel_path = get_relatvie_path_in_maya_project(rel_path, force)
    pj_path = pj_path if pj_path else cmds.workspace(query=True, rootDirectory=True)
    abs_path = ('/' if include_project_sep else '').join([pj_path, rel_path])
    abs_path = abs_path.replace(os.sep, os.altsep)
    abs_path = abs_path.strip('/')
    return abs_path
    
