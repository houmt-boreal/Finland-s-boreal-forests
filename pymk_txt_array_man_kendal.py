#!/usr/bin/env python
# -*- coding: utf-8 -*-

from osgeo import gdal
import numpy as np
import pymannkendall as mk
import glob, os


rows = 260
cols = 260

p_value1= np.empty([rows, cols])
# tau1= np.empty([rows, cols])
slope1= np.empty([rows, cols])

in_directory = r'D:\SIF_data\gosif\data.globalecology.unh.edu\data\GOSIF_v2\Monthly\hulun_sep'
files = glob.glob(os.path.join(in_directory, '*.tif'))

inDs = gdal.Open(r"D:\SIF_data\gosif\data.globalecology.unh.edu\data\GOSIF_v2\Monthly\hulun\hulun_gosif_2017.M08.tif")
driver = inDs.GetDriver()

alist=[]
for filea in files:
    print filea
    ds = gdal.Open(filea, gdal.GA_ReadOnly)
    ary = ds.GetRasterBand(1).ReadAsArray()
    ss = ary[:, :]
    alist.append(ss)

myarray = np.asarray(alist)
print myarray.shape

# blist=[]
# txt_directory = r'E:\zhu\mon_1982-2015'
# files_txt = glob.glob(os.path.join(txt_directory, '*.txt'))
# for filetxt in files_txt:
#   clim = np.loadtxt(filetxt)
#   blist.append(clim)
# myarray = np.asarray(blist)


for col in xrange(cols):
    # print col
    for row in xrange(rows):
        cvv=myarray[:, row, col]/10000.0
        # for NDVI
        # if any(((ii <= 0) or (np.isnan(ii))) for ii in cvv):  # for maxNDVI<=0
        # for gosif
        if any(((ii <= 0) or (ii >= 3.276) or (np.isnan(ii))) for ii in cvv):  # for maxNDVI<=0
        # if all(ii <= -700000 for ii in cvv):  # for tiNDVI<=0
        #     tau1[row, col] = 1111111    # depeding on MAX value among all pixels, for maxNDVI,999;  for tinavi, 1111111
            p_value1[row, col] = np.nan
            slope1[row, col] = np.nan
        else:
            trend, h, p_value, z, tau, s, var_s, slope = mk.original_test(cvv)
            # slope2 = mk.seasonal_sens_slope(cvv, period=12) # is same with slope from correlated_seasonal_test
            #alist.append(tau)
            # tau1[row, col] = tau
            p_value1[row, col] = p_value
            slope1[row, col] = slope

# outDs1 = driver.Create('D:\\bimonth\\mon25_seasonal_slope2_' + 'mk' + '.tif', cols, rows, 1, gdal.GDT_Float32)
# outDs1.SetGeoTransform(inDs.GetGeoTransform())
# outDs1.SetProjection(inDs.GetProjection())
# # print outDatas[90,270,i]
# outBand1 = outDs1.GetRasterBand(1)
# outBand1.WriteArray(tau1[:, :])  # get count
# outBand1.SetNoDataValue(1111111)
# outBand1 = None
# outDs1 = None

outDs2 = driver.Create(r'D:\mcd13c2_hulun1\gosif_2003_2018_sep_pvalue_' + 'mk' + '.tif', cols, rows, 1, gdal.GDT_Float32)
outDs2.SetGeoTransform(inDs.GetGeoTransform())
outDs2.SetProjection(inDs.GetProjection())
# print outDatas[90,270,i]
outBand2 = outDs2.GetRasterBand(1)
outBand2.WriteArray(p_value1[:, :])  # get count
# outBand2.SetNoDataValue(1111111)
outBand2 = None
outDs2 = None

outDs3 = driver.Create(r'D:\mcd13c2_hulun1\gosif_2003_2018_sep_slope_' + 'mk' + '.tif', cols, rows, 1, gdal.GDT_Float32)
outDs3.SetGeoTransform(inDs.GetGeoTransform())
outDs3.SetProjection(inDs.GetProjection())
# print outDatas[90,270,i]
outBand3 = outDs3.GetRasterBand(1)
outBand3.WriteArray(slope1[:, :])
# outBand1.SetNoDataValue(-9999)
# outBand3.SetNoDataValue(1111111)
outBand3 = None
outDs3 = None

print 'ok'








