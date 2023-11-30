# schema for warehouse table
ISS_25544_WAREHOUSE_SCHEMA = {
    'id': 'SERIAL PRIMARY KEY',
    'latitude': 'DECIMAL(10, 6) NOT NULL',
    'longitude': 'DECIMAL(10, 6) NOT NULL',
    'altitude': 'DECIMAL(15, 8) NOT NULL',
    'velocity': 'DECIMAL(15, 8) NOT NULL',
    'visibility': 'VARCHAR(25) NOT NULL',
    'footprint': 'DECIMAL(15, 8) NOT NULL',
    'date': 'TIMESTAMP NOT NULL',
    'daynum': 'DECIMAL NOT NULL',
    'solar_lat': 'DECIMAL(15, 8) NOT NULL',
    'solar_lon': 'DECIMAL(15, 8) NOT NULL',
    'units': "VARCHAR(2) NOT NULL"
}

# schema for normalized table
ISS_25544_NORMALIZED_TABLE_SCHEMA = {
    'id': 'SERIAL PRIMARY KEY',
    'latitude': 'DECIMAL(10, 6) NOT NULL',
    'longitude': 'DECIMAL(10, 6) NOT NULL',
    'visibility': 'VARCHAR(25) NOT NULL',
    'date': 'TIMESTAMP NOT NULL',
    'current_location': 'VARCHAR(255)',
    'distance_travelled': 'DECIMAL(15, 8) NOT NULL',
    "units": "VARCHAR(2)"
}