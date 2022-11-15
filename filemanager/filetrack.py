import os
import abc

def read_filetrack_csv(track_path, projection):
    PDS_file_tracks = []

    with open(track_path, 'r') as f:
        file_content = f.read().splitlines()
        header = ['time', 'x', 'y', 'sv', 'depth', 'heading']
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
                try:
                    count = 0
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
                
        return PDS_file_tracks

class Filetrack(metaclass=abc.ABCMeta):
    pass
    
class PDSFileTrack(Filetrack):
    """bla bla bla"""
    
    def __init__(self):
        self.project = None
        self.fname = None
        self.fext = '.pds'
        self.fgpt_ext = '.gpt'
        self.fdir = None
        self.rel_path = None
        self.projection = None
        self.tr_time = []  # Excel time (days since January 01, 1900)
        self.tr_x = []  # X, UTM34N
        self.tr_y = []  # Y, UTM34N
        self.tr_sv = []  # SoundSpeedSensor Measurements
        self.tr_depth = []  # Nadir Depth... Depth below SRF
        self.tr_heading = []  # Heading
