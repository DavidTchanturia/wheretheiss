from Constants.tables_schema import ISS_25544_WAREHOUSE_SCHEMA


CREATE_ISS_WAREHOUSE_TABLE = f"""
CREATE TABLE IF NOT EXISTS iss_25544_warehouse (
    {', '.join(f'{column} {data_type}' for column, data_type in ISS_25544_WAREHOUSE_SCHEMA.items())}
);
"""

INSERT_ISS_INFO_WAREHOUSE = f"""INSERT INTO iss_25544_warehouse (latitude, longitude, altitude, velocity, visibility, footprint, date, daynum, solar_lat, solar_lon, units)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""