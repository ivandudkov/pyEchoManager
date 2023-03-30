import abc
import os


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
        self.tr_sv = []  # SoundSpeedSensor Measurements
        self.tr_depth = []  # Transducer depth (below VRF)
        self.dbt_depth = []
        self.nadir_depth = []
        self.tr_heading = []  # Heading
        self.header = {}

@classmethod
def set_up_header():
    pass

def read_filetrack_csv(input, i_header, projection):
    PDS_file_tracks = []

    with open(input, 'r') as f:
        file_content = f.read().splitlines()
        i_header = i_header
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
                    print(f'error at line {num}. {i_header[count]}: {line_content[count]}')
                else:
                    count = 0
                    f_tr.tr_time.append(float(line_content[0]))
                    f_tr.tr_x.append(float(line_content[1]))
                    f_tr.tr_y.append(float(line_content[2]))
                    f_tr.tr_sv.append(float(line_content[3]))
                    f_tr.tr_depth.append(float(line_content[4]))
                    f_tr.tr_heading.append(float(line_content[5]))
                
        return PDS_file_tracks
