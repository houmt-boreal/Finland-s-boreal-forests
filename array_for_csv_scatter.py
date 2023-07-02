#!/usr/bin/env python
# -*- coding: utf-8 -*-
from osgeo import gdal, gdal_array
import numpy as np
import csv
import pandas as pd
from scipy import stats
# from itertools import izip

lc = r"E:\mcd43c4_product\old2002-2015\ppi.vs.forest\ppi.vs.forest_-LC-2013mod.tif"

# ti_vi = r"E:\mcd43c4_product\old2002-2015\ppi.vs.forest\ppi.vs.forest_ppi_ti_2013.tif"
# max_vi= r"E:\mcd43c4_product\old2002-2015\ppi.vs.forest\ppi.vs.forest_pi_max_2013.tif"

ti_vi = r"E:\mcd43c4_product\pksif_2013fin_for_scatter\ppi.vs.forest_ew_sum_apr_oct2013.tif"
max_vi= r"E:\mcd43c4_product\pksif_2013fin_for_scatter\ppi.vs.forest_ew_max_apr_oct2013.tif"

stock = r"E:\mcd43c4_product\old2002-2015\ppi.vs.forest\ppi.vs.forest_ngstock_all.tif"
canopy = r"E:\mcd43c4_product\old2002-2015\ppi.vs.forest\ppi.vs.forest__canopy_all.tif"
basal = r"E:\mcd43c4_product\old2002-2015\ppi.vs.forest\ppi.vs.forest_c_all_basal.tif"

# output = "G:/mcd43c4_product/nir_red_plus_minus_ratio.tif"

# Open band 1 as array
ds0 = gdal.Open(lc)
b0 = ds0.GetRasterBand(1)
arr0 = b0.ReadAsArray()

ds1 = gdal.Open(ti_vi)
b1 = ds1.GetRasterBand(1)
tivi = b1.ReadAsArray()

ds2 = gdal.Open(max_vi)
b2 = ds2.GetRasterBand(1)
maxvi = b2.ReadAsArray()


ds3 = gdal.Open(stock)
b3 = ds3.GetRasterBand(1)
stock_f = b3.ReadAsArray()

ds4 = gdal.Open(canopy)
b4 = ds4.GetRasterBand(1)
canopy_f = b4.ReadAsArray()

ds5 = gdal.Open(basal)
b5 = ds5.GetRasterBand(1)
basal_f = b5.ReadAsArray()

# a4=np.where(((arr0 == -1) & (arr2 > 0)& (arr2 < 1000)& (arr3 > -2)& (arr3 < 5)), arr3, -999)
# a5=np.where(((arr0 == -1) & (arr2 > 0)& (arr2 < 1000)& (arr3 > -2)& (arr3 < 5)), arr2, -999)
a1=np.where(((arr0 == -1) & (tivi > 0)& (tivi < 1000)), tivi, -999)
a2=np.where(((arr0 == -1) & (maxvi > 0)& (maxvi < 1000)), maxvi, -999)
a3=np.where(((arr0 == -1) & (stock_f > 0)& (stock_f < 1000)), stock_f,-999)
a4=np.where(((arr0 == -1) & (canopy_f > 0)& (canopy_f < 1000)), canopy_f,-999)
a5=np.where(((arr0 == -1) & (basal_f> 0)& (basal_f < 1000)), basal_f, -999)




df_from_arr = pd.DataFrame(data=[a1.ravel(), a2.ravel(), a3.ravel(), a4.ravel(), a5.ravel()])
df_from_arr = df_from_arr.T

df_from_arr = df_from_arr[~df_from_arr.eq(-999).any(1)]
df_from_arr.columns =['ti_ppi', 'max_ppi', 'stock', 'canopy', 'basal']
df_from_arr.to_excel(r'D:\r_script_me\scatter_ppi_inventory\pksif_apr_oct_forest.xlsx', sheet_name='sheet1', index=False)




