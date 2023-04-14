import os
import sys
from dataclasses import dataclass, field
from datetime import datetime
import re

import numpy as np


@dataclass
class SVProfileMeta:
    """A SVP metadata handling dataclass"""
    uid: int
    sn_type: str
    name: str
    timestamp: float
    station: str
    X: float
    Y: float
    proj: str
    

@dataclass
class PDSfileXY:
    
    uid: int
    name: str
    fdir: str
    ftime: datetime
    project: str
    rel_path: str
    timestamp: float = None
    proj: str
    x_coords: list = field(default_factory=list)
    y_coords: list = field(default_factory=list)
    posix_times: list = field(default_factory=list)
    ping_numbers: list = field(default_factory=list)
    matched_svps: list = field(default_factory=list)
    ping_list: list = field(default_factory=list)
    ssvs: list = field(default_factory=list)
    nadir_depths: list = field(default_factory=list)
    heading: list = field(default_factory=list)

class AssignSvp:
    """A class for assigning svp data to pds files"""
    
    def __init__(self):
        self.svp_profiles = []
        self.pds_files = []
        self.svp_array = np.empty((1, 4), dtype='float')
        self.pds_array = np.empty((1, 4), dtype='float')
        
        self.dist_delta = np.empty((1, 4), dtype='float')
        self.time_delta = np.empty((1, 4), dtype='float')
        self.val_array = np.empty((1, 4), dtype='float')
        
        
    def read_svpmeta(self, path_svpmeta):
        # SVP meta file has to be a CSV file
        # with a header:
        # UID,SN_Type,Name,Datetime,StationName,X,Y
        # where UID - ordered number, SN_Type - SVP probe serial number / name,
        # Name - SVP file name, Datetime - datetime in 'YYYY-MM-DDTHH:MM:SS' format,
        # X and Y - cartesian coordinates
        if not len(self.svp_profiles):
            self.svp_profiles = []
        
        with open(path_svpmeta, 'r') as file1:
            file_content = file1.read().splitlines()
            
            for line in file_content[1:]:
                line_content = line.split(',')
                
                svp_obj = SVProfileMeta(uid=int(line_content[0]),
                                        sn_type=line_content[1],
                                        name=line_content[2],
                                        timestamp=datetime.strptime(line_content[3],'%Y-%m-%dT%H:%M:%S').timestamp(),
                                        station=line_content[4],
                                        X=float(line_content[5]),
                                        Y=float(line_content[6]),
                                        proj='wgs84utm34n')
                self.svp_profiles.append(svp_obj)

    @classmethod
    def from_filetrack_obj():
        pass

    @staticmethod
    def read_filetrack_csv(self, input, i_headseq, projection):
        # if header is 'Time,X,Y,SSV,Nadir,Heading'
        # i_headseq should be [0,1,2,3,4,5]
        # if header if 'X,Y,Time,Nadir,SSV,Heading'
        # i_headseq should be [1,2,0,4,3,5]
        if not len(self.pds_files):
            self.pds_files = []

        with open(input, 'r') as f:
            
            file_content = f.read().splitlines()
            
            header = ['Time', 'X', 'Y', 'SSV', 'Nadir', 'Heading']
            
            for num, line in enumerate(file_content):
                
                if line.startswith('PDS2000 Export Utility'):
                    pass
                
                elif line.startswith('Input file:'):
                    file_path = line[12:]
                    fname = os.path.splitext(os.path.split(file_path)[1])[0]
                    ftime = datetime.strptime(re.search(r'\d{8}-\d{6}',fname)[0], '%Y%m%d-%H%M%S')
                    fdir = os.path.split(os.path.split(file_path)[0])[1]
                    project = os.path.split(os.path.split(os.path.split(file_path)[0])[0])[1]
                    rel_path = os.path.join(pdsfile_obj.fdir, pdsfile_obj.fname)
                    
                    pdsfile_obj = PDSfileXY(uid=int(line_content[0]),
                                            name=fname,
                                            fdir=fdir,
                                            ftime=ftime,
                                            project=project,
                                            rel_path=rel_path,
                                            proj=projection)
                    
                    self.pds_files.append(pdsfile_obj)

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
                        pdsfile_obj.posix_times.append(float(line_content[i_headseq[0]]))
                        pdsfile_obj.x_coords.append(float(line_content[i_headseq[1]]))
                        pdsfile_obj.y_coords.append(float(line_content[i_headseq[2]]))
                        pdsfile_obj.ssvs.append(float(line_content[i_headseq[3]]))
                        pdsfile_obj.nadir_depths.append(float(line_content[i_headseq[4]]))
                        pdsfile_obj.heading.append(float(line_content[i_headseq[5]]))



    def read_pdsmeta(self, path_pdsmeta):
        """ read pds filetrack csv file
        csv file has to have next header:
        fid,Fname,datetime,distance,X,Y
        datetime format: 2022-06-03T08:37:34

        Parameters
        ----------
        path_pdsmeta : _type_
            _description_
        """
        if not len(self.pds_files):
            self.pds_files = []
        
        with open(path_pdsmeta, 'r') as file2:
            file_content = file2.read().splitlines()
            
            filename = ''
            
            for line in file_content[1:]:
                line_content = line.split(',')
                try:
                    float(line_content[4])
                    float(line_content[5])
                except:
                    print(f'File {line_content[1]} has bad coordinates')
                else:
                    if filename != line_content[1]:
                        filename = line_content[1]
                        file_obj = PDSfileXY(uid=int(line_content[0]),
                                            name=line_content[1],
                                            timestamp=datetime.strptime(line_content[2],'%Y-%m-%dT%H:%M:%S').timestamp(),
                                            proj='wgs84utm34n')
                        file_obj.X.append(float(line_content[4]))
                        file_obj.Y.append(float(line_content[5]))
                        self.pds_files.append(file_obj)
                    else:
                        self.pds_files[-1].X.append(float(line_content[4]))
                        self.pds_files[-1].Y.append(float(line_content[5]))
    
    def create_arrays(self):
        
        # declare weighting matrices
        time_weight = np.array([[10*60, 20*60, 30*60, 40*60, 50*60, 60*60, 120*60, 240*60, 360*60, 480*60],[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]]).T
        # dist_weight = np.array([[1000, 1500, 2000, 3000, 4000, 5000, 10000, 15000, 20000, 40000],[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]]).T
        # v2
        dist_weight = np.array([[500, 1000, 1500, 3000, 4000, 5000, 10000, 15000, 20000, 40000],[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]]).T
        
        def apply_weights(delta_array, weight_array):
            delta_array = delta_array
            
            for idx in np.arange(len(weight_array[:,0])):
                if idx == 0:
                    mask = (weight_array[idx,0] > delta_array[:])
                    delta_array = np.where(mask, delta_array*weight_array[idx,1], delta_array)
                elif idx == len(weight_array[:,0]) - 1:
                    mask = (weight_array[idx,0] < delta_array[:])
                    delta_array = np.where(mask, delta_array*weight_array[idx,1], delta_array)
                else:
                    mask = (weight_array[idx,0] < delta_array[:]) & (weight_array[idx,0] > delta_array[:])
                    delta_array = np.where(mask, delta_array*weight_array[idx,1], delta_array)
            return delta_array
        
        self.svp_array = np.empty((len(self.svp_profiles), 3), dtype='float')
        
        for idx, svp_obj in enumerate(self.svp_profiles):
            self.svp_array[idx,0] = svp_obj.timestamp
            self.svp_array[idx,1] = svp_obj.X
            self.svp_array[idx,2] = svp_obj.Y
        
        for pds_obj in self.pds_files:
            dist_delta = np.empty((len(self.svp_profiles), len(pds_obj.X)))
            time_delta = np.empty((len(self.svp_profiles), 1))
            val_array = np.empty((len(self.svp_profiles), len(pds_obj.X)))
                                 
            time_delta = np.abs(self.svp_array[:,0] - pds_obj.timestamp)
            time_delta = apply_weights(time_delta, time_weight)
            
            for index, (x, y) in enumerate(zip(pds_obj.X, pds_obj.Y)):
                dist_delta[:,index] = np.sqrt((self.svp_array[:,1] - x)**2 + (self.svp_array[:,2] - y)**2)
                dist_delta[:,index] = apply_weights(dist_delta[:,index], dist_weight)
                val_array[:, index] = dist_delta[:,index]/np.linalg.norm(dist_delta[:,index]) + time_delta[:]/np.linalg.norm(time_delta[:])
                bestmatch_svp = np.argmin(val_array[:, index])
                pds_obj.matched_svp.append(bestmatch_svp)
                
        
    def pick_bestmatch(self, path):
        # pick bestmatch for entire file
        # path - path save to
        with open(path, 'w') as file:
            
            file.write('pds_name,svp_name\n')
            
            for idx, pds_file in enumerate(self.pds_files):
                bestmatch_svp = np.bincount(pds_file.matched_svp).argmax()
                svp_name = f'{self.svp_profiles[bestmatch_svp].sn_type}_{self.svp_profiles[bestmatch_svp].name}'
                pds_name = pds_file.name
                file.write(f'{pds_name},{svp_name}\n')
    
    @staticmethod
    def fileset_for_each_svp(dirpath, csv_filepath):
        # csv_filepath should be a file of pick_bestmatch function output
        svp_dict = {}
        
        with open(csv_filepath, 'r') as file:
            file_content = file.read().splitlines()
            for line in file_content[1:]:
                line_content = line.split(',')
                
                pds_name = line_content[1]
                svp_name = line_content[2].strip('"')
                
                if svp_name == '':
                    svp_name = 'None'
                
                if svp_name in svp_dict.keys():
                    svp_dict[svp_name].append(pds_name)
                else:
                    svp_dict[svp_name] = [pds_name]
        
        for key in svp_dict.keys():
            with open(os.path.join(dirpath, key + '.sub'), 'w') as file:
                file.write('[Files]\n')
                for num, filename in enumerate(svp_dict[key]):
                    file.write(
                        f'File({num}) = LogData\\{filename}\n'
                    )
                file.write('\n')
                
            
                    
                    
                    
            
        
        
            
            
            
    


