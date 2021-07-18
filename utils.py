from datetime import datetime, timedelta
import csv
import functools
import gzip
import io
import json
from typing import IO
import urllib.parse

import boto3
import psycopg2

import settings


s3_resource = boto3.resource("s3")


def print_function_state(func):
    @functools.wraps(func)
    def wrapper_print_function_state(*args, **kwargs):
        print(f"\n running function: {func.__name__}")
        value = func(*args, **kwargs)
        print(f" successfull: {func.__name__} ...")
        return value

    return wrapper_print_function_state


class Query:
    @staticmethod
    def insert(schema, staging_table, destination_table) -> str:
        return f"""
            INSERT INTO {schema}.{destination_table}
            SELECT * FROM {schema}.{staging_table};
        """

    @staticmethod
    def truncate(schema: str, table: str) -> str:
        query = f"""
            TRUNCATE TABLE {schema}.{table};
        """
        return query

    @staticmethod
    def delete(
        schema,
        staging_table,
        staging_id,
        destination_table,
        destination_id,
    ) -> str:
        """Returns delete query

        Args:
            schema (str): Table Schema
            staging_table (str): Staging table
            staging_id (str): column for delete
            destination_table (str): Destination table
            destination_id (str): column for delete

        Returns:
            str: query string

        """
        query = f"""
            DELETE FROM {schema}.{destination_table}
            USING {schema}.{staging_table}
            WHERE {destination_table}.{destination_id} = {staging_table}.{staging_id};
        """
        return query

    @staticmethod
    def copy_from(
        schema: str,
        table: str,
        object_path: str,
        header: list,
        header_rows=1,
        delimiter=",",
    ) -> str:
        header = get_header_for_copy_cmd(header)
        query = f"""
            COPY {schema}.{table}({header}) 
            FROM '{object_path}' 
            access_key_id '{settings.REDSHIFT_ACCESS_KEY_ID}' secret_access_key '{settings.REDSHIFT_SECRET_ACCESS_KEY}'
            FORMAT AS csv IGNOREHEADER AS {header_rows} EMPTYASNULL BLANKSASNULL timeformat 'auto' ;
        """
        return query


def list_bucket_files(bucket_name, prefix=''):
    bucket = s3_resource.Bucket(bucket_name)
    return bucket.objects.filter(Prefix=prefix)


@print_function_state
def move_s3_file(bucket_name: str, src_key: str, dst_key: str, s3_resource=s3_resource):
    """Moves file between s3 folders.

    Note! This function will delete file from source.

    Args:
        s3_resource (boto3.resources.factory.s3.ServiceResource): boto3.resource("s3")
        bucket_name (str): name of bucket
        src_key (str): path to src
        dst_key (str): path to dst
    """
    print(f"moving: \n bucket: {bucket_name} \n {src_key} >> {dst_key}")
    s3_resource.Object(bucket_name, dst_key).copy_from(CopySource=f"{bucket_name}/{src_key}")
    s3_resource.Object(bucket_name, src_key).delete()


@print_function_state
def records_to_csv(data: list) -> str:
    """Takes list of dictionaries, parses through csv module and returns a string.

    Args:
        data (list): List of dictionaries

    Returns:
        str
    """
    header = data[0].keys()
    file_obj = io.StringIO()
    dict_writer = csv.DictWriter(file_obj, header, quoting=csv.QUOTE_ALL)
    dict_writer.writeheader()
    dict_writer.writerows(data)
    return file_obj.getvalue()


def array_to_string(array: list) -> str:
    return "<c>".join([x for x in array if x is not None])


def string_to_array(string: str) -> list:
    return string.split("<c>")


@print_function_state
def bytes_to_json(data: bytes) -> list:
    data = json.loads(data)
    print(f"no. of rows: {len(data)}")
    return data


def get_dates(start_date: str, end_date: str) -> list:
    """
    Gets all dates including and between start and end date.

    Returns:
        list: list of strings where each string is a date in yyyy-mm-dd format.
    """
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    if start_date > end_date:
        return "Error: End date must be earlier than start date."

    delta = timedelta(days=1)

    # Get number of days between start and end date, including both.
    days = (end_date - start_date).days + 1

    return [(start_date + day * delta).strftime("%Y-%m-%d") for day in range(days)]


@print_function_state
def upload_to_s3(bucket_name, key_name, data, s3_resource=s3_resource):
    s3_obj = s3_resource.Object(bucket_name, key_name)
    s3_obj.put(Body=data)
    return True


@print_function_state
def read_s3_file(bucket_name: str, key: str, s3_resource=s3_resource) -> bytes:
    print(f"s3://{bucket_name}/{key}")
    s3_obj = s3_resource.Object(bucket_name=bucket_name, key=key)
    return s3_obj.get()["Body"].read()


@print_function_state
def get_redshift_connection():
    """
    Returns connection to redshift
    """
    connection = psycopg2.connect(
        host=settings.REDSHIFT_HOST,
        user=settings.REDSHIFT_USER,
        port=5439,
        password=settings.REDSHIFT_PASSWORD,
        dbname=settings.REDSHIFT_DBNAME,
    )
    return connection


@print_function_state
def execute_update(connection, query: str):
    message = None
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        result = True
    except Exception as e:
        connection.rollback()
        message = e
        result = False
    finally:
        connection.close()

    return (result, message)


@print_function_state
def execute_query(connection, query: str):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        result = cursor.fetchall()
    except Exception as e:
        connection.rollback()
        result = []
    finally:
        connection.close()

    return result


def get_header_for_copy_cmd(header: list) -> str:
    """
    Converts list of strings to string which is accepted by COPY command.
    """
    return ", ".join([f'"{x}"'.format(x) for x in header])


def get_conn_string(db_conn):
    return "dbname='{}' port='5439' user='{}' password='{}' host='{}'".format(
        db_conn["db_name"],
        db_conn["db_username"],
        db_conn["db_password"],
        db_conn["db_host"],
    )


def create_conn(conn_string):
    return psycopg2.connect(conn_string)


def get_conn(db_connection):
    return create_conn(get_conn_string(db_connection))


def mock_s3_event(bucket_name: str, key: str, quote_key=True):
    return {
        "Records": [
            {
                "s3": {
                    "bucket": {"name": bucket_name},
                    "object": {"key": urllib.parse.quote(key) if quote_key else key},
                }
            }
        ]
    }


def run_update(query: str, db_connection):
    con = get_conn(db_connection)
    return execute_update(con, con.cursor(), query)


def run_query(query: str, db_connection):
    con = get_conn(db_connection)
    return execute_query(con, con.cursor(), query)


def get_data_from_redshift(connection, query):
    cursor = connection.cursor()
    cursor.query(query)


if __name__ == "__main__":
    data = read_s3_file("anw-redshift", "test-sabi/csv_file.csv", s3_resource=s3_resource)
    print(type(data))
