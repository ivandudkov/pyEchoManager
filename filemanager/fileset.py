import abc
import os
import shutil
import time
from dataclasses import dataclass


from filemanager._checks import Checks


class Fileset(metaclass=abc.ABCMeta):
    """Bla Bla Bla"""
    
    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass
    @property
    @abc.abstractmethod
    def extension(self) -> str:
        pass
    @property
    @abc.abstractmethod
    def path(self):
        pass
    
    @abc.abstractmethod
    def matchfiles(self):
        pass
    @abc.abstractmethod
    def addfiles_fromlist(self):
        pass
    @abc.abstractmethod
    def copyfiles(self):
        pass
    
    @abc.abstractmethod
    def movefiles(self):
        pass
    @abc.abstractmethod
    def readfileset(self):
        pass
    
    @abc.abstractmethod
    def savefileset(self):
        pass

    @abc.abstractmethod
    def get_size(self):
        pass

    @classmethod
    def union(cls):
        pass


@dataclass
class File:
    __slots__ = [
        'name', 'ext','rel_path', 
        'abs_path', 'matched', 'existance'
        ]
    
    name: str
    ext: str
    rel_path: str
    abs_path: str
    matched: bool

class PDSFileset(Fileset):
    """A class describes PDS2000 fileset"""

    def __init__(self):
        self._name = None
        self._path = None
        self._extention = '.pds'
        self._files = []
        self.datadir = None
        self.matched = None
    @property
    def name(self):
        return self._name
    @property
    def path(self):
        return self._path
    @property
    def extension(self) -> str:
        return self._extention
    @property
    def files(self):
        return self._files

    def setname(self, name):
        self._name = name

    def matchfiles(self, path, verbose=False):
        """path - path to file storage folder"""
        pds_files = [
            (item.name, item.path) for item in os.scandir(path) 
            if item.is_file 
            and os.path.splitext(item.name)[1] == self.extension
            ]
        matched_count = 0
        for file_obj in self.files:
            if file_obj.matched:
                matched_count += 1
                continue
            else:
                try:
                    desired_tuple = [
                    item for item in pds_files 
                    if file_obj.name == os.path.splitext(item[0])[0]][0]
                except:
                    print(f"Warning! File wasn't matched: {file_obj.name}")
                else:
                    file_obj.abs_path = desired_tuple[1]
                    file_obj.matched = True
                    matched_count += 1
        self.matched = matched_count

        if verbose:
            print(f"{matched_count} of {len(self.files)} files matched")

    def addfile(self, filename):
        pds_file = File(
                    name=filename,
                    ext=self.extension,
                    rel_path=os.path.join('LogData', filename),
                    abs_path='',
                    matched=False
                )

        self._files = [
                        item for item in self._files 
                        if item.name != filename
                        ]

        self._files.append(pds_file)

    def addfiles(self, filenames):
        for filename in filenames:
            self.addfile(filename)

    def addfiles(self, filenames):
        for filename in filenames:
            self.addfile(filename)
    def addfiles_fromlist(self, path, overwrite=True) -> None:
        """
        path: path to csv table with filenames
        """
        filenames = []

        with open(path, 'r') as file:
            content = file.readlines()

            header = content[0].splitlines()[0].split(',')
            filename_idx = 0
            for field in header:
                if field == 'Fname':
                    break
                else:
                    filename_idx += 1

            for idx, line in enumerate(content[1:]):
                line_content = line.splitlines()[0].split(',')
                filenames.append(line_content[filename_idx])


            if len(self.files) and overwrite:
                for filename in filenames:
                    self._files = [
                        item for item in self._files 
                        if item.name != filename]
                    
            elif len(self.files) and not overwrite:
                for file_obj in self.files:
                    filenames = [
                        item for item in filenames 
                        if item == file_obj.name]
                
            for filename in filenames:
                pds_file = File(
                    name=filename,
                    ext=self.extension,
                    rel_path=os.path.join('LogData', filename),
                    abs_path='',
                    matched=False
                )
                self._files.append(pds_file)

    def deletefile(self, filename):
        """Filename - str"""
        self._files = [
                item for item in self._files 
                if item.name != filename
                ]

    def deletefiles(self, filenames) -> None:
        """
        filenames - a list with filenames
        """
        
        for filename in filenames:
            self.deletefile(filename)

    def changedatadir(self, datadirname: str) -> None:
        for file_obj in self.files:
            file_obj.rel_path = os.path.join(
                datadirname, 
                os.path.basename(file_obj.rel_path)
                )

    def deleteunmached(self) -> None:
        self._files = [item for item in self._files if item.matched]
        

    def copyfiles(self, path, verbose=False) -> None:
        """
        path - a path copy to
        """
        Checks.check_path(path)
        if len(self.files) == 0:
            raise RuntimeError("Fileset object doesn't contain any files")
        if len(self.files) != sum(item.matched for item in self.files):
            raise RuntimeError("Fileset contain unmached files. Please remove unmached files")
        files_overall = len(self.files)
        files_copied = 0
        for file_obj in self.files:
            try:
                if not file_obj.matched:
                    raise RuntimeError()
                shutil.copy(file_obj.abs_path, path)
                files_copied += 1 
                if verbose:
                    print(f'Copied {files_copied} of {files_overall} files')
            except RuntimeError:
                print(f'File {file_obj.name} is not matched')
            except:
                print(f'Path is not correct or {file_obj.name} is not exists')

    def movefiles(self, path, verbose=False) -> None:
        """
        path - a path move to
        """
        Checks.check_path(path)
        if len(self.files) == 0:
            raise RuntimeError("Fileset object doesn't contain any files")
        if len(self.files) != sum(item.matched for item in self.files):
            raise RuntimeError("Fileset contain unmached files. Please remove unmached files")
        files_overall = len(self.files)
        files_copied = 0
        for file_obj in self.files:
            try:
                if not file_obj.matched:
                    raise RuntimeError()
                shutil.move(file_obj.abs_path, path)
                # file_obj.abs_path = os.path.join(path, file_obj.name + file_obj.ext)
                file_obj.matched = False
                files_copied += 1 
                if verbose:
                    print(f'Moved {files_copied} of {files_overall} files')
            except RuntimeError:
                print(f'File {file_obj.name} is not matched')
            except:
                print(f'Path is not correct or {file_obj.name} is not exists')

    def readfileset(self, path, overwrite=True) -> None:
        Checks.check_path(path)
        basename = os.path.basename(path)
        self._name = os.path.splitext(basename)[0]
        self._path = os.path.abspath(path)
        fileset_files = []

        with open(path, 'r') as file:
            content = file.readlines()
            for idx, line in enumerate(content):
                line_content = line.splitlines()[0]

                if idx == 0:
                    pass  # pass the header
                elif (line_content.rstrip('\n')).rstrip(' ') == '':
                    pass  # pass the end of file
                else:
                    splitted_line = line_content.split(sep=' = ')
                    fileset_files.append(
                        (os.path.split(splitted_line[1])[1],
                        self._extention,
                        splitted_line[1],
                        '',
                        False)
                        )

        if len(self.files) and overwrite:
            for file_tuple in fileset_files:
                self._files = [
                    item for item in self._files 
                    if item.name != file_tuple[0]]
                
        elif len(self.files) and not overwrite:
            for file_obj in self.files:
                fileset_files = [
                    item for item in fileset_files 
                    if item[0] == file_obj.name]
        
        for file_tuple in fileset_files:
            pds_file = File(
                name=file_tuple[0],
                ext=file_tuple[1],
                rel_path=file_tuple[2],
                abs_path=file_tuple[3],
                matched=file_tuple[4]
            )
            self._files.append(pds_file)


    def savefileset(self, dirpath=os.getcwd()) -> None:
        with open(os.path.join(dirpath, self.name + '.sub'), 'w') as file:
            file.write('[Files]\n')
            for num, file_obj in enumerate(self.files):
                file.write(
                    f'File({num}) = {file_obj.rel_path}\n'
                )
            file.write('\n')

    def savefileset_ascsv(self, filename, dirpath=os.getcwd()) -> None:
        with open(os.path.join(dirpath, filename), 'w') as file:
            file.write('Fname,SVP,Fileset,ProcStatus,ProcBy,dtm,bsm,datetime\n')
            for num, file_obj in enumerate(self.files):
                file.write(
                    f'{file_obj.name},,{self.name},,,,,\n'
                )

    def get_size(self):

        size = 0
        for file_obj in self.files:
            try:
                size += os.path.getsize(file_obj.abs_path)
            except:
                print('Size failed')
        return size

    def get_filenames(self):
        filenames_list = []

        for file in self._files:
            filenames_list.append(file.name)
        
        return filenames_list
        
        
    @classmethod
    def readfilesets(fs_list):
        """
        Быстрый способ инициализировать файлсеты из списка fs_list
        fs_list должен включать абсолютные пути до файлсетов .sub
        """
        fs_objs = []
        
        for fs in fs_list:
            fileset = PDSFileset()
            fileset.readfileset(fs)
            fs_objs.append(fileset)
        
        return fs_objs

    @classmethod
    def difference(fs_obj1, fs_obj2):
        """
        Если в fs_obj1 есть файлы из fs_obj2,
        то эти файлы будут убраны из fs_obj1
        
        Профильтрованный объект файлсета diff_fs_objs
        будет возвращен
        """
        diff_fs_obj = fs_obj1

        for file2 in fs_obj2.files:
            diff_fs_obj.deletefile(file2.name)

        return diff_fs_obj


    @classmethod
    def difference_list(fs_objs1, fs_objs2):
        """
        если в каком-то файлсете из fs_objs1 есть данные из какого-то
        файлсета fs_objs2, то эти файлы будут убраны из файлсета fs_objs1.

        Лист diff_fs_objs включающий в себя профильтрованные файлсееты будет возвращен
        """
        diff_fs_objs = fs_objs1

        for fs_obj2 in fs_objs2:
            for file2 in fs_objs2.files:
                for diff_fs_obj in diff_fs_objs:
                    diff_fs_obj.deletefile(file2.name)
        
        return diff_fs_objs

    @classmethod
    def match_fs(pds_files, fs_objs):
        """
        Если в листе с абсолютными путями pds_files полностью присутствуют 
        все файлы из файлсета/тов из fs_objs, то файлсет/ы
        будут возвращены в новом списке fs_objs_filt
        """
        fs_objs_filt = []

        for fs in fs_objs:
            matched_files = []
            filename_list = fs.get_filenames()

            for pds_file in pds_files:
                if pds_file in filename_list:
                    matched_files.append(pds_file)
                else:
                    pass

            if len(matched_files) == len(fs.files):
                fs_objs_filt.append(fs)

        return fs_objs_filt