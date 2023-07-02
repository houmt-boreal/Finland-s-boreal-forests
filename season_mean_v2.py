#!/usr/bin/env python
# -*- coding: utf-8 -*-

from osgeo import gdal, gdal_array
import numpy as np
import glob,os

def writeFile(filename, geotransform, geoprojection, data):
    (rows, cols) = data.shape
    format = "GTiff"

    noDataValue = -9999  # 将-999赋予为nodata

    driver = gdal.GetDriverByName(format)
    # you can change the dataformat but be sure to be able to store negative values including -9999
    dst_datatype = gdal.GDT_Float32

    dst_ds = driver.Create(filename, cols, rows, 1, dst_datatype)
    dst_ds.SetGeoTransform(geotransform)
    dst_ds.SetProjection(geoprojection)
    dst_ds.GetRasterBand(1).WriteArray(data)
    dst_ds.GetRasterBand(1).SetNoDataValue(noDataValue)
    # return 1


in_directory1 = r'D:\griddata_fi\new2018\pre\pre_monthly'
files1 = glob.glob(os.path.join(in_directory1, '*06.tif'))

in_directory2 = r'D:\griddata_fi\new2018\pre\pre_monthly'
files2 = glob.glob(os.path.join(in_directory2, '*07.tif'))

in_directory3 = r'D:\griddata_fi\new2018\pre\pre_monthly'
files3 = glob.glob(os.path.join(in_directory3, '*08.tif'))

OUTPUT_FOLDER=r'D:\griddata_fi\new2018\pre\summer'


for filea,fileb, filec in zip(files1,files2,files3):
    output = OUTPUT_FOLDER + '/mean_pre' + filea[len(filea) - 11:len(filea) - 6] + 'summer.tif'
    # outRaster2 = OUTPUT_FOLDER + '/max_ppi' + filea[len(filea) - 11:len(filea) - 6] + '_summer.tif'
    # Open band 1 as array
    ds_a = gdal.Open(filea)
    b_a = ds_a.GetRasterBand(1)
    arr_a = b_a.ReadAsArray()

    ds_b = gdal.Open(fileb)
    b_b = ds_b.GetRasterBand(1)
    arr_b = b_b.ReadAsArray()

    ds_c = gdal.Open(filec)
    b_c = ds_c.GetRasterBand(1)
    arr_c = b_c.ReadAsArray()

    data2=(arr_a+arr_b+arr_c)/3     # not ignore nan
    # data2 = np.maximum(arr_a, arr_b, arr_c)   # not ignore nan

    data2[data2<-90]=-9999

    gt = ds_b.GetGeoTransform()
    srs = ds_b.GetProjection()


    writeFile(output, gt, srs, data2)

    ds_a = None
    ds_b = None
    ds_c = None
    data2 = None
print 'ok'






