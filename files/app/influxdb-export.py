#!/usr/bin/env python3
"""mqtt2influxdb"""

import json
import logging
import sys
import os
import time

import time
import argparse # for arg parsing...
import json # for parsing json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from datetime import datetime # for obtaining the curren time and formatting it
from influxdb import InfluxDBClient # via apt-get install python-influxdb
requests.packages.urllib3.disable_warnings(InsecureRequestWarning) # suppress unverified cert warnings

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
INFLUXDB_ADDRESS = os.getenv('INFLUXDB_ADDRESS', '127.0.0.1')
INFLUXDB_PORT = int(os.getenv('INFLUX_PORT', "8086"))
INFLUXDB_USER = os.getenv("INFLUXDB_USERNAME")
INFLUXDB_PASSWORD = os.getenv("INFLUXDB_PASSWORD")
INFLUXDB_DATABASE = os.getenv("INFLUXDB_DATABASE", 'mqtt')
INFLUXDB_SQL = os.getenv("INFLUXDB_SQL", 'select * from "infinite"."reading" ')

LOGFORMAT = '%(asctime)-15s %(message)s'

logging.basicConfig(level=LOG_LEVEL, format=LOGFORMAT)
LOG = logging.getLogger("influxdb-export")

def main():
    logging.info("INFO MODE")
    logging.debug("DEBUG MODE")
    
    global influxdb_client
    try:
        if INFLUXDB_USER and INFLUXDB_PASSWORD:
            logging.debug('InfluxDBClient 1')        
            influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, INFLUXDB_PORT, INFLUXDB_USER, INFLUXDB_PASSWORD, None)
        else:
            logging.debug('InfluxDBClient 2')        
            influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, INFLUXDB_PORT)
    except:
        sys.stderr.write("Can't create influx connection\n")
        sys.exit(1)
        
    logging.debug(influxdb_client)        
    logging.debug('Connecting to the database %s' % INFLUXDB_DATABASE)

    result = influxdb_client.query(INFLUXDB_SQL)
    logging.debug("Result: {0}".format(result))

    
if __name__ == '__main__':
        main()