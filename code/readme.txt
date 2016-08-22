readSST.ps1
- Windows PowerShell script to read SST data into PostGIS
- Calls gdal_translate to convert HDF5 file to  temporary TIFF file
- Calls gdalwarp to transform and clip to British National Grid
- Calls raster2pgsql to load raster into PostGIS

coastalWaters.py
- Reads NRW Coastal Waterbody polygons from gml
- Loads into PostGIS

zonalStats.py
- calculates mean SST for each Coastal Waterbody using QGIS Zonal statistics
- script must be run within QGIS Python console

calcHeat.py
- calculates heat capacity of coastal waters
