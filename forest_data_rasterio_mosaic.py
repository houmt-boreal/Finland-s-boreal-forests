#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rasterio
from rasterio.merge import merge
from rasterio.plot import show
import glob, os

dirpath = r"E:\canopy\growing_stock2013\2013_gimms_scale"
# dirpath = r"E:\canopy\growing_stock2013\2013_mcd43_scale"

# src = rasterio.open(r"E:\canopy\canopy2013\2013_gimms_scale\gimms_average_9999_T4.tif")
# src.crs  # CRS({'init': u'epsg:3067'})

out_fp = r"E:\canopy\growing_stock2013\growing_stock2013_gimms_Mosaic_all.tif"
# out_fp = r"E:\canopy\growing_stock2013\growing_stock2013_mcd43_Mosaic_all.tif"
# out_fp = r"E:\canopy\growing_stock2013\growing_stock2013_gimms_Mosaic_all.tif"


dem_fps = glob.glob(os.path.join(dirpath, "*.tif"))

src_files_to_mosaic = []
for fp in dem_fps:
    src = rasterio.open(fp)
    src_files_to_mosaic.append(src)

mosaic, out_trans = merge(src_files_to_mosaic)

out_meta = src.meta.copy()

out_meta.update({"driver": "GTiff",
        "height": mosaic.shape[1],
        "width": mosaic.shape[2],
        "transform": out_trans,
        "crs": "+proj=utm +zone=35 +ellps=GRS80 +units=m +no_defs "})   # proj4 string can get from run 'gdalsrsinfo epsg:3067' in windows shell

with rasterio.open(out_fp, "w", **out_meta) as dest:
     dest.write(mosaic)

out_fp=None
mosaic=None

