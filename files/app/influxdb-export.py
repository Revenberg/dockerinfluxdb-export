#!/usr/bin/env python3
"""influxdb-export"""

import logging
import json
import sys
import os
import schedule
import time
from datetime import datetime, timedelta
from influxdb import InfluxDBClient # via apt-get install python-influxdb

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
INFLUXDB_ADDRESS = os.getenv('INFLUXDB_ADDRESS', '127.0.0.1')
INFLUXDB_PORT = int(os.getenv('INFLUX_PORT', "8086"))
INFLUXDB_USER = os.getenv("INFLUXDB_USERNAME")
INFLUXDB_PASSWORD = os.getenv("INFLUXDB_PASSWORD")
INFLUXDB_DATABASE = os.getenv("INFLUXDB_DATABASE", 'mqtt')
INFLUXDB_SQL = os.getenv("INFLUXDB_SQL", 'select * from "infinite"."reading" ')
INFLUXDB_WHERE = os.getenv("INFLUXDB_WHERE", " WHERE time >= '%s 00:00:00' and time < '%s 23:59:59' ")


LOGFORMAT = '%(asctime)-15s %(message)s'

logging.basicConfig(level=LOG_LEVEL, format=LOGFORMAT)
LOG = logging.getLogger("influxdb-export")

def export(day):
    logging.info("INFO MODE")
    logging.debug("DEBUG MODE")

    logging.debug(day)

    try:
        if INFLUXDB_USER and INFLUXDB_PASSWORD:
            logging.debug('InfluxDBClient 1')
            influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, INFLUXDB_PORT, INFLUXDB_USER, INFLUXDB_PASSWORD, INFLUXDB_DATABASE)
        else:
            logging.debug('InfluxDBClient 2')
            influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, INFLUXDB_PORT, None, None, INFLUXDB_DATABASE)
    except:
        sys.stderr.write("Can't create influx connection\n")
        sys.exit(1)

    logging.debug('Connecting to the database %s' % INFLUXDB_DATABASE)

    today = datetime.today() - timedelta(days=day)
    todayyyymmdd = today.strftime('%Y-%m-%d')

    q = INFLUXDB_SQL + (INFLUXDB_WHERE  % (todayyyymmdd, todayyyymmdd))
    logging.debug(q)
    result = influxdb_client.query(q)

    f = open("/data/backup/" + todayyyymmdd + ".json", "w")
    for row in result.get_points():
        logging.debug(json.dumps(row))
        f.write(json.dumps(row))
    f.close()

def job():
    print("I'm working...")

def main():
    schedule.every().hour.do(export, export='1')
    schedule.every().hour.do(export, export='0')
    schedule.every(3).minutes.do(job)

    logging.debug(datetime.today())
    logging.debug( schedule.get_jobs() )

    while True:
        schedule.run_pending()
        time.sleep(1)
    
if __name__ == '__main__':
        main()