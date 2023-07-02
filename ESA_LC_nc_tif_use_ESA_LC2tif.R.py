#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import rioxarray   # for py3
import xarray

xds = xarray.open_dataset('E:\ESA_LC\LC\C3S-LC-L4-LCCS-Map-300m-P1Y-2018-v2.1.1.nc')
xds.rio.set_crs("epsg:4326")
xds["lccs_class"].rio.to_raster(r'D:\testlv.tif')



