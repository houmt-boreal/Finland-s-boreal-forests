#!/usr/bin/env python
# -*- coding: utf-8 -*-
from osgeo import gdal, gdal_array
import numpy as np
import glob,os

inDs=gdal.Open("E:/mcd43c4_product/ppi/ppi.20020525.v006.tif")
gt=inDs.GetGeoTransform()
srs=inDs.GetProjection()

def writeFile(filename, geotransform, geoprojection, data):
    (rows, cols) = data.shape
    format = "GTiff"
    # noDataValue = -999  # 将-999赋予为nodata
    driver = gdal.GetDriverByName(format)
    # you can change the dataformat but be sure to be able to store negative values including -9999
    dst_datatype = gdal.GDT_Float32

    dst_ds = driver.Create(filename, cols, rows, 1, dst_datatype)
    dst_ds.SetGeoTransform(geotransform)
    dst_ds.SetProjection(geoprojection)
    dst_ds.GetRasterBand(1).WriteArray(data)
    # dst_ds.GetRasterBand(1).SetNoDataValue(noDataValue)
    # return 1


in_directory = r'E:/mcd43c4_product/ppi'
files = glob.glob(os.path.join(in_directory, '*.tif'))


# OUTPUT_FOLDER= 'G:/mcd43c4_product/ndvi_monthly/max'
OUTPUT_FOLDER2= 'E:/mcd43c4_product/ppi_monthly_max'

for y in range(2002,2019):
   yy=str(y)
   for j in range(5, 10):
        if j > 9:
            mon = str(j)
        else:
            mon = "0" + str(j)
        blist = []
        for filea in files:
            if (filea[len(filea) - 13:len(filea) - 11] == mon)&(filea[len(filea) - 17:len(filea) - 13] == yy):
                ds_a = gdal.Open(filea)
                b_a = ds_a.GetRasterBand(1)
                arr_a = b_a.ReadAsArray()
                blist.append(arr_a)
        myarray = np.asarray(blist)
        data2 = np.nanmax(myarray, axis=0)
        #  data2 = np.nanmean(myarray, axis=0)  # ignoring any NaNs
        # outRaster = OUTPUT_FOLDER + '/ndvi.max.' + yy + mon + '.tif'
        outRaster2 = OUTPUT_FOLDER2 + '/ppi.max.' + yy+mon + '.tif'
        # writeFile(outRaster, gt, srs, data)
        # gdal_array.SaveArray(data.astype("float32"), outRaster, "GTIFF", ds_a)
        gdal_array.SaveArray(data2.astype("float32"), outRaster2, "GTIFF", ds_a)
        ds_a = None
        outRaster2 = None






