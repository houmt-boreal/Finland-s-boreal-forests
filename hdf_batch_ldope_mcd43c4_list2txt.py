#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, fnmatch
from osgeo import gdal
# CLIP= 'D:\\cru4.0\\fin_rect.shp'
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# http://www.gdal.org/gdalwarp.html
# https://gis.stackexchange.com/questions/155396/using-gdalwarp-to-change-resolution-of-file-in-degrees-to-metres
# https://gxnotes.com/article/19136.html
# https://gis.stackexchange.com/questions/198289/does-gohlke-gdal-break-command-line-gdal-ogr-in-windoiws
# Copying the DLL out of \plugins and into \osgeo (leaving GDAL_DRIVER_PATH at C:\Python27\Lib\site-packages\osgeo\gdalplugins) worked.

import os, fnmatch
from osgeo import gdal
os.environ['GDAL_DATA'] = r'C:\OSGeo4W64\share\gdal'

# INPUT_FOLDER= 'D:\\GIMMS3g_v1\\season_NE\\son'
# OUTPUT_FOLDER= 'D:\\GIMMS3g_v1\\season_NE\\son_3067'

# gdal_dataset = gdal.Open ("E:/MOD13Q1/MOD13Q1.A2019273.h19v02.006.2019290002820.hdf")
#
# print gdal_dataset.GetSubDatasets()[0]


# INPUT_FOLDER= 'D:\\cru4.0\\pet_fin'
# OUTPUT_FOLDER= 'D:\\cru4.0\\pet_fin_3067_10km'
INPUT_FOLDER= 'H:/mcd43c4'
OUTPUT_FOLDER1= 'G:/mcd43c4_product/no'
OUTPUT_FOLDER2= 'G:/mcd43c4_product/zenith_2016_2018'

# hdf_ds = gdal.Open(r'E:\h2304\old1\MYD13C1.A2002217.006.2015150124020.hdf', gdal.GA_ReadOnly)
# ndvi=hdf_ds.GetSubDatasets()[0][0]
# ndvi_value= ndvi[len(ndvi) - 25:len(ndvi) - 0]
# ndvi_qc=hdf_ds.GetSubDatasets()[2][0]
# ndvi_qual=ndvi_qc[len(ndvi_qc) - 31:len(ndvi_qc) - 0]

def findRasters (path, filter):
    for root, dirs, files in os.walk(path):
        for file in fnmatch.filter(files, filter):
            yield file
dirlist=[]
for raster in findRasters(INPUT_FOLDER, '*.hdf'):
    #inRaster = '"' + INPUT_FOLDER + '/' + raster + '"'
    inRaster = INPUT_FOLDER + '/' + raster
    outRaster1 = OUTPUT_FOLDER1 + '/no_' + raster +'.hdf'
    outRaster2 = OUTPUT_FOLDER2 + '/nir_' + raster + '.tif'
    # without -tr 10000 10000, just for reprojection
    # os.system("gdalwarp  -s_srs EPSG:4326 -t_srs EPSG:3067 "+ inRaster + " " +  outRaster)

    # with -tr 10000 10000   -tr xres yres: set output file resolution (in target georeferenced units)
    #os.system("gdal_translate -of GTiff -a_srs EPSG:3067 " + inRaster + " -sds " + outRaster)
    # cwd: E:\h2304\h2404> gdalinfo MYD13Q1.A2003233.h24v04.006.2015153114759.hdf   得到每层的名字信息，如SUBDATASET_1_NAME=HDF4_EOS:EOS_GRID:"MYD13Q1.A2003233.h24v04.006.2015153114759.hdf":MODIS_Grid_16DAY_250m_500m_VI:250m 16 days NDVI
    # 这个方法在csd里可以，在这不行 cwd: gdal_translate -of GTiff 'HDF4_EOS:EOS_GRID:"E:/h2304/old1/MYD13Q1.A2004217.h23v04.006.2015154162703.hdf":MODIS_Grid_16DAY_250m_500m_VI:250m 16 days NDVI' v2.tif
    # gdal_translate -of GTiff 'HDF4_EOS:EOS_GRID:"MYD13Q1.A2003233.h24v04.006.2015153114759.hdf":MODIS_Grid_16DAY_250m_500m_VI:250m 16 days NDVI' v.tif

    #print "gdal_translate -of GTiff -projwin_srs E:/6974.prj " + "'HDF4_EOS:EOS_GRID:" + inRaster + ":MODIS_Grid_16DAY_250m_500m_VI:250m 16 days NDVI'"+ ' -sds ' + " " + outRaster
   # os.system("gdal_translate -of GTiff -projwin_srs E:/6974.prj " + "'HDF4_EOS:EOS_GRID:" + inRaster + ":MODIS_Grid_16DAY_250m_500m_VI:250m 16 days NDVI'"+ ' -sds ' + " " + outRaster)

    # os.system("gdal_translate -of GTiff -projwin 670000 7835000 1820000 6610000 -projwin_srs E:/6974.prj "  + inRaster +' -sds ' +" " +outRaster )
    # os.system("gdal_translate -of GTiff -projwin 670000 7835000 1820000 6610000 "  + inRaster +' -sds ' +" " +outRaster )
    # os.system("gdal_translate -of GTiff -projwin_srs E:/6974.prj " +  inRaster + ' -sds ' + " " + outRaster)   # for MODIS

    #cdc="mask_sds -of="+outRaster1+ " " + "-fill=-2 -sds=Nadir_Reflectance_Band1 -mask="+ inRaster +",BRDF_Quality,==0,OR,*,BRDF_Quality,==1,OR,*,BRDF_Quality,==2,AND,*,Percent_Snow,==0 -meta "+inRaster
    #dirlist.append(cdc)

    # for NIR
    # os.system("mask_sds -of="+outRaster1+ " " + "-fill=-2 -sds=Nadir_Reflectance_Band2 -mask="+ inRaster +",BRDF_Quality,==0,OR,*,BRDF_Quality,==1,OR,*,BRDF_Quality,==2,AND,*,Percent_Snow,==0 -meta "+inRaster)
    # for solar zenith
    os.system("mask_sds -of=" + outRaster1 + " " + "-fill=255 -sds=Local_Solar_Noon -mask=" + inRaster + ",BRDF_Quality,==0,OR,*,BRDF_Quality,==1,OR,*,BRDF_Quality,==2,AND,*,Percent_Snow,==0 -meta " + inRaster)

    os.system("gdal_translate -of GTiff -a_ullr -180 90 180 -90 -a_srs EPSG:4008 " + outRaster1 + ' -sds ' + " " + outRaster2)


    outRaster1 = None
    outRaster2 = None
print 'ok'




