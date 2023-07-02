#!/usr/bin/env python
# -*- coding: utf-8 -*-
from osgeo import gdal, gdal_array
import numpy as np
import glob, os

in_directory = r'G:\mcd43c4_product\fenno_red_2016_2018\gs'
files = glob.glob(os.path.join(in_directory, '*.tif'))


blist=[]
for ras in files:
    ds = gdal.Open(ras, gdal.GA_ReadOnly)
    dat = ds.GetRasterBand(1).ReadAsArray()
    dat = dat / 10000.0
    dat = np.where(((dat <= 1) & (dat >= 0)), dat, np.nan)
    blist.append(dat)

arry = np.asarray(blist)

min=np.nanmin(arry, axis=0)
# np.nanmin(arry)  # one value
output='G:/mcd43c4_product/min_red_fenno20162018.tif'
gdal_array.SaveArray(min.astype("float32"), output, "GTIFF", ds)

ds=None
arry=None




