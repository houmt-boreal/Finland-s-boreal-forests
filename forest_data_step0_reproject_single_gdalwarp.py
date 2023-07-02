#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, fnmatch
from osgeo import ogr
from osgeo import osr
from osgeo import gdal
os.environ['GDAL_DATA'] = r'C:\OSGeo4W64\share\gdal'



# inRaster = r'E:\canopy\canopy2013\latvuspeitto_vmi11_0913_R4_nan.tif'
# outRaster = r'E:\canopy\canopy2013\outout13_R4w.tif'

inRaster  = r"E:\ESA_LC\LC_fenno\use_paper\mask_used\fenno_ESACCI-LC-300m-2013-v2.0.7_epsg4008_mcd43_50percent.tif"
outRaster = r'E:\ESA_LC\LC_fenno\use_paper\mask_used\fenno_ESACCI-LC-300m-2013-v2.0.7_epsg3067_mcd43_50percent.tif'

# os.system("gdalwarp -tr 48 48 -r average " + inRaster + " " + outRaster)
os.system("gdalwarp  -s_srs EPSG:4008 -t_srs EPSG:3067 " + inRaster + " " + outRaster)

    # os.system("gdalwarp -s_srs E:/6974.prj -t_srs EPSG:3067 " + inRaster + " " + outRaster)
    # 6974.prj from https://spatialreference.org/ref/sr-org/6974/     prj.file
    # with -tr 10000 10000   -tr xres yres: set output file resolution (in target georeferenced units)

    # for both reprojection and resample
    #os.system("gdalwarp -tr 2.5 2.5 -r bilinear " + inRaster + " " + outRaster)

    # for both reprojection and resample
    #os.system("gdalwarp  -s_srs EPSG:4326 -t_srs EPSG:3067 -tr 10000 10000 -r bilinear " + inRaster + " " + outRaster)

print 'ok'