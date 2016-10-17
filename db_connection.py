"""
    db_connection.py, author: Lukas Klescinec <lukas.klescinec@gmail.com>
    FIIT Slovak University of Technology 2016

    This file is part of school project on lesson Advanced Databases.
"""
import psycopg2


from settings import HOSTNAME, USERNAME, PASSWORD, DB_NAME


def open_connection():
    print "Trying to connect to a database."
    try:
        db_conn = psycopg2.connect(host=HOSTNAME, user=USERNAME, password=PASSWORD, dbname=DB_NAME)
        return db_conn
    except psycopg2.Error as e:
        raise e.pgerror


def close_connection(conn):
    pass
