FROM python:alpine3.7

RUN pip install --upgrade pip && pip uninstall serial

COPY files/requirements.txt /app/

WORKDIR /app
RUN pip install -r requirements.txt

RUN mkdir -p /data/backup

COPY files/app* /app/

CMD python ./influxdb-export.py
