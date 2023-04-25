import os
import sys

from filemanager.filetrack import PDSFileTrack

tracktable_path = r'D:\aa_yandexcloud\aa_cloudmbesproceessing\aa_abp50_processing\TTR21_KaraSea_MPP_p02.csv'
output_file_path = r'D:\aa_yandexcloud\aa_cloudmbesproceessing\aa_abp50_processing\TTR21_KaraSea_MPP_p02_proc.csv'

# tracktable_paths = find_file_with_extension('.csv',tracktable_folder)
# for tracktable in tracktable_paths:
#     name = os.path.splitext(os.path.split(tracktable)[1])[0] + '_proc.csv'
#     output_file_path = os.path.join(output_folder, name)
    
#     ft_obj_list = read_filetrack_csv(tracktable, 'LambConfConic2Par_TTR21')
#     create_fsets_path_csv(ft_obj_list, output_file_path, fs_obj_list=None)
    
# if header is 'Time,X,Y,SSV,Nadir,Heading'
# i_headseq should be [0,1,2,3,4,5]
ft_obj_list = PDSFileTrack.read_filetrack_csv(input=tracktable_path, i_headseq=[0,1,2,3,4,5], projection='LambConfConic2Par_TTR21')
# Create one CSV file for all filesets and files:
PDSFileTrack.create_fsets_path_csv(ft_obj_list, output_file_path, fs_obj_list=None)




