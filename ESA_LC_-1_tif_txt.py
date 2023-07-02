#!/usr/bin/env python
# -*- coding: utf-8 -*-
from osgeo import gdal
import numpy as np
import os, glob

raster = gdal.Open(r'D:\jag_modified\mc43_ppi_finland_10km_rasterio\finland_ESACCI-LC-300m-2002-2018-10km_mode.tif')
data = raster.GetRasterBand(1).ReadAsArray().astype('float')
data = data.ravel()
cv=np.transpose(data)
np.savetxt(r'D:\griddata_fi\new2018\txt\lc_mask_2002_2018.txt', cv, delimiter=',')
