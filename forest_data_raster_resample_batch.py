#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, glob
from osgeo import ogr
from osgeo import osr
from osgeo import gdal
os.environ['GDAL_DATA'] = r'C:\OSGeo4W64\share\gdal'
# INPUT_FOLDER= 'D:\\GIMMS3g_v1\\season_NE\\son'
# OUTPUT_FOLDER= 'D:\\GIMMS3g_v1\\season_NE\\son_3067'


OUTPUT_FOLDER= r'E:\canopy\growing_stock2013\2013_gimms_scale'
# OUTPUT_FOLDER= r'E:\canopy\growing_stock2013\2013_mcd43_scale'

in_directory = r'E:\canopy\growing_stock2013\2013_nan'
# in_directory = r'E:\canopy\growing_stock2013\2013_two_values'

files = glob.glob(os.path.join(in_directory, '*.tif'))

ras = gdal.Open(r"E:\canopy\basal_area2013\gimms_reso_meter.tif")
# ras = gdal.Open(r'E:\canopy\basal_area2013\mcd43_reso_meter.tif')
gt =ras.GetGeoTransform()
pixelSizeX = gt[1]
pixelSizeY = -gt[5]




for inRaster in files:

    outRaster = OUTPUT_FOLDER + '/mcd43_average_9999' + inRaster[len(inRaster) - 7:len(inRaster) - 0]
    # outRaster = OUTPUT_FOLDER + '/gimms_average_9999' + inRaster[len(inRaster) - 7:len(inRaster) - 0]
    # for two values
    # os.system("gdalwarp -tr " + str(pixelSizeX) + " " + str(pixelSizeY) + " -r average " + inRaster + " " + outRaster)

    # for -9999 nodata，已经预先定义了nodata为-9999
    os.system("gdalwarp -tr "+str(pixelSizeX)+" "+str(pixelSizeY)+" -srcnodata -9999 -r average " + inRaster + " " + outRaster)
    # 等于 os.system("gdalwarp -tr " + str(pixelSizeX) + " " + str(pixelSizeY) + " -r average " + inRaster + " " + outRaster)

    # average: computes the weighted average of all non-NODATA contributing pixels. 注意:np.nan不被认为是nodata，但待采样的栅格中，有一个nan值，重采样的栅格将全部为nan
    # 因为np.nan正常参与计算，不被认为是nodata，只是存在np.nan的格点一般无论怎么计算，结果都是np.nan


    # only define projection
    # os.system("gdalwarp -t_srs EPSG:3067 " + inRaster + " " + outRaster)

    # os.system("gdalwarp -s_srs E:/6974.prj -t_srs EPSG:3067 " + inRaster + " " + outRaster)
    # 6974.prj from https://spatialreference.org/ref/sr-org/6974/     prj.file
    # with -tr 10000 10000   -tr xres yres: set output file resolution (in target georeferenced units)

    # for both reprojection and resample
    #os.system("gdalwarp -tr 2.5 2.5 -r bilinear " + inRaster + " " + outRaster)

    # for both reprojection and resample
    #os.system("gdalwarp  -s_srs EPSG:4326 -t_srs EPSG:3067 -tr 10000 10000 -r bilinear " + inRaster + " " + outRaster)
    inRaster=None
    outRaster=None

print 'ok'