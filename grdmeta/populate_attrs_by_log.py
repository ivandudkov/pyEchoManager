import os
import sys
from osgeo import ogr, osr, gdal
import numpy as np
import time


def pop_attrs(path, logline):
    extension = os.path.splitext(path)[-1]
    
    if extension == '.gpkg':
        drv = ogr.GetDriverByName('GPKG')
    elif extension == '.shp':
        drv = ogr.GetDriverByName('ESRI Shapefile')
    else:
        raise RuntimeError(f"{path} extention is not valid")
        
    ogrData = drv.Open(path, 1)  # 0/1 is read/write

    # https://gdal.org/python/osgeo.ogr-module.html, search OFT
    # Field name - max 10 chars
    fld_ID = ogr.FieldDefn('ID', ogr.OFTInteger)
    fld_Cruise = ogr.FieldDefn('Cruise', ogr.OFTString)
    fld_Cruise.SetWidth(10)
    fld_Platform = ogr.FieldDefn('Platform', ogr.OFTString)
    fld_Platform.SetWidth(100)
    fld_DateStart = ogr.FieldDefn('DateStart', ogr.OFTString)
    fld_DateStart.SetWidth(10)
    fld_DateEnd = ogr.FieldDefn('DateEnd', ogr.OFTString)
    fld_DateEnd.SetWidth(10)
    fld_Type = ogr.FieldDefn('Type', ogr.OFTString)
    fld_Type.SetWidth(10)
    fld_Instrument = ogr.FieldDefn('Instrument', ogr.OFTString)
    fld_Instrument.SetWidth(50)
    fld_CRF = ogr.FieldDefn('CRF', ogr.OFTString)
    fld_CRF.SetWidth(150)
    fld_Fileset = ogr.FieldDefn('Fileset', ogr.OFTString)
    fld_Fileset.SetWidth(150)
    fld_DTM_Resolution = ogr.FieldDefn('DTM_Res', ogr.OFTString)
    fld_DTM_Resolution.SetWidth(50)
    fld_Backscatter_Resolution = ogr.FieldDefn('BS_Res', ogr.OFTString)
    fld_Backscatter_Resolution.SetWidth(50)
    fld_Comments = ogr.FieldDefn('Comments', ogr.OFTString)
    fld_Comments.SetWidth(250)
    fld_Disk = ogr.FieldDefn('Disk', ogr.OFTString)
    fld_Disk.SetWidth(100)
    fld_Folder = ogr.FieldDefn('Folder', ogr.OFTString)
    fld_Folder.SetWidth(100)
    fld_Processed_by = ogr.FieldDefn('Procssd_by', ogr.OFTString)
    fld_Processed_by.SetWidth(100)
    fld_Responsible = ogr.FieldDefn('Responsbl', ogr.OFTString)
    fld_Responsible.SetWidth(50)
    
    layer = ogrData[0]
    layer.ResetReading()  # чтобы быть уверенным, что мы в начале слоя

    layer.CreateField(fld_ID)
    layer.CreateField(fld_Cruise)
    layer.CreateField(fld_Platform)
    layer.CreateField(fld_DateStart)
    layer.CreateField(fld_DateEnd)
    layer.CreateField(fld_Type)
    layer.CreateField(fld_Instrument)
    layer.CreateField(fld_CRF)
    layer.CreateField(fld_Fileset)
    layer.CreateField(fld_DTM_Resolution)
    layer.CreateField(fld_Backscatter_Resolution)
    layer.CreateField(fld_Comments)
    layer.CreateField(fld_Disk)
    layer.CreateField(fld_Folder)
    layer.CreateField(fld_Processed_by)
    layer.CreateField(fld_Responsible)
    
    feature = layer.GetNextFeature()


    metadata_list = logline.content

    while feature:
        feature.SetField("ID", int(metadata_list[0]))
        feature.SetField("Cruise", metadata_list[1])
        feature.SetField("Platform", metadata_list[2])
        feature.SetField("DateStart", metadata_list[3])
        feature.SetField("DateEnd", metadata_list[4])
        feature.SetField("Type", metadata_list[5])
        feature.SetField("Instrument", metadata_list[6])
        feature.SetField("CRF", metadata_list[7])
        feature.SetField("Fileset", metadata_list[8])
        feature.SetField("DTM_Res", metadata_list[9])
        feature.SetField("BS_Res", metadata_list[10])
        feature.SetField("Comments", metadata_list[11])
        feature.SetField("Disk", metadata_list[12])
        feature.SetField("Folder", metadata_list[13])
        feature.SetField("Procssd_by", metadata_list[14])
        feature.SetField("Responsbl", metadata_list[15])

        layer.SetFeature(feature)
        feature = layer.GetNextFeature()

    ogrData.Destroy()
    
def repop_attrs(path, logline):
    extension = os.path.splitext(path)[-1]
    
    if extension == '.gpkg':
        drv = ogr.GetDriverByName('GPKG')
    elif extension == '.shp':
        drv = ogr.GetDriverByName('ESRI Shapefile')
    else:
        raise RuntimeError(f"{path} extention is not valid")
        
    ogrData = drv.Open(path, 1)  # 0/1 is read/write
    layer = ogrData[0]
    layer.ResetReading()  # чтобы быть уверенным, что мы в начале слоя
    
    feature = layer.GetNextFeature()
    metadata_list = logline.content

    while feature:
        feature.SetField("ID", int(metadata_list[0]))
        feature.SetField("Cruise", metadata_list[1])
        feature.SetField("Platform", metadata_list[2])
        feature.SetField("DateStart", metadata_list[3])
        feature.SetField("DateEnd", metadata_list[4])
        feature.SetField("Type", metadata_list[5])
        feature.SetField("Instrument", metadata_list[6])
        feature.SetField("CRF", metadata_list[7])
        feature.SetField("Fileset", metadata_list[8])
        feature.SetField("DTM_Res", metadata_list[9])
        feature.SetField("BS_Res", metadata_list[10])
        feature.SetField("Comments", metadata_list[11])
        feature.SetField("Disk", metadata_list[12])
        feature.SetField("Folder", metadata_list[13])
        feature.SetField("Procssd_by", metadata_list[14])
        feature.SetField("Responsbl", metadata_list[15])

        layer.SetFeature(feature)
        feature = layer.GetNextFeature()

    ogrData.Destroy()