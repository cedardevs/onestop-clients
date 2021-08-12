import psycopg2
import sys
import argparse
import json
import yaml

def script_generation(coords, granule_id):
    '''
    Generates a postgres script used for insertion into the database based on the coordinates and granule id given

    :param coords: List[floats]
        coordinates you want to upload to database

    :param granule_id: str
        granule id associated with the coordinates

    :return:

    '''
    # Create an insertion script based on the list of coordinates
    script = ''
    script= script + "insert into granule.data (id, coordinates) values('{}', 'POINT({} {})') ; ".format(granule_id,coords[0],coords[1])
    return script



def postgres_insert(script):
    '''
    Uploads data into spatial database

    :param script: str
        get from script_generation(coords, granule_id)

    :return: str
        response from postgres
    '''
    with open('scripts/config/postgres-config-dev.yml') as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)


    # Define our connection string for postgres db
    conn_string = "host="+ str(conf['host'])+ " port=" + str(conf['port'])+ " dbname="+ conf['db_name']+ " user=" + conf['user']+ " password="+ conf['db_password']

    # print the connection string we will use to connect
    print('Connection String:', conn_string)


    try:
        # get a connection, if a connect cannot be made an exception will be raised here
        conn = psycopg2.connect(conn_string)

        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        cursor = conn.cursor()
        print("Connected!\n")

        cursor.execute(script)
        conn.commit()
        cursor.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

