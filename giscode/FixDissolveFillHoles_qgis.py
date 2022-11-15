from mbesmanager.polygonize_esriascii import gdal_polygonize_esriiascii
from mbesmanager.file_ext_search import file_ext_search
from mbesmanager.file_path_modify import file_path_modify

import os
import sys
from osgeo import ogr, osr, gdal
import numpy as np

import processing
data_path = './dtm'

asc_files = file_ext_search(extension='.asc', path=data_path)
shp_files = []
espg_crf_wgs84utm34n = 32634

for file in asc_files:
    shp_files.append(file[:-4] + '.shp')
print(shp_files)

out_file = shp_files[0][:-4] + "fg.shp"

# processing.run("native:fixgeometries", {"INPUT": shp_files[0],
#                                        "OUTPUT": out_file})

out_file2 = shp_files[0][:-4] + "_dsvld.shp"

processing.run("native:dissolve", {"INPUT": out_file,
                                   "FIELD": [],
                                   "OUTPUT": out_file2})


