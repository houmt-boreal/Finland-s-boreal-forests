# -*- coding: utf-8 -*-

from osgeo import gdal, gdal_array
import numpy as np
import os, fnmatch,glob


firstrun = 1


def readFile(filename):
    filehandle = gdal.Open(filename)
    band1 = filehandle.GetRasterBand(1)
    geotransform = filehandle.GetGeoTransform()
    geoproj = filehandle.GetProjection()
    Z = band1.ReadAsArray()
    xsize = filehandle.RasterXSize
    ysize = filehandle.RasterYSize
    return xsize,ysize,geotransform,geoproj,Z

def writeFile(filename,geotransform,geoprojection,data):
    (x,y) = data.shape
    format = "GTiff"
    driver = gdal.GetDriverByName(format)
    # you can change the dataformat but be sure to be able to store negative values including -9999
    dst_datatype = gdal.GDT_Float32
    dst_ds = driver.Create(filename,y,x,1,dst_datatype)
    dst_ds.GetRasterBand(1).WriteArray(data)
    dst_ds.SetGeoTransform(geotransform)
    dst_ds.SetProjection(geoprojection)
    dst_ds.GetRasterBand(1).SetNoDataValue(-9999)
    return 1



in_directory = r'G:\mcd43c4_product\ppi_monthly_mean_summer_months'
files = glob.glob(os.path.join(in_directory, '*.tif'))

# OUTPUT_FOLDER= r'E:\canopy\growing_stock2013\2013_two_values'
OUTPUT_FOLDER= r'G:\mcd43c4_product\ppi_monthly_mean_summer_months_nan_-9999_for_june'

for inRaster in files:

    outRaster = OUTPUT_FOLDER + '/' + inRaster[len(inRaster) - 19:len(inRaster) - 0]
    # outRaster = OUTPUT_FOLDER + '/two_values' + inRaster[len(inRaster) - 7:len(inRaster) - 0]


    if firstrun == 1 :
        [xsize,ysize,geotransform,geoproj,Z] = readFile(inRaster)


    # Set large negative values to -9999
    # Z=Z/1.0
    # Z[Z>32700]= -9999

    # Z[Z>100]= np.nan # suit for array, not for list
    # Z[Z < 0] = np.nan
    # Or
    # Z = np.where(((Z < 32700) & (Z >= 0)), Z, -9999)  # suit for array, not for list
    # Z = np.where(((Z < 32700) & (Z >= 0)), -1,1)  # two values for easily count

    # Choose your preference: (comment either rule)
    # Z[Z==-9999]= np.nan
    # Or
    Z[np.isnan(Z)]= -9999
    Z[Z < 0] = -9999 # for PPI <0



    writeFile(outRaster,geotransform,geoproj,Z)
    inRaster=None
    outRaster=None

    # Open your file in QGIS and set Nodata value if necessary for colormaps etc.
print 'ok'






