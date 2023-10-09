import abc
import os
from datetime import datetime, timezone


class Filetrack(metaclass=abc.ABCMeta):
    pass
    
class PDSFileTrack(Filetrack):
    """bla bla bla"""
    
    def __init__(self):
        self.project = ''
        self.fname = ''
        self.fext = '.pds'
        self.fgpt_ext = '.gpt'
        self.fdir = ''
        self.rel_path = ''
        self.ESPG_code = None
        self.tr_time = []  # POSIX time
        self.tr_x = []  # X
        self.tr_y = []  # Y
        self.tr_ssv = []  # SoundSpeedSensor Measurements
        self.tr_depth = []  # Transducer depth (below VRF)
        self.dbt_depth = []
        self.nadir_depth = []
        self.tr_heading = []  # Heading
        self.header = {}

    @staticmethod
    def read_filetrack_csv(input, i_headseq, projection):
        # if header is 'Time,X,Y,SSV,Nadir,Heading'
        # i_headseq should be [0,1,2,3,4,5]
        # if header if 'X,Y,Time,Nadir,SSV,Heading'
        # i_headseq should be [1,2,0,4,3,5]
        
        PDS_file_tracks = []

        with open(input, 'r') as f:
            file_content = f.read().splitlines()
            header = ['Time', 'X', 'Y', 'SSV', 'Nadir', 'Heading']
            for num, line in enumerate(file_content):
                if line.startswith('PDS2000 Export Utility'):
                    f_tr = PDSFileTrack()
                    f_tr.projection = projection
                    PDS_file_tracks.append(f_tr)
                elif line.startswith('Input file:'):
                    file_path = line[12:]
                    f_tr.fname = os.path.splitext(os.path.split(file_path)[1])[0]
                    f_tr.fdir = os.path.split(os.path.split(file_path)[0])[1]
                    f_tr.project = os.path.split(os.path.split(os.path.split(file_path)[0])[0])[1]
                    f_tr.rel_path = os.path.join(f_tr.fdir, f_tr.fname)

                elif line == '' or line.startswith('Time'):
                    pass

                else:
                    line_content = line.split(',')
                    count = 0
                    try:
                        for cont in line_content:
                            float(cont)
                            count += 1
                    except:
                        print(f'error at line {num}. {header[i_headseq[count]]}: {line_content[count]}')
                    else:
                        count = 0
                        f_tr.tr_time.append(float(line_content[i_headseq[0]]))
                        f_tr.tr_x.append(float(line_content[i_headseq[1]]))
                        f_tr.tr_y.append(float(line_content[i_headseq[2]]))
                        f_tr.tr_ssv.append(float(line_content[i_headseq[3]]))
                        f_tr.tr_depth.append(float(line_content[i_headseq[4]]))
                        f_tr.tr_heading.append(float(line_content[i_headseq[5]]))
                    
            return PDS_file_tracks

    @staticmethod
    def create_fsets_path_csv(ft_obj_list, output_csv_file_path, fs_obj_list=None):
        with open(output_csv_file_path, 'w') as f:
            header = f'Project,Fname,Datetime,Proj,X,Y,SSV,NadirDepth,Heading\n'
            f.write(header)
            if fs_obj_list == None:
                for ft_obj in ft_obj_list:
                    for index, time in enumerate(ft_obj.tr_time):
                        f.write(
                            f'{ft_obj.project},'
                            f'{ft_obj.fname},'
                            f'{datetime.fromtimestamp(time, timezone.utc).isoformat()},'
                            f'{ft_obj.projection},'
                            f'{ft_obj.tr_x[index]},'
                            f'{ft_obj.tr_y[index]},'
                            f'{ft_obj.tr_ssv[index]},'
                            f'{ft_obj.tr_depth[index]},'
                            f'{ft_obj.tr_heading[index]}\n'
                        )
            else:
                for fs_obj in fs_obj_list:
                    fs_name = os.path.splitext(fs_obj.fileset_name)[0]
                    for ft_obj in ft_obj_list:
                        if ft_obj.fname + ft_obj.fext in fs_obj.linked_pds_files_names:
                            for index, time in enumerate(ft_obj.tr_time):
                                f.write(f'{ft_obj.project},{fs_name},{ft_obj.fname},{datetime.utcfromtimestamp(time).isoformat()},{ft_obj.projection},{ft_obj.tr_x[index]},{ft_obj.tr_y[index]},{ft_obj.tr_sv[index]},{ft_obj.tr_depth[index]},{ft_obj.tr_heading[index]}\n')

    @staticmethod
    def create_nadir_depth_profile(ft_obj_list, output_csv_file_path, fs_obj_list=None):
        with open(output_csv_file_path, 'w') as f:
            header = f'Datetime,X,Y,NadirDepth\n'
            f.write(header)
            if fs_obj_list == None:
                for ft_obj in ft_obj_list:
                    for index, time in enumerate(ft_obj.tr_time):
                        f.write(
                            f'{datetime.fromtimestamp(time, timezone.utc).isoformat()},'
                            f'{ft_obj.tr_x[index]},'
                            f'{ft_obj.tr_y[index]},'
                            f'{ft_obj.tr_depth[index]}\n'
                        )
            else:
                for fs_obj in fs_obj_list:
                    fs_name = os.path.splitext(fs_obj.fileset_name)[0]
                    for ft_obj in ft_obj_list:
                        if ft_obj.fname + ft_obj.fext in fs_obj.linked_pds_files_names:
                            for index, time in enumerate(ft_obj.tr_time):
                                f.write(f'{ft_obj.project},{fs_name},{ft_obj.fname},{datetime.utcfromtimestamp(time).isoformat()},{ft_obj.projection},{ft_obj.tr_x[index]},{ft_obj.tr_y[index]},{ft_obj.tr_sv[index]},{ft_obj.tr_depth[index]},{ft_obj.tr_heading[index]}\n')
