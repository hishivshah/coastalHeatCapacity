import psycopg2

# Constants
rho = 1027 # density of sea water (kg/m^3)
C_p = 4180 # specific heat of water (J/kg/K)
unitConv = 10**-6 # unit conversion from Watts to Mega Watts
# Multiply constants
const = rho * C_p * unitConv

# Connect to postgis database
connStr = "dbname=coastalHeat user=postgres password=ownwardenter"
with psycopg2.connect(connStr) as db:
    cur = db.cursor()

    # Add column
    cur.execute("ALTER TABLE coastalwaters DROP COLUMN IF EXISTS heat;")
    cur.execute("ALTER TABLE coastalwaters ADD COLUMN heat NUMERIC;")

    # Calculate heat production
    cur.execute("UPDATE coastalwaters SET heat = (mean-(-1)) * %s;",
                (const,))
