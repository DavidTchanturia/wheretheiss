from Constants.tables_schema import ISS_25544_WAREHOUSE_SCHEMA, ISS_25544_NORMALIZED_TABLE_SCHEMA


CREATE_ISS_WAREHOUSE_TABLE = f"""
CREATE TABLE IF NOT EXISTS iss_25544_warehouse (
    {', '.join(f'{column} {data_type}' for column, data_type in ISS_25544_WAREHOUSE_SCHEMA.items())}
);
"""

CREATE_ISS_NORMALIZED_TABLE = f"""
CREATE TABLE IF NOT EXISTS iss_normalized (
    {', '.join(f'{column} {data_type}' for column, data_type in ISS_25544_NORMALIZED_TABLE_SCHEMA.items())}
);
"""


INSERT_ISS_INFO_WAREHOUSE = f"""INSERT INTO iss_25544_warehouse (latitude, longitude, altitude, velocity, visibility, footprint, date, daynum, solar_lat, solar_lon, units)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

INSERT_INTO_NORMALIZED_TABLE = f"""INSERT INTO iss_normalized (latitude, longitude, visibility, date, current_location, distance_travelled, units)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

SELECT_ALL_FROM_ISS_WAREHOUSE = """SELECT * FROM iss_25544_warehouse"""

SELECT_DATA_IN_RANGE_QUERY = "SELECT * FROM iss_25544_warehouse WHERE date BETWEEN '{five_minutes_ago}' AND '{current_timestamp}'"