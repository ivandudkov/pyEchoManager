
#%%
import os
import numpy as np

from assignsvp import assignsvp as asvp

path01_svpmeta = r'D:\aa_yandexcloud\aa_cloudmbesproceessing\aa_abp50_processing\assignsvp\ABP50_TTR21_assignsvp_preproc02.csv'
path02_pdstrack = r'D:\aa_yandexcloud\aa_cloudmbesproceessing\aa_abp50_processing\TTR21_KaraSea_MPP_p02.csv'
path03_output = r'D:\aa_yandexcloud\aa_cloudmbesproceessing\aa_abp50_processing\TTR21_KaraSea_MPP_p02_proc_svp.csv'
path_04_output_stnd = r'D:\aa_yandexcloud\aa_cloudmbesproceessing\aa_abp50_processing\TTR21_KaraSea_MPP_p02_proc_svp_stnd.csv'

assign_svp = asvp.AssignSvp()

assign_svp.read_svpmeta(path_svpmeta=path01_svpmeta)
assign_svp.read_filetrack_csv(input=path02_pdstrack, i_headseq=[0,1,2,3,4,5], projection='LambConfConic2Par_TTR21')
#%%
assign_svp.create_arrays()
print('over')

# %%
svp_file = assign_svp.svp_profiles[431]
print(svp_file)
# %%
assign_svp.save_matched_track(assign_svp.pds_files, assign_svp.svp_profiles, path03_output)
# %%
path_04_output_stnd = r'D:\aa_yandexcloud\aa_cloudmbesproceessing\aa_abp50_processing\TTR21_KaraSea_MPP_p02_proc_svp_stnd.csv'
assign_svp.save_matched_track(assign_svp.pds_files, assign_svp.svp_profiles, path_04_output_stnd, True)
# %%
p = {}

p['amm'] = []
p['amm'].append('aa')
p['amm'].append('ab')

print(p)
# %%
import os
import numpy as np

from assignsvp import assignsvp as asvp
assign_svp = asvp.AssignSvp()

spreadsheet = r'D:\aa_yandexcloud\aa_cloudmbesproceessing\aa_abp50_processing\test01.csv'
output = r'D:\aa_yandexcloud\aa_cloudmbesproceessing\aa_abp50_processing\test01_output.csv'
assign_svp.assign_svp_filesets(spreadsheet=spreadsheet, output=output, header_seq=[0,1,5], prefix='ttr21')


# %%
