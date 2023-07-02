#!/usr/bin/env python
# -*- coding: utf-8 -*-

from osgeo import gdal
import scipy
import numpy as np
from matplotlib import pyplot
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import pacf
from statsmodels.tsa.seasonal import seasonal_decompose
import glob
import os


rows = 138
cols = 168

p_value= np.empty([rows, cols])
rho= np.empty([rows, cols])


in_directory = r'D:\GIMMS3g_v1\Fenno_ndvi_mean_month_del_flag3\ndvi_fin'
files = glob.glob(os.path.join(in_directory, '*09.tif'))

inDs = gdal.Open(r'D:\GIMMS3g_v1\Fenno_ndvi_mean_month_del_flag3\ndvi_fin\ndvi_fin_2003_05.tif')
driver = inDs.GetDriver()

alist=[]
for filea in files:
    # print filea
    ds = gdal.Open(filea, gdal.GA_ReadOnly)
    ary = ds.GetRasterBand(1).ReadAsArray()
    ss = ary[:, :]
    alist.append(ss)
gimms = np.asarray(alist)

blist=[]
inDs2 = r'G:\mcd43c4_product\ppi_monthly_mean_epsg4326_fin'
files2 = glob.glob(os.path.join(inDs2, '*09.tif'))
for fileb in files2:
    ds2 = gdal.Open(fileb, gdal.GA_ReadOnly)
    ary2 = ds2.GetRasterBand(1).ReadAsArray()
    ss2 = ary2[:, :]
    blist.append(ss2)

mcd43 = np.asarray(blist)

for col in xrange(cols):
    # print col
    for row in xrange(rows):
        cvv=mcd43[:, row, col]
        cli=gimms[:, row, col]
        #if any( (np.isnan(ii)) for ii in cvv) or any(((iii <= 0) or (np.isnan(iii))) for iii in cli):  # for maxNDVI<=0
        if any( (ii < 0) or (np.isnan(ii)) for ii in cvv) or any((iii < 0) or (np.isnan(iii)) for iii in cli):  # for ppi<0 ,ndvi<0
        # if all(ii <= -700000 for ii in cvv):  # for tiNDVI<=0
            p_value[row, col] = np.nan
            rho[row, col] = np.nan
        else:
            # for z-score, month-based
            # for mm in xrange(12):
            #     cvv[slice(mm, 408, 12)] = scipy.stats.zscore(cvv[slice(mm, 408, 12)])   # total 408 months
            #     cli[slice(mm, 408, 12)] = scipy.stats.zscore(cli[slice(mm, 408, 12)])   # https://docs.python.org/2.3/whatsnew/section-slices.html

            # for Checks for Stationarity
            # res1 = adfuller(cvv)
            # res2 = adfuller(cli)
            # rho[row, col] = res1[1]  # p-value, p-value <= 0.05: is stationary.
            # p_value[row, col] = res2[1] # p-value


            # for raw series
            r = scipy.stats.spearmanr(cvv, cli)
            rho[row, col] = r[0]  # correlation coefficient
            p_value[row, col] = r[1]

            # for residu after remove seasonal and trend
            # https://www.cbcity.de/timeseries-decomposition-in-python-with-statsmodels-and-pandas
            # result_1 = seasonal_decompose(cvv, model='additive', freq=4)
            # result_2 = seasonal_decompose(cli, model='additive', freq=4)
            # cvv = result_1.resid
            # cvv = cvv[np.logical_not(np.isnan(cvv))]  #  drop na for array
            # cli= result_2.resid
            # cli = cli[np.logical_not(np.isnan(cli))]
            # r = scipy.stats.spearmanr(cvv, cli)
            # rho[row, col] = r[0]
            # p_value[row, col] = r[1]

            # for residu after numpy.diff
            # cvv = np.diff(cvv)
            # cli = np.diff(cli)
            # r = scipy.stats.spearmanr(cvv, cli)
            # rho[row, col] = r[0]
            # p_value[row, col] = r[1]


outDs1 = driver.Create(r'D:\jag_modified\spearman_sep_ppi_ndvi_corr.tif', cols, rows, 1, gdal.GDT_Float32)
outDs1.SetGeoTransform(inDs.GetGeoTransform())
outDs1.SetProjection(inDs.GetProjection())
# print outDatas[90,270,i]
outBand1 = outDs1.GetRasterBand(1)
outBand1.WriteArray(rho[:, :])  # get count
# outBand1.SetNoDataValue(11111)
outBand1 = None
outDs1 = None

outDs2 = driver.Create(r'D:\jag_modified\spearman_sep_ppi_ndvi_pvalue.tif', cols, rows, 1, gdal.GDT_Float32)
outDs2.SetGeoTransform(inDs.GetGeoTransform())
outDs2.SetProjection(inDs.GetProjection())
# print outDatas[90,270,i]
outBand2 = outDs2.GetRasterBand(1)
outBand2.WriteArray(p_value[:, :])  # get count
# outBand2.SetNoDataValue(11111)
outBand2 = None
outDs2 = None


print 'ok'








