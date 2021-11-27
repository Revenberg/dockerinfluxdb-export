# dockerinfluxdb-export

sudo apt install gnupg2 pass
docker image build -t dockerinfluxdb-export:latest  .
docker login -u revenberg
docker image push revenberg/dockerinfluxdb-export:latest

docker run revenberg/dockerinfluxdb-export

docker exec -it ??? /bin/sh

docker push revenberg/dockerinfluxdb-export:latest

# ~/dockerinfluxdb-export/build.sh;docker rm -f $(docker ps | grep influxdb-export | cut -d' ' -f1);cd /var/docker-compose;docker-compose up -d influxdb-export;docker logs -f $(docker ps | grep influxdb-export | cut -d' ' -f1)