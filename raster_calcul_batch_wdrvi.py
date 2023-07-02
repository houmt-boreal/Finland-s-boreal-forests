#!/usr/bin/env python
# -*- coding: utf-8 -*-
from osgeo import gdal, gdal_array
import numpy as np
import glob,os

inDs = r'D:\GIMMS3g_v1\Fenno_ndvi_mean_month_del_flag3\2013new'
files = glob.glob(os.path.join(inDs, '*.tif'))
# fiela=files[0]
# filea[len(filea) - 21:len(filea) - 8]

OUTPUT_FOLDER= r'D:\GIMMS3g_v1\Fenno_ndvi_mean_month_del_flag3\wdrvi'
# https://stackoverflow.com/questions/28239439/two-loops-together-in-python
for filea in files:
    outRaster = OUTPUT_FOLDER + '/wdrvi.' + filea[len(filea) - 11:len(filea) - 0]

    # Open band 1 as array
    ds_a = gdal.Open(filea)
    b_a = ds_a.GetRasterBand(1)
    arr_a = b_a.ReadAsArray()
    data = np.where((arr_a > 0)&(arr_a <= 1), arr_a, np.nan)
    data = (1.2* data -0.8)/((-0.8)*data+1.2)

    # save array, using ds as a prototype
    gdal_array.SaveArray(data.astype("float32"), outRaster, "GTIFF", ds_a)
    ds_a = None





