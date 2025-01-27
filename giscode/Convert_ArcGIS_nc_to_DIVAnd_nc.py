#!/usr/bin/env python
# coding: utf-8

# # 

# In[1]:


from netCDF4 import Dataset
import numpy as np
import os

# Read .nc file, which is ok for DIVAnd:
data_path = os.getcwd() + "\\data\\"
input_ArcGIS_nc_bathymetry = data_path + "Doldrums_ANS33_SRTM15v_15arcsecs.nc"
output_DIVAnd_nc_bathymetry = data_path + "Doldrums_ANS33_SRTM15v_15arcsecs_flipped.nc"


# In[2]:


data_path_trend = os.getcwd() + "\\data\\trend_nc_data\\mean10\\"

input_trend1  = data_path_trend + "Trend_10mean_3800m.nc"
input_trend2  = data_path_trend + "Trend_10mean_3900m.nc"
input_trend3  = data_path_trend + "Trend_10mean_4000m.nc"
input_trend4  = data_path_trend + "Trend_10mean_4100m.nc"
input_trend5  = data_path_trend + "Trend_10mean_4200m.nc"
input_list = [input_trend1, input_trend2, input_trend3, input_trend4, input_trend5]

output_trend1  = data_path_trend + "Trend_10mean_3800m_diva.nc"
output_trend2  = data_path_trend + "Trend_10mean_3900m_diva.nc"
output_trend3  = data_path_trend + "Trend_10mean_4000m_diva.nc"
output_trend4  = data_path_trend + "Trend_10mean_4100m_diva.nc"
output_trend5  = data_path_trend + "Trend_10mean_4200m_diva.nc"
output_list = [output_trend1, output_trend2, output_trend3, output_trend4, output_trend5]


# # Загрузка переменных из .nc АркГИСа

# In[2]:


# Get ArcGIS .nc data
nc_read_arc = Dataset(input_ArcGIS_nc_bathymetry, 'r')
lat_arc = np.flip(nc_read_arc.variables['lat'][:])
lon_arc = nc_read_arc.variables['lon'][:]
depth_arc = np.flip(nc_read_arc.variables['bat'][:], 0)
nc_read_arc.close


# # Создание .nc файла с кастомной батиметрией для DIVAnd

# In[3]:


# Create new nc-file
rootgrp = Dataset(output_DIVAnd_nc_bathymetry, "w", format="NETCDF3_64BIT_OFFSET")
rootgrp.set_fill_off()
# Creating dimensions
lat = rootgrp.createDimension("lat", len(lat_arc))
lon = rootgrp.createDimension("lon", len(lon_arc))

# Creating variables
longitudes = rootgrp.createVariable("lon","f8",("lon",))
longitudes.long_name = 'Longitude'
longitudes.standard_name = 'longitude'
longitudes.units = 'degrees_east'

latitudes = rootgrp.createVariable("lat","f8",("lat",))
latitudes.long_name = 'Latitude'
latitudes.standard_name = 'latitude'
latitudes.units = 'degrees_north'

Height = rootgrp.createVariable("bat","f4",("lat","lon",))
Height.long_name = 'elevation above sea level'
Height.standard_name = 'height'
Height.units = 'meters'


# Passing data into variables
longitudes[:] = lon_arc
latitudes[:] = lat_arc
Height[:] = depth_arc

print(rootgrp)
print(rootgrp.variables)

# Close .nc file creation
rootgrp.close


# In[3]:


for i in range(len(input_list)):
    # Get ArcGIS .nc data
    nc_read_arc = Dataset(input_list[i], 'r')
    lat_arc = np.flip(nc_read_arc.variables['lat'][:])
    lon_arc = nc_read_arc.variables['lon'][:]
    depth_arc = np.flip(nc_read_arc.variables['bat'][:], 0)
    nc_read_arc.close
    
    # Create new nc-file
    rootgrp = Dataset(output_list[i], "w", format="NETCDF3_64BIT_OFFSET")
    rootgrp.set_fill_off()
    # Creating dimensions
    lat = rootgrp.createDimension("lat", len(lat_arc))
    lon = rootgrp.createDimension("lon", len(lon_arc))

    # Creating variables
    longitudes = rootgrp.createVariable("lon","f8",("lon",))
    longitudes.long_name = 'Longitude'
    longitudes.standard_name = 'longitude'
    longitudes.units = 'degrees_east'

    latitudes = rootgrp.createVariable("lat","f8",("lat",))
    latitudes.long_name = 'Latitude'
    latitudes.standard_name = 'latitude'
    latitudes.units = 'degrees_north'

    Height = rootgrp.createVariable("bat","f4",("lat","lon",))
    Height.long_name = 'elevation above sea level'
    Height.standard_name = 'height'
    Height.units = 'meters'


    # Passing data into variables
    longitudes[:] = lon_arc
    latitudes[:] = lat_arc
    Height[:] = depth_arc

    print(rootgrp)
    print(rootgrp.variables)

    # Close .nc file creation
    rootgrp.close
    


# In[ ]:




