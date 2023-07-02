#!/usr/bin/env python
# -*- coding: utf-8 -*-
from osgeo import gdal
import numpy as np
import glob, os
os.environ['GDAL_DATA'] = r'C:\OSGeo4W64\share\gdal'

in_directory = r'G:\mcd43c4_product\fenno_nir'
files = glob.glob(os.path.join(in_directory, '*.tif'))
#Loop through and open all rasters and stack them into a 3d array

inDs=gdal.Open("G:/mcd43c4_product/fenno_nir/fenno_nir_MCD43C4.20020502.v006.hdf.tif")
gt=inDs.GetGeoTransform()
srs=inDs.GetProjection()

def writeFile(filename, geotransform, geoprojection, data):
    (rows, cols) = data.shape
    format = "GTiff"
    noDataValue = 1e+20  # numpy.ma.masked_outside, fill_value=1e+20
    # noDataValue = np.nan
    driver = gdal.GetDriverByName(format)
    # you can change the dataformat but be sure to be able to store negative values including -9999
    dst_datatype = gdal.GDT_Float32

    dst_ds = driver.Create(filename, cols, rows, 1, dst_datatype)
    dst_ds.SetGeoTransform(geotransform)
    dst_ds.SetProjection(geoprojection)
    dst_ds.GetRasterBand(1).WriteArray(data)
    dst_ds.GetRasterBand(1).SetNoDataValue(noDataValue)
    # return 1



for ras in files:
    ds=gdal.Open(ras)
    dat=ds.GetRasterBand(1).ReadAsArray()
    dat = dat / 10000.0
    dat=dat[None,:,:]               #turn 2d array into 3d

    try:stk=np.vstack((stk,dat)) #Do we already have a 3d stack?
    except NameError:stk=dat        #Nope, this is the first time through the loop

#Create masked array where valid values are >=0 and <=1
stk=np.ma.masked_outside(stk,1,0)

#Get max and min
max=stk.max(axis=0)
# min=stk.min(axis=0)
# OR use: numpy.nanmax(a, axis=None, out=None, keepdims=<no value>)[source]
#Write out to new rasters with gdal if you like...
# writeFile('G:/mcd43c4_product/max_red_fi_may_sep.tif', gt, srs, max)
writeFile('G:/mcd43c4_product/max_nir_fenno.tif', gt, srs, max)
outRaster = None




