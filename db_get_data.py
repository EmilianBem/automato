from datetime import datetime
import psycopg2
from db_connections import connect_to_db


def get_db_data():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        # Prepare the SQL INSERT statement
        select_query = """
        SELECT * FROM measurements;
        """

        # Execute the INSERT statement
        cursor.execute(select_query)
        rows = cursor.fetchall()

        connection.commit()
        print(rows)

    except (Exception, psycopg2.Error) as error:
        print("Error:", error)

    finally:
        if connection:
            connection.close()
            print("Connection closed")

    return rows


