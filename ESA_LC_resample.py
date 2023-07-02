#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, glob
from osgeo import ogr
from osgeo import osr
from osgeo import gdal
os.environ['GDAL_DATA'] = r'C:\OSGeo4W64\share\gdal'
inRaster= r"E:\ESA_LC\LC_fenno\fenno_ESACCI-LC-300m-2002-2018-v2.0.7_twovalues.tif"
outRaster= r"E:\ESA_LC\LC_fenno\fenno_ESACCI-LC-300m-2002-2018-10km_mode.tif"



# ras = gdal.Open(r"G:\mcd43c4_product\fenno_red_2016\fenno_red_MCD43C4.20160501.v006.hdf.tif")
ras = gdal.Open(r"D:\griddata_fi\new2018\Daily global radiation_TIFF\GlobalRad_10km_1961_2018_geotif\globrad_2016.tif")
gt =ras.GetGeoTransform()
pixelSizeX = gt[1]
pixelSizeY = -gt[5]


# os.system("gdalwarp -tr "+str(pixelSizeX)+" "+str(pixelSizeY)+" -r average " + inRaster + " " + outRaster)
os.system("gdalwarp -s_srs EPSG:4326 -t_srs EPSG:3067 -tr "+str(pixelSizeX)+" "+str(pixelSizeY)+" -r mode " + inRaster + " " + outRaster)
# -r mode: selects the value which appears most often of all the sampled points. just means >50%
inRaster=None
outRaster=None

print 'ok'