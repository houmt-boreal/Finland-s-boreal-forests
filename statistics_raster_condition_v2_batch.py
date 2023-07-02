#!/usr/bin/env python
# -*- coding: utf-8 -*-
from osgeo import gdal, gdal_array
import numpy as np
import os, glob
import pandas as pd
from xlrd import open_workbook
from pandas import DataFrame
# for ext in s:
#     # Get file names
lc1 = r"D:\jag_modified\lc_10km\a_-2018-10km_mode.tif"
# lc2 = r"D:\jag_modified\lc_10km\mb_-2018-10km_mode.tif"
# lc3 = r"D:\jag_modified\lc_10km\sb_-2018-10km_mode.tif"
ds = gdal.Open(lc1)
b1 = ds.GetRasterBand(1)
arr = b1.ReadAsArray()

# ds2 = gdal.Open(lc2)
# b2 = ds2.GetRasterBand(1)
# arr2 = b2.ReadAsArray()
#
# ds3 = gdal.Open(lc3)
# b3 = ds3.GetRasterBand(1)
# arr3 = b3.ReadAsArray()


# np.count_nonzero(arr < 0)   #Counts the number of non-zero values in the array , https://note.nkmk.me/en/python-numpy-count/
# # np.count_nonzero(np.isnan(myarray))
# # np.count_nonzero(myarray < 3000, axis=0)
# np.sum(arr==-1) # 808  # = np.count_nonzero(arr < 0)
# data=None

in_directory1 = r'D:\jag_modified\spei_a'
files1 = glob.glob(os.path.join(in_directory1, '*.tif'))
alist=[]
for filea in files1:
    # Open band 1 as array
    ds_a = gdal.Open(filea)
    b_a = ds_a.GetRasterBand(1)
    arr_a = b_a.ReadAsArray()

    data=np.where(((arr == -1) & (arr_a >= -100)& (arr_a <= 100)), arr_a, np.nan)
    data = np.nanmean(data)
    alist.append(data)
#
df = DataFrame({'spei': alist})
df.to_excel(r'D:\jag_modified\spei_a_2002_2018.xlsx', sheet_name='sheet1', index=False)


print 'ok'


