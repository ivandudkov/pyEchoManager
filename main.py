import os
from cli import cli

path = r'C:\YandexDisk\aa_cloudmbesproceessing\aa_abp55_processing\DTM\CSV_From_Realtime'

csv_files = cli.search(path, '.csv')


for file in csv_files:
    print(f'Start processing {file}')
    xyz = []
    
    new_file = os.path.join(path,'mod_' + os.path.basename(file))
    with open(file, 'r') as f1:
        f1_content = f1.read().splitlines()
        
        for line in f1_content:
            line_content = line.split(';')
            x = line_content[0]
            y = line_content[1]
            z = line_content[2]
            xyz.append(f'{x},{y},{z}\n')
            
            
    with open(new_file, 'w') as f2:
        f2.write('x,y,z\n')
        
        for xyz_line in xyz:
            f2.write(xyz_line)
            
    print(f'file {file} done')