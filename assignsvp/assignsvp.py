import os
import sys
from dataclasses import dataclass, field
from datetime import datetime

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
    timestamp: float
    proj: str
    x_coords: list = field(default_factory=list)
    y_coords: list = field(default_factory=list)
    posix_times: list = field(default_factory=list)
    ping_numbers: list = field(default_factory=list)
    matched_svps: list = field(default_factory=list)
    ping_list: list = field(default_factory=list)






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
    def pdscsv_to_appropriatecsv(input, i_header, output):
    
        if os.path.exists(input):
            pass
        else:
            print(RuntimeError('Either path is not correct of file does not exists'))

        with open(input, 'r') as input_f:
            file_content = input_f.read().splitlines()
            
            for num, line in enumerate(file_content):
                if line.startswith('Input file:'):
                    pdsfile_path = line[12:]
                    fname = os.path.splitext(os.path.split(pdsfile_path)[1])[0]
                    fdir = os.path.split(os.path.split(pdsfile_path)[0])[1]
                    project = os.path.split(os.path.split(os.path.split(pdsfile_path)[0])[0])[1]
                    frel_path = os.path.join(fdir, fname)

                elif line == '' or line.startswith('Time') or line.startswith('PDS2000 Export Utility'):
                    pass
                
                else:
                    line_content = line.split(',')
                    count = 0
                    try:
                        for cont in line_content:
                            float(cont)
                            count += 1
                    except:
                        print(f'error at line {num}. {header[count]}: {line_content[count]}')
                    else:
                        count = 0
                        f_tr.tr_time.append(float(line_content[0]))
                        f_tr.tr_x.append(float(line_content[1]))
                        f_tr.tr_y.append(float(line_content[2]))
                        f_tr.tr_sv.append(float(line_content[3]))
                        f_tr.tr_depth.append(float(line_content[4]))
                        f_tr.tr_heading.append(float(line_content[5]))


    def read_pdsmeta(self, path_pdsmeta):
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
        
        with open(path, 'w') as file:
            
            file.write('pds_name,svp_name\n')
            
            for idx, pds_file in enumerate(self.pds_files):
                bestmatch_svp = np.bincount(pds_file.matched_svp).argmax()
                svp_name = f'{self.svp_profiles[bestmatch_svp].sn_type}_{self.svp_profiles[bestmatch_svp].name}'
                pds_name = pds_file.name
                file.write(f'{pds_name},{svp_name}\n')
    
    @staticmethod
    def fileset_for_each_svp(dirpath, csv_filepath):
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
                
            
                    
                    
                    
            
        
        
            
            
            
    


