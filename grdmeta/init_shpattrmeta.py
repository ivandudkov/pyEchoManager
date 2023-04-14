from .polygonize_esriascii import gdal_polygonize_esriiascii
from mycode.file_ext_search import file_ext_search
# from .file_path_modify import file_path_modify
from .processing_log import ProcessingLog
from .populate_attrs_by_log import pop_attrs
from .populate_attrs_by_log import repop_attrs

import os
import sys
from osgeo import ogr, osr, gdal
import numpy as np
import time

gpkg_path = 'C:\Workspace\Projects\Pr_MBESManager\data\shp'

gpkg_files = file_ext_search(extension='.shp', path=gpkg_path)
espg_crf_wgs84utm34n = 32634

log_path = '.\\data'
log_paths = file_ext_search(extension='.txt', path=log_path)

for num, path in enumerate(log_paths):
    print(f'{num} {path}')

proc_log = ProcessingLog()
proc_log.read_log(log_paths[0])

count = 0
for num, logline in enumerate(proc_log.lines):
    logline_fs = os.path.splitext(logline.name)[0]
    
    for file in gpkg_files:
        fs_name = os.path.splitext(os.path.split(file)[1])[0]
        if logline_fs in fs_name:
            pop_attrs(file, logline)
            # repop_attrs(file, logline)