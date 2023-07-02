#!/usr/bin/env python
# -*- coding: utf-8 -*-
from osgeo import gdal, gdal_array
import numpy as np
import glob,os
from calendar import monthrange



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




in_directory = r'D:\cru4.03\pet_mm-day_global'
files = glob.glob(os.path.join(in_directory, '*.tif'))


for innc in files:
    fy = innc[len(innc) - 10:len(innc) - 6] # get some characters from fileneme
    ff = int(fy)   # string, floating point → integer
    fm = innc[len(innc) - 6:len(innc) - 4]  # get some characters from fileneme
    mm = int(fm)
    nn = monthrange(ff, mm)
    days=nn[1]

    raster = gdal.Open(innc)
    b_c = raster.GetRasterBand(1)
    arr_c = b_c.ReadAsArray()

    nod=np.min(arr_c)
    data2 = np.where((arr_c!=nod), arr_c*days, -9999)


    gt = raster.GetGeoTransform()
    srs = raster.GetProjection()

    output = r'D:\cru4.03\pet_mm-monthly_global\pet_month_sum_'+ innc[len(innc) - 10:len(innc) - 0]
    writeFile(output, gt, srs, data2)
    raster = None
    data2 = None



