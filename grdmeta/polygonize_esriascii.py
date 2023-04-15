import os
from osgeo import ogr, osr, gdal
import numpy as np


def gdal_polygonize_esriiascii(inpath, outpath, espgcrf):
    # this allows GDAL to throw Python Exceptions
    gdal.UseExceptions()
    
    # Load ESRI ASCII raster
    ds = gdal.Open(inpath)
    
    # Get elevation band and no-data value
    srcband = ds.GetRasterBand(1)
    nodata_val = srcband.GetNoDataValue()
    
    # Create binary band. 1 - data value, 0 - no-data value
    elev_array = srcband.ReadAsArray()
    mask = np.where(elev_array!=nodata_val, 1, 0)
    
    # Temporary dataset
    tmp_ds = gdal.GetDriverByName('MEM').CreateCopy('', ds, 0)
    tmp_ds.AddBand()
    tmp_ds.GetRasterBand(2).WriteArray(mask)
    suppband = tmp_ds.GetRasterBand(2)
    
    # Сreate output datasource
    dst_layername = os.path.split(os.path.splitext(outpath)[0])[0]
    drv = ogr.GetDriverByName("ESRI Shapefile")
    dst_ds = drv.CreateDataSource(outpath)
    dst_layer = dst_ds.CreateLayer(dst_layername, srs = None )

    gdal.Polygonize(suppband, suppband, dst_layer, -1, [], callback=None )
    
    # Write crf information for the output shapefile
    sr_crf = osr.SpatialReference()
    sr_crf.ImportFromEPSG(espgcrf)
    sr_crf.MorphToESRI()
    file = open(os.path.splitext(outpath)[0] + '.prj', 'w')
    file.write(sr_crf.ExportToWkt())
    file.close()
    
    del ds
    del tmp_ds
    del dst_ds
    