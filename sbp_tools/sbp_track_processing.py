import os
from datetime import datetime, time, date, timezone, timedelta
from filemanager import file_ext_search as fes
from dataclasses import dataclass, field
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

@dataclass
class SegyPosFile:
    name: str
    path: str
    fin_traceno: int = 0
    datetime: list = field(default_factory=list)
    traceno: list = field(default_factory=list)
    cdp_x: list = field(default_factory=list)
    cdp_x_smoothed: list = field(default_factory=list)
    cdp_y_smoothed: list = field(default_factory=list)
    cdp_x_cartesian_smoothed: list = field(default_factory=list)
    cdp_y_cartesian_smoothed: list = field(default_factory=list)
    cdp_y: list = field(default_factory=list)
    year: list = field(default_factory=list)
    day: list = field(default_factory=list)
    hour: list = field(default_factory=list)
    minute: list = field(default_factory=list)
    second: list = field(default_factory=list)
    

def read_segypos(pos_files, finedict, baddict, posobj_list, year, utm_coords=False):
    for pos_file in pos_files:
        segy_name = os.path.splitext(os.path.basename(pos_file))[0]
        pos_obj = SegyPosFile(name=segy_name, path=pos_file)
        
        number = 0
        has_error = False
        was_before = False
        
        with open(pos_file, 'r') as file1:
            file_content = file1.read().splitlines()
            
            for line in file_content[1:]:
                line_content = line.split()

                try:
                    
                    if int(line_content[3]) != year:
                        raise RuntimeError('BadYear')
                    
                    elif int(int(line_content[4])) > 370 and int(line_content[4]) < 0:
                        raise RuntimeError('BadDay')
                    
                    elif int(int(line_content[4])) > 24 and int(line_content[5]) < 0:
                        raise RuntimeError('BadHour')
                    
                    elif int(int(line_content[4])) > 60 and int(line_content[6]) < 0:
                        raise RuntimeError('BadMin')
                    
                    elif int(int(line_content[4])) > 60 and int(line_content[7]) < 0:
                        raise RuntimeError('BadSec')
                    
                    if utm_coords:
                        if float(line_content[1]) < 50000 and float(line_content[1]) > 700000:
                            raise RuntimeError('BadCDP_X')
                        
                        elif float(line_content[2]) < 200000 and float(line_content[2]) > 8000000:
                            raise RuntimeError('BadCDP_Y')

                    else:
                        if float(line_content[1]) < 15.0 and float(line_content[1]) > 50.0:
                            raise RuntimeError('BadCDP_X')
                        
                        elif float(line_content[2]) < 30.0 and float(line_content[2]) > 70.0:
                            raise RuntimeError('BadCDP_Y')
                    
                    ar = time(hour=int(line_content[5]),
                            minute=int(line_content[6]), second=int(line_content[7]))
                except:
                    number += 1
                    has_error = True
                    if not was_before:
                        baddict[segy_name] = pos_obj.traceno[-1]
                        was_before = True
                        
                else:
                    pos_obj.datetime.append(f'{line_content[3]}-{line_content[4]}T{line_content[5]}:{line_content[6]}:{line_content[7]}')
                    pos_obj.traceno.append(int(line_content[0]))
                    pos_obj.cdp_x.append(float(line_content[1]))
                    pos_obj.cdp_y.append(float(line_content[2]))
                    pos_obj.year.append(int(line_content[3]))
                    pos_obj.day.append(int(line_content[4]))
                    pos_obj.hour.append(int(line_content[5]))
                    pos_obj.minute.append(int(line_content[6]))
                    pos_obj.second.append(int(line_content[7]))
                    
            finedict[segy_name] = pos_obj.traceno[-1]
            
            if has_error:
                print(f'Number of bad lines in {segy_name}: {number}')
                
            posobj_list.append(pos_obj)
            
            
