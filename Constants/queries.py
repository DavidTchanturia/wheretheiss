from Constants.tables_schema import ISS_25544_WAREHOUSE_SCHEMA, ISS_25544_NORMALIZED_TABLE_SCHEMA


CREATE_ISS_WAREHOUSE_TABLE = f"""
CREATE TABLE IF NOT EXISTS iss_25544_warehouse (
    {', '.join(f'{column} {data_type}' for column, data_type in ISS_25544_WAREHOUSE_SCHEMA.items())}
);
"""

# I could not include check here so have to wrtie a whole query
# CREATE_ISS_NORMALIZED_TABLE = f"""
# CREATE TABLE IF NOT EXISTS iss_normalized (
#     {', '.join(f'{column} {data_type}' for column, data_type in ISS_25544_NORMALIZED_TABLE_SCHEMA.items())}
# );
# """

# converted "daylight", "eclipsed" to 1, 0 to partition using range
CREATE_ISS_NORMALIZED_TABLE = """
CREATE TABLE IF NOT EXISTS iss_normalized (
    id SERIAL,
    latitude DECIMAL(10, 6) NOT NULL,
    longitude DECIMAL(10, 6) NOT NULL,
    visibility INT NOT NULL,
    date TIMESTAMP NOT NULL,
    current_location VARCHAR(255),
    distance_travelled DECIMAL(15, 4) NOT NULL,
    units VARCHAR(2),
    PRIMARY KEY (id, visibility)
) PARTITION BY RANGE (visibility);
"""

# creates eclipsed partition
CREATE_ECLIPSED_PARTITION = """
CREATE TABLE IF NOT EXISTS iss_normalized_partition_0 PARTITION OF iss_normalized
    FOR VALUES FROM (MINVALUE) TO (1);
"""

# creates daylight partition
CREATE_DAYLIGHT_PARTITION = """
CREATE TABLE IF NOT EXISTS iss_normalized_partition_1 PARTITION OF iss_normalized
    FOR VALUES FROM (1) TO (MAXVALUE);
"""


INSERT_ISS_INFO_WAREHOUSE = f"""INSERT INTO iss_25544_warehouse (latitude, longitude, altitude, velocity, visibility, footprint, date, daynum, solar_lat, solar_lon, units)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

INSERT_INTO_NORMALIZED_TABLE = """
INSERT INTO iss_normalized (latitude, longitude, visibility, date, current_location, distance_travelled, units)
VALUES (%s, %s, CASE WHEN %s = 'daylight' THEN 1 ELSE 0 END, %s, %s, %s, %s)
"""

# selects data that are in between two timestamps based on columns own timestamp
SELECT_DATA_IN_RANGE_QUERY = """SELECT latitude, longitude, visibility, date
                                FROM iss_25544_warehouse WHERE date BETWEEN '{five_minutes_ago}' AND '{current_timestamp}'"""