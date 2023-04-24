
#%%
import os
import numpy as np

from assignsvp import assignsvp as asvp

path01_svpmeta = r'D:\aa_yandexcloud\aa_cloudmbesproceessing\aa_abp49_processing\assignsvp\hydro_profiles_ctdsvp.csv'
path02_pdstrack = r'D:\aa_yandexcloud\aa_cloudmbesproceessing\aa_abp49_processing\assignsvp_v2\track_data\abp49_id031_DNPoly_Po_Track.csv'
path02_pdstrack2 = r'D:\aa_yandexcloud\aa_cloudmbesproceessing\aa_abp49_processing\assignsvp_v2\track_data\abp49_id032_RBPoly_Po_Track.csv'
path03 = r'D:\aa_yandexcloud\aa_cloudmbesproceessing\aa_abp49_processing\assignsvp_v2\abp49_id032_RBPoly_Po_Track2.csv'

assign_svp = asvp.AssignSvp()

assign_svp.read_svpmeta(path_svpmeta=path01_svpmeta)
assign_svp.read_filetrack_csv(input=path02_pdstrack2, i_headseq=[0,2,3,5,7,-999], projection='WGS84UTM34N')

assign_svp.create_arrays()
print('over')
#%%
pds_file = assign_svp.pds_files[5]
print(pds_file)

# %%
svp_file = assign_svp.svp_profiles[431]
print(svp_file)
# %%
path01_svpmeta = r'D:\aa_yandexcloud\aa_cloudmbesproceessing\aa_abp49_processing\assignsvp\hydro_profiles_ctdsvp.csv'
path02_pdstrack = r'D:\aa_yandexcloud\aa_cloudmbesproceessing\aa_abp49_processing\assignsvp_v2\track_data\abp49_id031_DNPoly_Po_Track.csv'
path02_pdstrack2 = r'D:\aa_yandexcloud\aa_cloudmbesproceessing\aa_abp49_processing\assignsvp_v2\track_data\abp49_id032_RBPoly_Po_Track.csv'
path03 = r'D:\aa_yandexcloud\aa_cloudmbesproceessing\aa_abp49_processing\assignsvp_v2\abp49_id032_RBPoly_Po_Track2.csv'

assign_svp.save_matched_track(assign_svp.pds_files, assign_svp.svp_profiles, path03)
# %%
path01_svpmeta = r'D:\aa_yandexcloud\aa_cloudmbesproceessing\aa_abp49_processing\assignsvp\hydro_profiles_ctdsvp.csv'
path02_pdstrack = r'D:\aa_yandexcloud\aa_cloudmbesproceessing\aa_abp49_processing\assignsvp_v2\track_data\abp49_id031_DNPoly_Po_Track.csv'
path02_pdstrack2 = r'D:\aa_yandexcloud\aa_cloudmbesproceessing\aa_abp49_processing\assignsvp_v2\track_data\abp49_id032_RBPoly_Po_Track.csv'
path03 = r'D:\aa_yandexcloud\aa_cloudmbesproceessing\aa_abp49_processing\assignsvp_v2\abp49_id032_RBPoly_Po_Track12.csv'

assign_svp.save_matched_track_starts_ends(assign_svp.pds_files, assign_svp.svp_profiles, path03)
# %%
print(len(assign_svp.pds_files))
# %%
