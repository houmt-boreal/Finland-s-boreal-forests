#!/usr/bin/env python
# -*- coding: utf-8 -*-
from osgeo import gdal, gdal_array
import numpy as np
# for ext in s:
#     # Get file names
nirmax = r"E:\ESA_LC\LC_fenno\fenno_ESACCI-LC-L4-LCCS-Map-300m-P1Y-2002-v2.0.7.tif"
redmin = r"E:\ESA_LC\LC_fenno\fenno_ESACCI-LC-L4-LCCS-Map-300m-2018.tif"
output = r"E:\ESA_LC\LC_fenno\fenno_ESACCI-LC-300m-2002-2018-v2.0.7_twovalues.tif"

# nirmax = r"E:\ESA_LC\LC_fenno\fenno_ESACCI-LC-L4-LCCS-Map-300m-P1Y-2013-v2.0.7.tif"
# output = r"E:\ESA_LC\LC_fenno\fenno_ESACCI-LC-300m-2013-v2.0.7.tif"

# Open band 1 as array
ds = gdal.Open(nirmax)
b1 = ds.GetRasterBand(1)
arr = b1.ReadAsArray()
arr=arr/1.0

ds2 = gdal.Open(redmin)
b2 = ds2.GetRasterBand(1)
arr2 = b2.ReadAsArray()
arr2=arr2/1.0


arr=np.where(((arr <= 90) & (arr >= 50)), -1, 1)
arr2=np.where(((arr2 <= 90) & (arr2 >= 50)), -1,1)
data = np.where(((arr == -1) & (arr2 == -1)), -1,1)

# data = np.where(((arr <= 90) & (arr >= 50)), -1,1)

gdal_array.SaveArray(data.astype("float32"), output, "GTIFF", ds)
ds = None
# ds2 = None





