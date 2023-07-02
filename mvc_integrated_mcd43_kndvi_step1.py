#!/usr/bin/env python
# -*- coding: utf-8 -*-

from osgeo import gdal
import numpy as np
import glob
import os


rows = 400
cols = 790

in_directory = r'E:\mcd43c4_product\ppi_monthly_max'
files = glob.glob(os.path.join(in_directory, '*.tif'))

inDs = gdal.Open(r"E:\mcd43c4_product\ppi_monthly_max\ppi.max.200608.tif")
driver = inDs.GetDriver()

# for filea in files:
#     filea ="D:\\GIMMS3g_v1\\NDVI_raw_tif\\ndvi3g_v1_1982_011.tif"
#     print filea[len(filea) - 12:len(filea) - 8]
#     print filea[len(filea) - 7:len(filea) - 5]

for m in range(1,2):
    mm=2012+m
    dd=str(mm)
    print (dd)
    blist = []
    for filea in files:
        if filea[len(filea) - 10:len(filea) - 6] == dd:
            # print filea
            ds = gdal.Open(filea, gdal.GA_ReadOnly)
            ary = ds.GetRasterBand(1).ReadAsArray()
            ss = ary[:, :]
            # ss[ss<0]=np.nan
            # ss[ss>100]=np.nan
            blist.append(ss)
    myarray = np.asarray(blist)
    # print blist
    # print np.amax(blist, axis=0)# https://docs.scipy.org/doc/numpy/reference/generated/numpy.amax.html
    outDs1 = driver.Create(r'E:\mcd43c4_product\ppi_ti_max\ppi_max_Mar_Sep' + dd + '.tif', cols, rows, 1, gdal.GDT_Float32)
    outDs1.SetGeoTransform(inDs.GetGeoTransform())
    outDs1.SetProjection(inDs.GetProjection())
    # print outDatas[90,270,i]
    outBand1 = outDs1.GetRasterBand(1)
    outBand1.WriteArray(np.amax(myarray, axis=0))  # get max
    # outBand1.WriteArray(np.sum(myarray, axis=0))  # get sum, nan means nan
    # outBand1.SetNoDataValue(-9999)
    outBand1 = None
    outDs1 = None

print ('ok')





