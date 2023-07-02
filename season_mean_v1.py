#!/usr/bin/env python
# -*- coding: utf-8 -*-
from osgeo import gdal, gdal_array
import numpy as np
import glob,os

in_directory1 = r'G:\mcd43c4_product\ppi_monthly_mean\summer'
filesa = glob.glob(os.path.join(in_directory1, '*06.tif'))

in_directory2 = r'G:\mcd43c4_product\ppi_monthly_mean\summer'
filesb = glob.glob(os.path.join(in_directory2, '*07.tif'))

in_directory3 = r'G:\mcd43c4_product\ppi_monthly_mean\summer'
filesc = glob.glob(os.path.join(in_directory3, '*08.tif'))

OUTPUT_FOLDER= r'G:\mcd43c4_product\ppi_monthly_mean'

# https://stackoverflow.com/questions/28239439/two-loops-together-in-python
for filea,fileb,filec in zip(filesa,filesb,filesc):
    outRaster = OUTPUT_FOLDER + '/ppi.mean' + filea[len(filea) - 10:len(filea) - 6] + 'su.tif'

    # Open band 1 as array
    ds_a = gdal.Open(filea)
    b_a = ds_a.GetRasterBand(1)
    arr_a = b_a.ReadAsArray()

    ds_b = gdal.Open(fileb)
    b_b = ds_b.GetRasterBand(1)
    arr_b = b_b.ReadAsArray()

    ds_c = gdal.Open(filec)
    b_c = ds_c.GetRasterBand(1)
    arr_c = b_c.ReadAsArray()

    arr_a = np.where(((arr_a <= 100) & (arr_a >= 0)), arr_a, np.nan)
    arr_b = np.where(((arr_b <= 100) & (arr_b >= 0)), arr_b, np.nan)
    arr_c = np.where(((arr_c <= 100) & (arr_c >= 0)), arr_c, np.nan)

    data = (arr_a + arr_b + arr_c) / 3

    # save array, using ds as a prototype
    gdal_array.SaveArray(data.astype("float32"), outRaster, "GTIFF", ds_a)

    ds_a = None
    ds_b = None
    ds_c = None




