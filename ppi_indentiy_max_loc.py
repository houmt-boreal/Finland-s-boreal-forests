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

rows = 116
cols = 68


in_directory1 = r'G:\mcd43c4_product\ppi_monthly_mean_10km_col_row_is_climate'
files1 = glob.glob(os.path.join(in_directory1, '*05.tif'))

in_directory1 = r'G:\mcd43c4_product\ppi_monthly_mean_10km_col_row_is_climate'
files2 = glob.glob(os.path.join(in_directory1, '*06.tif'))

in_directory1 = r'G:\mcd43c4_product\ppi_monthly_mean_10km_col_row_is_climate'
files3 = glob.glob(os.path.join(in_directory1, '*07.tif'))

in_directory1 = r'G:\mcd43c4_product\ppi_monthly_mean_10km_col_row_is_climate'
files4 = glob.glob(os.path.join(in_directory1, '*08.tif'))

in_directory1 = r'G:\mcd43c4_product\ppi_monthly_mean_10km_col_row_is_climate'
files5 = glob.glob(os.path.join(in_directory1, '*09.tif'))



inDs = gdal.Open(r"G:\mcd43c4_product\ppi_monthly_mean_10km_col_row_is_climate\ppi.mean.200707.tif")
driver = inDs.GetDriver()


alist=[]
for filea1 in files1:
    # print filea1
    ds1 = gdal.Open(filea1, gdal.GA_ReadOnly)
    ary1 = ds1.GetRasterBand(1).ReadAsArray()
    ss1 = ary1[:, :]
    alist.append(ss1)
array_1 = np.asarray(alist)


blist=[]
for filea2 in files2:
    # print filea2
    ds2 = gdal.Open(filea2, gdal.GA_ReadOnly)
    ary2 = ds2.GetRasterBand(1).ReadAsArray()
    ss2 = ary2[:, :]
    blist.append(ss2)
array_2 = np.asarray(blist)


clist=[]
for filea3 in files3:
    # print filea1
    ds3 = gdal.Open(filea3, gdal.GA_ReadOnly)
    ary3 = ds3.GetRasterBand(1).ReadAsArray()
    ss3 = ary3[:, :]
    clist.append(ss3)
array_3 = np.asarray(clist)


dlist=[]
for filea4 in files4:
    # print filea2
    ds4 = gdal.Open(filea4, gdal.GA_ReadOnly)
    ary4 = ds4.GetRasterBand(1).ReadAsArray()
    ss4 = ary4[:, :]
    dlist.append(ss4)
array_4 = np.asarray(dlist)

elist=[]
for filea5 in files5:
    # print filea1
    ds5 = gdal.Open(filea5, gdal.GA_ReadOnly)
    ary5 = ds5.GetRasterBand(1).ReadAsArray()
    ss5 = ary5[:, :]
    elist.append(ss5)
array_5 = np.asarray(elist)


print np.shape(array_5)


for ste in xrange(0,17):
    ndvi_max = np.empty([rows, cols])
    # tau1= np.empty([rows, cols])
    flag_max = np.empty([rows, cols])
    for col in xrange(cols):
      #print col
      for row in xrange(rows):
        #for bimon in xrange(2):
        ndvi1 = array_1[ste, row, col]
        ndvi2 = array_2[ste, row, col]
        ndvi3 = array_3[ste, row, col]
        ndvi4 = array_4[ste, row, col]
        ndvi5 = array_5[ste, row, col]
        cvv=[ndvi1,ndvi2,ndvi3,ndvi4,ndvi5]
        cvv=np.asarray(cvv)
        if any(((ii < 0) or (np.isnan(ii))) for ii in cvv):
            ndvi_max[row, col] = -9999
            flag_max[row, col] = -9999
        else:
            max_ppi= max(ndvi1,ndvi2,ndvi3,ndvi4,ndvi5)
            ndvi_max[row, col] = max(ndvi1,ndvi2,ndvi3,ndvi4,ndvi5)
            if (max_ppi==ndvi1):  # for maxNDVI<=0
                flag_max[row, col] = 5   #  loc is May
            elif (max_ppi==ndvi2):
                flag_max[row, col] = 6
            elif (max_ppi == ndvi3):
                flag_max[row, col] = 7
            elif (max_ppi == ndvi4):
                flag_max[row, col] = 8
            elif (max_ppi==ndvi5):
                flag_max[row, col] = 9

    star=str(2002+ste)
    outDs1 = driver.Create(r'G:\mcd43c4_product\ppi_max_' + star + '.tif', cols, rows, 1, gdal.GDT_Float32)
    outDs1.SetGeoTransform(inDs.GetGeoTransform())
    outDs1.SetProjection(inDs.GetProjection())
    # print outDatas[90,270,i]
    outBand1 = outDs1.GetRasterBand(1)
    # outBand1.WriteArray(np.amax(blist, axis=0))  # get maximum
    outBand1.WriteArray(ndvi_max[:, :])
    outBand1.SetNoDataValue(-9999)
    outBand1 = None
    outDs1 = None

    outDs2 = driver.Create(r'G:\mcd43c4_product\ppi_max_loc_' + star  + '.tif', cols, rows, 1, gdal.GDT_Float32)
    outDs2.SetGeoTransform(inDs.GetGeoTransform())
    outDs2.SetProjection(inDs.GetProjection())
    # print outDatas[90,270,i]
    outBand2 = outDs2.GetRasterBand(1)
    outBand2.WriteArray(flag_max[:, :])  # get count
    outBand2.SetNoDataValue(-9999)
    outBand2 = None
    outDs2 = None

print 'ok'






