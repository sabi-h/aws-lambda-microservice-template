from datetime import datetime, timedelta
from pprint import pprint
from urllib.parse import unquote_plus
import csv
import json
import logging
import os
import time

import pandas as pd
import requests

import fields
import settings
from utils import (
    get_dates,
    upload_to_s3,
    read_s3_file,
    bytes_to_json,
    array_to_string,
    mock_s3_event,
    records_to_csv,
    execute_update,
    get_redshift_connection,
)
from utils import Query, move_s3_file


def transform(data: bytes) -> bytes:
    return data


def load(data: bytes) -> bool:
    return


def lambda_backfill(event, context):
    data = b'hello world'
    transform(data)
    load(data)


if __name__ == "__main__":

    # -----------------------------------------------------------------------------
    # Backfill Test Start
    # -----------------------------------------------------------------------------
    event = {
        "start_date": "2021-01-01",
        "end_date": "2021-01-01",
        "day_quarters": [1],
        "extract": True,
        "transform": False,
        "load": False,
    }

    lambda_backfill(event, context={})
