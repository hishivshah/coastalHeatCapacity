import os
import datetime

import openpyxl
import psycopg2

# Input paths
projectDir = "D:\Projects\coastalHeatCapacity"
dataDir = os.path.join(projectDir, "data")
stationsXlsx = os.path.join(dataDir, "cefas", "CTN _ Wales_METADATA.xlsx")

# Connect to postgis database
connStr = "dbname=coastalHeat user=postgres password=ownwardenter"
with psycopg2.connect(connStr) as db:
    cur = db.cursor()

    # Create table
    cur.execute("DROP TABLE IF EXISTS stations;")
    cur.execute("""CREATE TABLE stations (
                       id INTEGER PRIMARY KEY,
                       name TEXT,
                       source TEXT,
                       startDate DATE,
                       endDate DATE,
                       interval TEXT,
                       status TEXT,
                       geometry GEOMETRY(POINT, 4326)
                   );""")

    # Read Excel worksheet
    wb = openpyxl.load_workbook(stationsXlsx)
    ws = wb["METADATA"]
    for row in ws.iter_rows("A4:G11"):
        id = row[0].value
        location = row[1].value
        source = row[2].value
        lat, lon = row[3].value.split(" ")
        if lat[-1] == "N":
            lat = float(lat[:-1])
        elif lat[-1] == "S":
            lat = float(lat[:-1]) * -1
        if lon[-1] == "E":
            lon = float(lon[:-1])
        elif lon[-1] == "W":
            lon = float(lon[:-1]) * -1
        start = row[4].value
        end = row[5].value
        if type(end) != datetime.datetime:
            end = None
        observations, status = row[6].value.split(" / ")

        # Insert data into postgis table
        cur.execute("""INSERT INTO stations VALUES (
                            %s, %s, %s, %s, %s, %s, %s,
                            ST_SetSRID(ST_Point(%s, %s), 4326)
                        );""",
                        (id, location, source, start, end, observations, status,
                         lon, lat))
