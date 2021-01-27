import psycopg2
import sys
import argparse
import json
from onestop.util.SqsConsumer import SqsConsumer
from onestop.util.S3Utils import S3Utils
from onestop.util.S3MessageAdapter import S3MessageAdapter
from onestop.WebPublisher import WebPublisher
import json
import csv

def sql_script_generation(file_data, object_uuid):
    # Extract the appropriate fields
    lines = file_data.decode('utf-8').split('\n')
    sql_script = ''
    for row in csv.DictReader(lines):
        lon = float(row['LON'])
        lat = float(row['LAT'])
        sql_script= sql_script + "insert into granule (granule_id, coordinates) values('{}', 'POINT({} {})') ; ".format(object_uuid,lon,lat)

    return sql_script

def handler(recs):
    print("Handler...")

    # Now get boto client for object-uuid retrieval
    object_uuid = None
    bucket = None

    if recs is None:
        print("No records retrieved")
    else:
        rec = recs[0]
        bucket = rec['s3']['bucket']['name']
        s3_key = rec['s3']['object']['key']

        object_uuid = s3_utils.get_uuid_metadata(s3_resource, bucket, s3_key)
        if object_uuid is not None:
            print("Retrieved object-uuid: " + object_uuid)
        else:
            print("Adding uuid")
            s3_utils.add_uuid_metadata(s3_resource, bucket, s3_key)

    # Looks to see if the file is a csv file
    if '.csv' in str(s3_key):
         # Use S3Utils to read the file as a raw text
        s3 = s3_utils.connect('s3', s3_utils.conf['s3_region'])
        file_data = s3_utils.read_bytes_s3(s3, bucket, s3_key)
        sql_script = sql_script_generation(file_data, object_uuid)



    # Define our connection string for postgres db
    conn_string = "host= 127.0.0.1 port=5432 dbname=user user=postgres password=foamcat"

    # print the connection string we will use to connect
    print('Connection String:', conn_string)


    try:
        # get a connection, if a connect cannot be made an exception will be raised here
        conn = psycopg2.connect(conn_string)

        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        cursor = conn.cursor()
        print("Connected!\n")

        cursor.execute(sql_script)
        conn.commit()
        cursor.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Launches spatial test")
    parser.add_argument('-conf', dest="conf", required=True,
                        help="AWS config filepath")

    parser.add_argument('-cred', dest="cred", required=True,
                        help="Credentials filepath")
    args = vars(parser.parse_args())

    # Get configuration file path locations
    conf_loc = args.pop('conf')
    cred_loc = args.pop('cred')

    # Upload a test file to s3 bucket
    s3_utils = S3Utils(conf_loc, cred_loc)

    # Low-level api ? Can we just use high level revisit me!
    s3 = s3_utils.connect("s3", None)

    # High-level api
    s3_resource = s3_utils.connect("s3_resource", None)

    bucket = s3_utils.conf['s3_bucket']
    overwrite = True

    sqs_max_polls = s3_utils.conf['sqs_max_polls']

    # Add 3 files to bucket
    local_files = ["file1.csv", "file4.csv"]
    s3_file = None
    for file in local_files:
        local_file = "tests/data/" + file
        s3_file = "csv/" + file
        s3_utils.upload_s3(s3, local_file, bucket, s3_file, overwrite)

    # Receive s3 message and MVM from SQS queue
    sqs_consumer = SqsConsumer(conf_loc, cred_loc)
    s3ma = S3MessageAdapter("config/csb-data-stream-config.yml")
    wp = WebPublisher("config/web-publisher-config-dev.yml", cred_loc)

    queue = sqs_consumer.connect()
    try:
        debug = False
        sqs_consumer.receive_messages(queue, sqs_max_polls, handler)

    except Exception as e:
        print("Message queue consumption failed: {}".format(e))
