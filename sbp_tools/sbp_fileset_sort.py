import os
from dataclasses import dataclass
from datetime import datetime, timezone

import numpy as np
import shutil

from filemanager import file_ext_search as fes


@dataclass
class SegyFile:
    name: str
    fileset: str
    path: str
    
    
def read_sbplog(path, fname_idx, fs_idx, sep=',', encoding='utf-8'):
    sbp_files = []
    
    with open(path, 'r', encoding=encoding) as f1:
        file_content = f1.read().splitlines()
        
        for idx, line in enumerate(file_content):
            line_content = line.split(sep)
            
            if idx == 0:
                pass
            else:
                fname = (line_content[fname_idx] + '.sgy').replace("\"", "")
                
                fileset = line_content[fs_idx]
                if fileset == '':
                    fileset = 'None'
                sbp_file = SegyFile(name=fname,fileset=fileset,path='')
                sbp_files.append(sbp_file)
                
    return sbp_files

def upd_segy_path(sgy_objs, pathlist):
    for path in pathlist:
        filename = os.path.basename(path)
        
        for sgy_obj in sgy_objs:
            if sgy_obj.name == filename:
                sgy_obj.path = path
                

def sort_files_by_fset(sgy_objs, path_sort_to):
    dirlist = [direct.path for direct in os.scandir(path_sort_to) if os.DirEntry.is_dir(direct)]
    
    for obj in sgy_objs:
        if obj.fileset == 'None':
            pass
        elif obj.fileset == '':
            pass
        elif obj.path == '':
            pass
        
        else:
            fset_dir = os.path.join(path_sort_to, obj.fileset)
            
            if fset_dir in dirlist:
                shutil.move(obj.path, fset_dir)
                obj.path = os.path.join(fset_dir, os.path.basename(obj.path))
                
            else:
                os.mkdir(fset_dir)
                dirlist.append(fset_dir)

                shutil.move(obj.path, fset_dir)
                obj.path = os.path.join(fset_dir, os.path.basename(obj.path))
                
def sort_p70_segy_by_yearday(sgy_files, path_sort_to):
    dirlist = [direct.path for direct in os.scandir(path_sort_to) if os.DirEntry.is_dir(direct)]
    sgy_dict = {}
    
    for sgy_file in sgy_files:
        name_content = os.path.basename(sgy_file).split('_')
        creation_time = None
        
        for content in name_content:
            if content.startswith('SLF'):
                creation_time = datetime.strptime(content[3:],'%y%m%d%H%M')
                yearday = datetime.strftime(creation_time,'%Y_%j')
                
                if yearday not in sgy_dict.keys():
                    sgy_dict[yearday] = [sgy_file]
                else:
                    sgy_dict[yearday].append(sgy_file)
    
    for key in sgy_dict.keys():
        key_dir = os.path.join(path_sort_to, key)
        try:
            if key_dir in dirlist:
                for sgy_file in sgy_dict[key]:
                    shutil.move(sgy_file, key_dir)
                
            else:
                os.mkdir(key_dir)
                dirlist.append(key_dir)
                
                for sgy_file in sgy_dict[key]:
                    shutil.move(sgy_file, key_dir)
        except:
            pass