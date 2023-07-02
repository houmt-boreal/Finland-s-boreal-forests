#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,glob
import numpy as np
import pandas as pd
from calendar import monthrange
from osgeo import gdal, gdal_array

inDs=gdal.Open(r"D:\griddata_fi\new2018\Daily mean temperature_tif\mean_tem_day_2002_2018\tday_2005.tif")
gt=inDs.GetGeoTransform()
srs=inDs.GetProjection()

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



OUTPUT_FOLDER= r'D:\griddata_fi\new2018\pre\pre_monthly'

INPUT_FOLDER= r'D:\griddata_fi\new2018\pre\2001_2018'
files = glob.glob(os.path.join(INPUT_FOLDER, '*.tif'))


for innc in files:
    fy = innc[len(innc) - 8:len(innc) - 4] # get some characters from fileneme
    # ff = int(fy)   # string, floating point → integer
    raster = gdal.Open(innc)
    for i in range(1, 13):
        if i > 9:
            mon = str(i)
        else:
            mon = "0" + str(i)
        # print nn[1]
        data2 = raster.GetRasterBand(i).ReadAsArray().astype('float')
        # mean = np.mean(data[data != 0])   #calculate mean without value 0
        # data2=np.sum(myarray, axis=0)
        # data2=np.mean(myarray, axis=0)
        # if (ff == 2003) & (i == 10):
        #     print band
        #     outcsv = r'D:/cli_20131001n.csv'
        #     np.savetxt(outcsv, myarray[0,:,:], delimiter=',',  comments="")
        data2[data2<-10000] = -9999
        outnc = OUTPUT_FOLDER + '/mean_pre_' + fy+"_"+ mon+ '.tif'
        writeFile(outnc, gt, srs, data2)
        outnc = None


