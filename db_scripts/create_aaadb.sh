docker stop $(docker ps -q -a)
docker rm $(docker ps -q -a)

stop_cont() {
    docker stop $* 2>/dev/null && docker rm $* 2>/dev/null
}

stop_all_cont() {
    docker stop aaa_manager cfssl mongo 2>/dev/null && docker rm aaa_manager cfssl mongo 2>/dev/null
}

stop_all_cont
sudo rm -rf data/*
sudo rm -rf dump/*
sed -i 's/mongod\ --port\ 27017.*/mongod\ --port\ 27017\ --dbpath\ \/data\/db/' docker-compose.yml

# user creation
docker-compose run --entrypoint python3 --name aaa_manager aaa_manager -m db_scripts.create_mongo_user
#stop_cont aaa_manager mongo


# Generate database dump
docker exec mongo mongodump
#stop_cont mongo

sed -i 's/mongod\ --port\ 27017.*/mongod\ --port\ 27017\ --clusterAuthMode\ x509\ --sslMode\ requireSSL\ --sslPEMKeyFile\ \/certs\/mongo_crt\.pem --sslCAFile\ \/certs\/root_ca\.pem\ --dbpath\ \/data\/db/' docker-compose.yml