def process_track(pos_objs, transformer, window_length=201, smooth=True, utm_coords=False):
    for segy_pos_obj in pos_objs:
        window_length = window_length
        file_length = len(segy_pos_obj.cdp_x)
        
        loop = True
        while loop:
            if window_length > file_length/4 and window_length > 101:
                window_length = int(window_length/4)

            elif window_length > file_length or window_length < 10:
                loop = False
            else:
                loop = False
        
        if smooth is False:
            if utm_coords:
                cartesian_x = segy_pos_obj.cdp_x
                cartesian_y = segy_pos_obj.cdp_y
            else:
                cartesian_x, cartesian_y = transformer.transform(segy_pos_obj.cdp_x, segy_pos_obj.cdp_y)
            
            segy_pos_obj.cdp_x_cartesian_smoothed = cartesian_x
            segy_pos_obj.cdp_y_cartesian_smoothed = cartesian_y
        
        elif window_length > file_length or window_length < 10:
            print(f'Can not smooth file {segy_pos_obj.name}')
            
            if utm_coords:
                cartesian_x = segy_pos_obj.cdp_x
                cartesian_y = segy_pos_obj.cdp_y
            else:
                cartesian_x, cartesian_y = transformer.transform(segy_pos_obj.cdp_x, segy_pos_obj.cdp_y)
                
            if '_not_smoothed' in segy_pos_obj.name:
                pass
            else:
                segy_pos_obj.name = segy_pos_obj.name + '_not_smoothed'
            
            segy_pos_obj.cdp_x_cartesian_smoothed = cartesian_x
            segy_pos_obj.cdp_y_cartesian_smoothed = cartesian_y
        
        else:
            segy_pos_obj.cpd_x_smoothed = signal.savgol_filter(segy_pos_obj.cdp_x,window_length,3)
            segy_pos_obj.cpd_y_smoothed = signal.savgol_filter(segy_pos_obj.cdp_y,window_length,3)
            
            if utm_coords:
                cartesian_x = segy_pos_obj.cpd_x_smoothed
                cartesian_y = segy_pos_obj.cpd_y_smoothed
            else:
                cartesian_x, cartesian_y = transformer.transform(segy_pos_obj.cpd_x_smoothed, segy_pos_obj.cpd_y_smoothed)
        
            segy_pos_obj.cdp_x_cartesian_smoothed = cartesian_x.tolist()
            segy_pos_obj.cdp_y_cartesian_smoothed = cartesian_y.tolist()

def save_track(pos_objs, save_to):
    with open(save_to, 'w') as file2:
        file2.write('num_o,num_i,name,datetime,traceno,cdp_x,cdp_y,year,day,hour,minute,second\n')
        num_o = 0
        num_f = 0
        
        for segy_pos_obj in pos_objs:
            
            if '_rawpos' in segy_pos_obj.name:
                name = segy_pos_obj.name[:-7]
            else:
                name = segy_pos_obj.name
            
            for num_i,traceno in enumerate(segy_pos_obj.traceno):
                file2.write(f'{num_o},{num_i},{name},{segy_pos_obj.datetime[num_i]},{segy_pos_obj.traceno[num_i]},{segy_pos_obj.cdp_x_cartesian_smoothed[num_i]},')
                file2.write(f'{segy_pos_obj.cdp_y_cartesian_smoothed[num_i]},{segy_pos_obj.year[num_i]},{segy_pos_obj.day[num_i]},{segy_pos_obj.hour[num_i]},{segy_pos_obj.minute[num_i]},')
                file2.write(f'{segy_pos_obj.second[num_i]}\n')
                num_o += 1
                
            num_f += 1
            print(f'File {segy_pos_obj.name} is done {num_f} of {len(pos_objs)}')
            
def save_track_to_radex(pos_objs):
        
    for pos_obj in pos_objs:
        save_to = os.path.dirname(pos_obj.path)
        
        if '_rawpos' in pos_obj.name:
            name = pos_obj.name[:-7]
        else:
            name = pos_obj.name
    
        with open(os.path.join(save_to, name + '_proc.txt'), 'w') as file3:
            file3.write(f'TraceNo\tCDPX\tCDPY\n')
            for num, cdp_x in enumerate(pos_obj.cdp_x_cartesian_smoothed):
                file3.write(f'{pos_obj.traceno[num]}\t{pos_obj.cdp_x_cartesian_smoothed[num]}\t{pos_obj.cdp_y_cartesian_smoothed[num]}\n')
                

def proc_track_from_pds(trackfile_paths, save_to, cruisename, delimiter=','):
    delimeter = delimiter

    yearday_dict = {}

    for trackfile in trackfile_paths:
        with open(trackfile, 'r') as f1:
            file_content = f1.read().splitlines()
            
            for line in file_content:
                line_content = line.split(delimeter)
                
                posix_time = float(line_content[0])
                datetime_pds = line_content[1]
                x_coord = float(line_content[2])
                y_coord = float(line_content[3])
                
                datetime_conv = datetime.fromtimestamp(posix_time, tz=timezone.utc)
                
                year_day = datetime_conv.strftime('%Y_%j')
                        
                if year_day in yearday_dict.keys():
                    pass
                else:
                    yearday_dict[year_day] = []
                
                file_string = f'{posix_time:.05f} {x_coord:.04f} {y_coord:.04f} '+ datetime_conv.strftime('%Y %m %d %j %H %M %S %f')
                yearday_dict[year_day].append(file_string)
                
    for key_yearday in yearday_dict.keys():
        trackfile_yearday = os.path.join(save_to, cruisename + '_' + key_yearday + '.txt')
        
        with open(trackfile_yearday, 'w') as f2:
            f2.write('posix_timestamp x y year day month yearday hour minute second microsecond\n')
            
            yearday_dict[key_yearday].sort()
            for line in yearday_dict[key_yearday]:
                f2.write(f'{line}\n')

