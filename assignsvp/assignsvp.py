import os
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
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
    proj: str
    timestamp: float = None
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
        # UID,SN_Type,Name,Datetime,StationName,X,Y,lat,lon
        # where UID - ordered number, SN_Type - SVP probe serial number / name,
        # Name - SVP file name, Datetime - datetime in 'YYYY-MM-DDTHH:MM:SS' format,
        # X and Y - cartesian coordinates
        if not len(self.svp_profiles):
            self.svp_profiles = []
        
        with open(path_svpmeta, 'r') as file1:
            file_content = file1.read().splitlines()
            
            for line in file_content[1:]:
                line_content = line.split(',')
                datetime_svp = datetime.strptime(line_content[3],'%Y-%m-%dT%H:%M:%S')
                ts = datetime_svp.replace(tzinfo=timezone.utc).timestamp()
                
                svp_obj = SVProfileMeta(uid=int(line_content[0]),
                                        sn_type=line_content[1],
                                        name=line_content[2],
                                        timestamp=ts,
                                        station=line_content[4],
                                        X=float(line_content[5]),
                                        Y=float(line_content[6]),
                                        proj='wgs84utm34n')
                self.svp_profiles.append(svp_obj)

    @classmethod
    def from_filetrack_obj():
        pass

    def read_filetrack_csv(self, input, i_headseq, projection):
        # if header is 'Time,X,Y,SSV,Nadir,Heading'
        # i_headseq should be [0,1,2,3,4,5]
        # if header if 'X,Y,Time,Nadir,SSV,Heading'
        # i_headseq should be [1,2,0,4,3,5]
        # if you don't have any of 'X,Y,Time,Nadir,SSV,Heading' data
        # put there -999 index, like if you don't have Heading
        # i-headseq will be: [1,2,0,4,3,-999]
        
        if not len(self.pds_files):
            self.pds_files = []
        
        header = ['Time', 'X', 'Y', 'SSV', 'Nadir', 'Heading']
        
        for idx, h in enumerate(i_headseq):
            if h == -999:
                print(f'Warning, there is no {header[idx]} data!')

        with open(input, 'r') as f:
            
            file_content = f.read().splitlines()
            
            for num, line in enumerate(file_content):
                
                if line.startswith('PDS2000 Export Utility'):
                    pass
                
                elif line.startswith('Input file:'):
                    file_path = line[12:]
                    fname = os.path.splitext(os.path.split(file_path)[1])[0]
                    ftime = datetime.strptime(re.search(r'\d{8}-\d{6}',fname)[0], '%Y%m%d-%H%M%S')
                    fdir = os.path.split(os.path.split(file_path)[0])[1]
                    project = os.path.split(os.path.split(os.path.split(file_path)[0])[0])[1]
                    rel_path = os.path.join(fdir, fname)
                    
                    pdsfile_obj = PDSfileXY(uid=int(num),
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
                        
                        if i_headseq[0] != -999:
                            pdsfile_obj.posix_times.append(float(line_content[i_headseq[0]]))
                        if i_headseq[1] != -999:
                            pdsfile_obj.x_coords.append(float(line_content[i_headseq[1]]))
                        if i_headseq[2] != -999:
                            pdsfile_obj.y_coords.append(float(line_content[i_headseq[2]]))
                        if i_headseq[3] != -999:
                            pdsfile_obj.ssvs.append(float(line_content[i_headseq[3]]))
                        if i_headseq[4] != -999:
                            pdsfile_obj.nadir_depths.append(float(line_content[i_headseq[4]]))
                        if i_headseq[5] != -999:
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
        # time_weight = np.array([[10*60, 20*60, 30*60, 40*60, 50*60, 60*60, 120*60, 240*60, 360*60, 480*60],[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]]).T
        # dist_weight = np.array([[1500, 2000, 3000, 4000, 5000, 6000, 10000, 15000, 20000, 40000],[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]]).T

        # Good_v1
        dist_weight = np.array([[5000, 6000, 7000, 8000, 9000, 9500, 10000, 15000, 20000, 40000],[0.7, 0.6, 0.5, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]]).T
        time_weight = np.array([[60*60, 120*60, 180*60, 240*60, 300*60, 360*60, 480*60, 600*60, 800*60, 1200*60],[0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9, 0.95, 1]]).T
        # Better than good v2
        # dist_weight = np.array([[5000, 6000, 7000, 8000, 9000, 9500, 10000, 15000, 20000, 40000],[0.7, 0.6, 0.55, 0.6, 0.65, 0.68, 0.7, 0.8, 0.9, 1]]).T
        # time_weight = np.array([[60*60, 120*60, 180*60, 240*60, 300*60, 360*60, 480*60, 600*60, 800*60, 1200*60],[0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9, 0.95, 1]]).T
        
        # V3
        # dist_weight = np.array([[5000, 6000, 7000, 8000, 9000, 9500, 10000, 11000, 12000, 14000],[0.7, 0.6, 0.5, 0.5, 0.5, 0.6, 0.7, 0.8, 0.9, 1]]).T
        # time_weight = np.array([[60*60, 120*60, 180*60, 240*60, 300*60, 360*60, 480*60, 600*60, 800*60, 1200*60],[0.1, 0.2, 0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.5, 0.3]]).T


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
                    mask = (weight_array[idx-1,0] < delta_array[:]) & (weight_array[idx,0] > delta_array[:])
                    delta_array = np.where(mask, delta_array*weight_array[idx,1], delta_array)
            return delta_array
        
        self.svp_array = np.empty((len(self.svp_profiles), 3), dtype='float')
        
        for idx, svp_obj in enumerate(self.svp_profiles):
            self.svp_array[idx,0] = svp_obj.timestamp
            self.svp_array[idx,1] = svp_obj.X
            self.svp_array[idx,2] = svp_obj.Y
        
        for pds_obj in self.pds_files:
            dist_delta = np.empty((len(self.svp_profiles), len(pds_obj.x_coords)))
            time_delta = np.empty((len(self.svp_profiles), 1))
            val_array = np.empty((len(self.svp_profiles), len(pds_obj.y_coords)))
            
            for index, (timestamp, x, y) in enumerate(zip(pds_obj.posix_times,pds_obj.x_coords, pds_obj.y_coords)):
                time_delta = np.abs(self.svp_array[:,0] - timestamp)
                time_delta = apply_weights(time_delta, time_weight)
                dist_delta[:,index] = np.sqrt((self.svp_array[:,1] - x)**2 + (self.svp_array[:,2] - y)**2)
                dist_delta[:,index] = apply_weights(dist_delta[:,index], dist_weight)
                val_array[:, index] = dist_delta[:,index]/np.linalg.norm(dist_delta[:,index]) + time_delta[:]/np.linalg.norm(time_delta[:])
                # val_array[:, index] = dist_delta[:,index] + time_delta[:]
                bestmatch_svp = np.argmin(val_array[:, index])
                pds_obj.matched_svps.append((timestamp, bestmatch_svp))
                
        
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
    
    @staticmethod
    def save_matched_track(pds_files, svp_files, path, stnd_only = False):
        
        with open(path, 'w') as f:
            
            f.write('uid,fname,tsmp,datetime,x,y,svp_station,fname_svpstation\n')
            
            for pds_file in pds_files:
                for idx, timestamp in enumerate(pds_file.posix_times):
                    if stnd_only and idx >= 1 and pds_file.matched_svps[idx-1][1] == pds_file.matched_svps[idx][1]:
                        pass
                    else:
                        pds_isodatetime = datetime.fromtimestamp(timestamp, timezone.utc).isoformat()
                        svp_isodatetime = datetime.fromtimestamp(
                            svp_files[pds_file.matched_svps[idx][1]].timestamp, timezone.utc
                            ).isoformat()
                        
                        f.write(f'{pds_file.uid},')
                        f.write(f'{pds_file.name},')
                        f.write(f'{timestamp},')
                        f.write(f'{pds_isodatetime},')
                        f.write(f'{pds_file.x_coords[idx]},')
                        f.write(f'{pds_file.y_coords[idx]},')
                        f.write(f'{svp_files[pds_file.matched_svps[idx][1]].station},')
                        f.write(f'{pds_file.name}_{svp_files[pds_file.matched_svps[idx][1]].station}\n')
                        
    @staticmethod
    def assign_svp_filesets(spreadsheet, output, header_seq, prefix):
        # spreadsheet is a csv table
        # header_seq: time,fname,svp_station
        # if header is: uid,fname,datetime,svp_name,svp_station,StatusMBES
        # the sequence should be: [2,1,3]
        
        svp_filesets = {}
        pds_dict = {}
        
        lines = []
        
        with open(spreadsheet, 'r') as file:
            file_content = file.read().splitlines()
            
            for line in file_content[1:]:
                line_content = line.split(',')
                
                print(line_content[header_seq[0]])
                
                datetime_pds = datetime.fromisoformat(line_content[header_seq[0]]).strftime("%H%M%S")
                pds_name = line_content[header_seq[1]]
                svp_name = line_content[header_seq[2]]
                
                lines.append([datetime_pds,pds_name,svp_name])
                
                if pds_name in pds_dict.keys():
                    pds_dict[pds_name][0].append(datetime_pds)
                    pds_dict[pds_name][1].append(svp_name)
                else:
                    pds_dict[pds_name] = [[datetime_pds], [svp_name]]

        for pds_file in pds_dict.keys():
            unique_svp, indices = np.unique(pds_dict[pds_file][1], return_index=True)
            
            if len(unique_svp) > 1:
                fileset_name = f'{prefix}'
                
                for idx, uni_svp in zip(indices, unique_svp):
                    fileset_name += f'_{pds_dict[pds_file][0][idx]}_{uni_svp}'
                
                svp_filesets[fileset_name] = [pds_file]
            else:
                fileset_name = f'{prefix}_{unique_svp[0]}'
                
                if fileset_name in svp_filesets.keys():
                    svp_filesets[fileset_name].append(pds_file)
                else:
                    svp_filesets[fileset_name] = [pds_file]
        
        with open(output, 'w') as file:
            file.write('datetime,fname,svp_station,svp_fileset\n')
            
            for line_content in lines:
                datetime_pds = line_content[0]
                fname = line_content[1]
                svp_name = line_content[2]
                fs_name = ''
                
                for fileset_name in svp_filesets.keys():
                    if fname in svp_filesets[fileset_name]:
                        fs_name = fileset_name
            
                file.write(f'{datetime_pds},{fname},{svp_name},{fs_name}\n')
    
                    
            
        
        
            
            
            
    


