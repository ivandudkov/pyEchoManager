import os
import sys


def write_miniSVP_metadata(SVP_path, SVP_list_path):
    with open(SVP_path, 'r') as f:
        file_content = f.read().splitlines()

    date = file_content[0].split(' ')[1].split('/')
    time = file_content[0].split(' ')[2].split(':')

    datetime = f'{date[2]}-{date[1]}-{date[0]}T{time[0]}:{time[1]}:{time[2]}'
    serial_num = file_content[2].split(' ')[2]
    filename = os.path.split(SVP_path)[-1].split('.')[0]

    if os.path.exists(SVP_list_path):
        with open(SVP_list_path, 'a') as f:
            f.write(f"{datetime}\t{serial_num}\t{filename}\n")
    else:
        with open(SVP_list_path, 'w') as f:
            f.write('Datatime\tS/N\tFname\n')
            f.write(f"{datetime}\t{serial_num}\t{filename}\n")