import os

import openpyxl
import psycopg2

# Input paths
projectDir = "D:\Projects\coastalHeatCapacity"
dataDir = os.path.join(projectDir, "data")
moelfreXlsx = os.path.join(dataDir, "cefas",
                           "CefasTempNetwork_MOELFRE_1966-2007.xlsx")
id = 36

# Connect to postgis database
connStr = "dbname=coastalHeat user=postgres password=ownwardenter"
with psycopg2.connect(connStr) as db:
    cur = db.cursor()

    # Create table
    cur.execute("""CREATE TABLE moelfre (
                       lsn INTEGER PRIMARY KEY,
                       dateCollected TIMESTAMP,
                       temperature NUMERIC
                   );""")

    # Read Excel data
    wb = openpyxl.load_workbook(moelfreXlsx, data_only=True)
    ws = wb["MOELFRE"]
    for row in ws.iter_rows("A2:AL3701"):
        lsn = row[0].value
        date = row[1].value
        temperature = row[33].value

        # Insert data into postgis table
        cur.execute("INSERT INTO moelfre VALUES (%s, %s, %s);",
                    (lsn, date, temperature))

    # Calculate monthly means, insert into temperature table
    cur.execute("DELETE FROM temperature WHERE stationId = %s;", (id,))
    cur.execute("""INSERT INTO temperature
                   SELECT
                       %s AS stationId,
                       EXTRACT(YEAR FROM datecollected) AS year,
                       EXTRACT(MONTH FROM datecollected) AS month,
                       AVG(temperature) AS temperature
                   FROM moelfre
                   GROUP BY 1,2,3
                   ORDER BY 2,3;""",
                (id,))

    # Drop table moelfre
    cur.execute("DROP TABLE moelfre;")
