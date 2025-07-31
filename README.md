# Hacettepe Route Analysis

This repo compares the routes obtained from the legacy database of [harita.hacettepe.edu.tr/](https://harita.hacettepe.edu.tr/) which relied on an in-house developed geospatial database (can be restored from the `postgis_databases/legacy`), and with those obtained from OSRM as of July 2025. The routes are avaiable in two modes: i) _bicycle_ and ii) _pedestrian_.

Steps the execute the functions to obtain the scatter plots:
1. Restore the `postgis_databases/hacettepe_routes` into the PostGIS database: `hacettepe_routes`.
2. Update the code so that it matches with your PostgreSQL/PostGIS settings:
```SQL
conn = psycopg2.connect(
    dbname="hacettepe_routes",
    user="postgres",
    password="12345Aa",
    host="localhost",
    port="5432"
)
```

