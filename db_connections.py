import psycopg2


def connect_to_db():
    # connect to database
    try:
        connection = psycopg2.connect(
            host="192.168.99.149",
            database="automato",
            user="pi",
            password='dupa'
        )
        print("connection database sukcesfull")
    except (Exception, psycopg2.Error) as error:
        print("Error:", error)

    return connection
