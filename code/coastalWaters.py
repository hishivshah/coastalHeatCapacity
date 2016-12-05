import os

import ogr
import psycopg2

# Input paths
projectDir = "D:\Projects\coastalHeatCapacity"
dataDir = os.path.join(projectDir, "data")
gmlPath = os.path.join(dataDir, "nrw",
                       "WaterFrameworkDirectiveCoastalWaterbodiesCycle2.gml")

# Connect to postgis database
connStr = "dbname=coastalheat user=postgres password=ownwardenter"
with psycopg2.connect(connStr) as db:
    cur = db.cursor()

    # Create table
    cur.execute("DROP TABLE IF EXISTS coastalWaters;")
    cur.execute("""CREATE TABLE coastalWaters (
                       wb_id TEXT PRIMARY KEY,
                       name TEXT,
                       geometry GEOMETRY(MULTIPOLYGON, 27700)
                    );""")

    # Read GML file
    dataSource = ogr.Open(gmlPath)
    layer = dataSource.GetLayer()
    layer.SetAttributeFilter("EA_REG_CD = 8")
    for feature in layer:
        wb_id = feature.GetField("EA_WB_ID")
        name = feature.GetField("NAME")
        geometry = feature.GetGeometryRef()
        wkt = geometry.ExportToWkt()

        # Insert into table
        cur.execute("""INSERT INTO coastalWaters
                       VALUES (%s, %s,
                               ST_Multi(ST_GeomFromText(%s, 27700)));""",
                    (wb_id, name, wkt))
