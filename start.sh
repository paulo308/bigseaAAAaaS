#!/bin/sh

restore_mongo() {
    # stop and remove all running containers using mongo:3.3 image
    # start mongo server and restore the data dump
    docker-compose run -d --entrypoint mongod --name mongo mongo --dbpath /data/db
    docker exec mongo mongorestore
    docker stop mongo && docker rm mongo
}

# remove all containers and custom networks
docker rm -f $(docker ps -a -q) 2>/dev/null
for network in $(docker network ls -q -f "type=custom"); do
    docker network rm $network
done

restore_mongo
docker-compose -f docker-compose.yml up --build 
