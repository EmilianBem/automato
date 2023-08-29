from datetime import datetime
from app import get_measurements
import psycopg2
from db_connections import connect_to_db

def insert_data(connection=connect_to_db()):
    try:
        
        cursor = connection.cursor()

         # Prepare the SQL INSERT statement
        insert_query = """
        INSERT INTO measurements (time_stamp, soil_temperature, moisture, bme_temperature, humidity, pressure)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        data = get_measurements()

        data_to_insert = (
            datetime.now(),
            round(data["soil_temperature"],2),
            round(data["moisture"],0),
            round(data["bme_temperature"],0),
            round(data["humidity"],0),
            round(data["pressure"],4)
        )
        print(data_to_insert)

        # Execute the INSERT statement
        cursor.execute(insert_query, data_to_insert)
        connection.commit()
        print("Data inserted successfully")

    except (Exception, psycopg2.Error) as error:
        print("Error:", error)

    finally:
        if connection:
            connection.close()
            print("Connection closed")


