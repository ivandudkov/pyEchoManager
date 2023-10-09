import os
import numpy as np

from cli import cli

track_folder = r'\\10.197.125.15\Public\ABP53\abp53_mbes_processing\MBES_Track\raw'
proj = 'WGS84_UTM34N'

# Использование функции поиска трек таблиц
track_list = cli.search(track_folder, '.csv')
print('\n')
# выбор треков для обработки
picked_tracksheet = [track_list[15]]

svpmeta_dir = r'\\10.197.125.15\Public\ABP53\abp53_mbes_processing\SVP_meta'
svpmeta_list = cli.search(svpmeta_dir, '.csv')
picked_svpmeta = [svpmeta_list[2]]


# собственно, обработка
from assignsvp import assignsvp as asvp

output_folder_full = r'\\10.197.125.15\Public\ABP53\abp53_mbes_processing\MBES_Track\processed_full'
# output_folder_stend = r'\\10.197.125.15\Public\ABP53\abp53_mbes_processing\MBES_Track\processed_stend'

for track in picked_tracksheet:
    
    assign_svp = asvp.AssignSvp()
    assign_svp.read_filetrack_csv(input=track, i_headseq=[0,1,2,3,4,5], projection=proj)
    assign_svp.read_svpmeta(path_svpmeta=picked_svpmeta[0])

    assign_svp.create_arrays()
    print('over')
    
    name = os.path.splitext(os.path.basename(track))[0] + '_9' + '.csv'

    output_full = os.path.join(output_folder_full, name)
    # output_stend = os.path.join(output_folder_stend, os.path.basename(track))

    assign_svp.save_matched_track(assign_svp.pds_files, assign_svp.svp_profiles, output_full)
    # assign_svp.save_matched_track(assign_svp.pds_files, assign_svp.svp_profiles, output_stend, True)