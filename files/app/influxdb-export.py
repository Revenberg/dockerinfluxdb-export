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
from prometheus_client import Counter, Gauge, start_http_server

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
PROMETHEUS_PREFIX = os.getenv("PROMETHEUS_PREFIX", "influxdb_export")
PROMETHEUS_PORT = int(os.getenv("PROMETHEUS_PORT", "9003"))
PROMETHEUS_LABEL = os.getenv("PROMETHEUS_LABEL", "export")

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

# global variable
prom_metrics = {}  # pylint: disable=C0103
prom_msg_counter = Counter(
    f"{PROMETHEUS_PREFIX}message_total", "Counter of received messages", [PROMETHEUS_LABEL]
)

def exporting(day):
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
    i = 0
    for row in result.get_points():
        f.write(json.dumps(row) + '\n')
        i = i + 1
    f.close()

    # create metric if does not exist
    prom_metric_name="influxdb_export"
    if not prom_metrics.get(prom_metric_name):
        prom_metrics[prom_metric_name] = Gauge(
            prom_metric_name, "metric generated from MQTT message.", [PROMETHEUS_LABEL]
        )
        LOG.info("creating prometheus metric: %s", prom_metric_name)

    # expose the metric to prometheus
    prom_metrics[prom_metric_name].labels(**{PROMETHEUS_LABEL: PROMETHEUS_LABEL}).set( i )
    LOG.debug("new value for %s: %s", prom_metric_name, i)
    
def main():
    # start prometheus server
    start_http_server(PROMETHEUS_PORT)


    schedule.every(6).hours.do(exporting, day=1)
    schedule.every().hour.do(exporting, day=0)
    
    logging.debug(datetime.today())
    logging.debug( schedule.get_jobs() )

    schedule.run_all()

    while True:
        schedule.run_pending()
        time.sleep(1)
    
if __name__ == '__main__':
        main()
