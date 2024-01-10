# wheretheiss ETL Project Documentation

## Overview

Welcome to the ETL (Extract, Transform, Load) project, a sophisticated solution designed to interact with the International Space Station (ISS) API. This project seamlessly ingests real-time data from the ISS API, transforms it through a comprehensive pipeline, and loads it into a PostgreSQL database, mimicking the architecture of a data lake and data warehouse.

## Project Architecture

1. **ISS API Integration:**
   The pipeline is intricately connected to the ISS API, ensuring a continuous flow of real-time data.
data about the international space station is inserted in the data lake very two seconds after sending the request to the api.
Two apis used in the program are:
- [International Space Station API](https://api.wheretheiss.at/v1/satellites)
- [Reverse Geocoding API](https://api.wheretheiss.at/v1/satellites)
<br>

2. **Data Lake Simulation:**
   Raw data without any modifications is continuously ingested into the `raw_data.json` file, mirroring the structure and principles of a data lake.

<br>


3. **Data Warehouse Processing:**
   Every two minutes, data from the data lake which has not already been inserted is efficiently inserted into the `iss_24455_warehouse` table within the PostgreSQL database.
This table emulates the characteristics of a data warehouse.

<br>

4. **Data Transformation and Geocoding:**
   Every five minutes, the warehouse data is extracted, and the distance traveled by the ISS in the past five minutes is calculated. all the middle data transformations are happening using Pandas
Subsequently, latitude and longitude are utilized in conjunction with a reverse geocoding API to determine the exact location of the ISS.

<br>

5. **Table Partitioning:**
   The `iss_normalized` table is intelligently partitioned based on the visibility field, which signifies whether it is day (visibility = 1) or night (visibility = 0).

6. **Execution Process:**
   The project can be executed  by running the `main.sh` Bash file. This file orchestrates the execution of the JSON module (as a background task), the warehouse module, and the ISS normalized table module.

7. **Dockerization:**
   To streamline deployment, a Dockerfile and `docker-compose.yml` have created. This results in the creation of a single image containing two services: the application itself and a PostgreSQL instance.

## Getting Started

To run the program, follow these simple steps:

```bash
docker-compose up --build
