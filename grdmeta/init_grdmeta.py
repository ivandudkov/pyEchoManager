import os
import sys
from osgeo import ogr, osr, gdal
import numpy as np
import time

from grdmeta.polygonize_esriascii import gdal_polygonize_esriiascii
from filemanager.file_ext_search import file_ext_search
from cli.color import color

def polygonize_grd(input_path, output_path, espg_code, grid_ext=0):
    
    if grid_ext == 0:
        extension = '.asc'
    elif grid_ext == 1:
        extension = '.tiff'
    else:
        raise RuntimeError('Grid extention should be either 0 (ESRI ASCII grid) or 1 (tiff grid)')
    
    grid_list = file_ext_search(extension=extension, path=input_path)
    shp_list = []

    num = 0
    for file in grid_list:
        shp_list.append(
            os.path.join(output_path, os.path.splitext(os.path.basename(file))[0] + '.shp'))
        print(f'{num} {file}')
        num += 1
    
    f_num = 1
    f_overall = len(grid_list)

    print(f"{color.BOLD}Polygonizing the ESRII ASCII fileset with \
    {color.BLUE}{f_overall}{color.END} files \n{color.END}")
    print(f"Input directory: {color.GREEN}\"{input_path}\"{color.END}")
    print(f"Output direcroty: {color.GREEN}\"{output_path}\"{color.END}\n\n")

    t00 = time.time()
    for grd, shp in zip(grid_list, shp_list):
        f_name = os.path.splitext(os.path.basename(grd))[0]
        
        print(f'Polygonizing the file {color.RED}#{f_num}{color.END}: {color.BLUE}{f_name}{color.END}')
        t0 = time.time()
        gdal_polygonize_esriiascii(inpath=grd, outpath=shp, espgcrf=espg_code)
        print(f'Processed {color.BLUE}{f_num}{color.END} out of {color.BLUE}{f_overall}{color.END} ESRII ASCII files')
        f_num += 1
        print(f'Time elapsed for the procedure: {color.BLUE}{time.time() - t0:.2f}{color.END} seconds')
        print(f'Overall time elapsed: {color.BLUE}{(time.time() - t00) / 60:.2f}{color.END} minutes\n')
        
