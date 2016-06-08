import os

import openpyxl
import psycopg2

# Input paths
projectDir = "D:\Projects\coastalHeatCapacity"
dataDir = os.path.join(projectDir, "data")
xlsxDir = os.path.join(dataDir, "cefas")

# Lookup table identfying where data for each station is located
# (id, filename, worksheet, cell range)
lookup = [(30, "CefasTempNetwork__BARRY_1978-1999.xlsx", "Monthly Means", "A3:M24"),
          (31, "CefasTempNetwork_SWANSEA_1976-2000.xlsx", "Monthly Means", "A3:M27"),
          (32, "CefasTempNetwork_ANGLE_1990-2007.xlsx", "Monthly Mean", "A2:M19"),
          (33, "CefasTempNetwork_SKOMER_1985-2015.xlsx", "Monthly Means", "A5:M35"),
          (34, "CefasTempNetwork_WYLFA_1967-2007.xlsx", "Monthly Means", "A3:M43"),
          (35, "CefasTempNetwork_AMLWCH_1964-2003.xlsx", "Monthly Means", "A3:M42"),
          (37, "CefasTempNetwork_BANGOR_2010-2015.xlsx", "ALL DATA", "A5:M10")]

# Connect to postgis database
connStr = "dbname=coastalHeat user=postgres password=ownwardenter"
with psycopg2.connect(connStr) as db:
    cur = db.cursor()

    # Create table
    cur.execute("DROP TABLE IF EXISTS temperature;")
    cur.execute("""CREATE TABLE temperature (
                       stationId INTEGER REFERENCES stations(id),
                       year INTEGER,
                       month INTEGER,
                       temperature NUMERIC,
                       PRIMARY KEY (stationId, year, month)
                   );""")

    # Read data from Excel workbooks
    for a in lookup:
        id = a[0]
        wb = openpyxl.load_workbook(os.path.join(xlsxDir, a[1]), data_only=True)
        ws = wb[a[2]]
        for row in ws.iter_rows(a[3]):
            year = row[0].value
            month = 0
            for cell in row[1:]:
                month += 1
                temperature = cell.value
                if type(temperature) == unicode:
                    temperature = float(temperature)

                # Insert into postgis table
                cur.execute("INSERT INTO temperature VALUES (%s, %s, %s, %s);",
                            (id, year, month, temperature))
