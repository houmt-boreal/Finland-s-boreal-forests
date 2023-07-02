#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xlrd import open_workbook
from pandas import DataFrame
from osgeo import gdal
import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
import glob
import os
import fnmatch
gdal.AllRegister()

rows = 216
cols = 454


in_directory1 = r'D:\\GIMMS3g_v1\\Fennoscandia_ndvi_raw_tif'
files1 = glob.glob(os.path.join(in_directory1, '*.tif'))

in_directory2 = r'D:\\GIMMS3g_v1\\Fennoscandia_ndvi_flag_raw_tif'
files2 = glob.glob(os.path.join(in_directory2, '*.tif'))

print files1
print files2

inDs = gdal.Open("D:\\GIMMS3g_v1\\Fennoscandia_ndvi_raw_tif\\Fennoscandia_ndvi_1982_072.tif")
driver = inDs.GetDriver()


alist=[]
for filea1 in files1:
    # print filea1
    ds1 = gdal.Open(filea1, gdal.GA_ReadOnly)
    ary1 = ds1.GetRasterBand(1).ReadAsArray()
    ss1 = ary1[:, :]
    alist.append(ss1)
array_ndvi = np.asarray(alist)


blist=[]
for filea2 in files2:
    # print filea2
    ds2 = gdal.Open(filea2, gdal.GA_ReadOnly)
    ary2 = ds2.GetRasterBand(1).ReadAsArray()
    ss2 = ary2[:, :]
    blist.append(ss2)
array_flag = np.asarray(blist)
print np.shape(array_flag)

star=0
cxx = pd.date_range('1982-01-01', '2015-12-31', freq='MS').strftime("%Y-%m").tolist()
for ste in xrange(0,816,2):
    ndvi_mean = np.empty([rows, cols])
    # tau1= np.empty([rows, cols])
    flag_max = np.empty([rows, cols])
    for col in xrange(cols):
      #print col
      for row in xrange(rows):
        #for bimon in xrange(2):
        ndvi0 = array_ndvi[ste, row, col]
        ndvi1 = array_ndvi[ste+1, row, col]
        ndvi0=ndvi0/10000.0
        ndvi1=ndvi1/10000.0
        flag0 = array_flag[ste, row, col]
        flag1 = array_flag[ste + 1, row, col]
        # mean
        if (ndvi0 >= -0.3) and (ndvi0 <= 1) and (ndvi1 >= -0.3) and (ndvi1 <= 1) and (flag0 <= 3000) and (flag1 <= 3000):  # for maxNDVI<=0
            ndvi_mean[row, col] = (ndvi0+ndvi1)/2
            flag_max[row, col] = min(flag0,flag1)
        else:
            ndvi_mean[row, col] = np.nan
            flag_max[row, col] = 4000

        # Python 3.4
        # from statistics import mean, median
        # somelist = [1, 12, 2, 53, 23, 6, 17]
        # avg_value = mean(somelist)
        # median_value = median(somelist)

        # mvc
        # ndvi_max[row, col] = max(ndvi0,ndvi1)
        # if (ndvi0<ndvi1):  # for maxNDVI<=0
        #     flag_max[row, col] = flag1
        # elif (ndvi0>ndvi1):
        #     flag_max[row, col] = flag0
        # else:
        #     flag_max[row, col] = min(flag0,flag1)
    mon=cxx[star][len(cxx[star]) - 2:len(cxx[star])-0]
    yy=cxx[star][len(cxx[star]) - 7:len(cxx[star])-3]
    star=star+1
    outDs1 = driver.Create('D:\\GIMMS3g_v1\\Fenno_ndvi_mean_month_del_flag3\\fi_ndvi_mean_' + yy + '_' + mon + '.tif', cols, rows, 1, gdal.GDT_Float32)
    outDs1.SetGeoTransform(inDs.GetGeoTransform())
    outDs1.SetProjection(inDs.GetProjection())
    # print outDatas[90,270,i]
    outBand1 = outDs1.GetRasterBand(1)
    # outBand1.WriteArray(np.amax(blist, axis=0))  # get maximum
    outBand1.WriteArray(ndvi_mean[:, :])
    # outBand1.SetNoDataValue(-9999)
    outBand1 = None
    outDs1 = None

    outDs2 = driver.Create('D:\\GIMMS3g_v1\\Fenno_ndvi_mean_month_del_flag3\\fi_flag_mean_' + yy + '_' + mon + '.tif', cols, rows, 1, gdal.GDT_Float32)
    outDs2.SetGeoTransform(inDs.GetGeoTransform())
    outDs2.SetProjection(inDs.GetProjection())
    # print outDatas[90,270,i]
    outBand2 = outDs2.GetRasterBand(1)
    outBand2.WriteArray(flag_max[:, :])  # get count
    # outBand2.SetNoDataValue(11111)
    outBand2 = None
    outDs2 = None

print 'ok'






