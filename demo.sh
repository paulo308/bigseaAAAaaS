#!/bin/sh

# remove all containers and custom networks
docker rm -f $(docker ps -a -q) 2>/dev/null
for network in $(docker network ls -q -f "type=custom"); do
    docker network rm $network
done

docker-compose -f docker-compose.yml up --build 
