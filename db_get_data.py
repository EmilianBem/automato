from datetime import datetime
from threading import Thread

import psycopg2

from db_connections import connect_to_db


def get_db_data(*self):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        measurements = {
            'temp': 'bme_temperature',
            'hum': 'humidity'
        }
        measurement = ''
        for item in self:
            measurement = measurement + item
        measurement = measurements[measurement]

        # Prepare the SQL INSERT statement
        select_query = f"""
        select date(time_stamp) as day, {measurement} from measurements group by 1,2 order by day;
        """

        # Execute the INSERT statement
        cursor.execute(select_query)
        rows = cursor.fetchall()
        print(rows)
        connection.commit()
        formatted_data = {str(date): float(temp) for date, temp in rows}

        print(formatted_data)

    except (Exception, psycopg2.Error) as error:
        print("Error:", error)

    finally:
        if connection:
            connection.close()
            print("Connection closed")

    return formatted_data


class CustomThread(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return
