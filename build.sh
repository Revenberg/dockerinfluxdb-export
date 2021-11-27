#!/bin/bash

# version 2021-08-07 15:20

cd ~/dockerinfluxdb-export

if [ -n "$1" ]; then
  ex=$1
else
  rc=$(git remote show origin |  grep "local out of date" | wc -l)
  if [ $rc -ne "0" ]; then
    ex=true
  else
    ex=false
  fi
fi

if [ $ex == true ]; then
    git pull
    chmod +x build.sh

    docker image build -t revenberg/influxdb-export:latest .

    docker push revenberg/influxdb-export:latest

    sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' influxdb-export)
    # testing: 

    echo "==========================================================="
    echo "=                                                         ="
    echo "=          docker run revenberg/influxdb-export                ="
    echo "=                                                         ="
    echo "==========================================================="
    # docker run revenberg/influxdb-export
fi

cd -
