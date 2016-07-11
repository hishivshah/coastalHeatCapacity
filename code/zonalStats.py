"""Run this script within the QGIS Python console."""
from qgis.analysis import QgsZonalStatistics

# Add polygon layer
uri = QgsDataSourceURI()
uri.setConnection("localhost", "5432", "coastalHeat", "postgres",
                  "ownwardenter")
uri.setDataSource("public", "coastalwaters", "geometry")
zones = QgsVectorLayer(uri.uri(), "coastalwaters", "postgres")

# Raster layer
connStr = "PG: dbname=coastalHeat user=postgres password=ownwardenter mode=2 schema=public column=rast table=sst"

# Calculate zonal statistics
zonalStats = QgsZonalStatistics(zones, connStr, "", 1, QgsZonalStatistics.Mean)
zonalStats.calculateStatistics(None)
