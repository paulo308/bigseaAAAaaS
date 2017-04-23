
sudo rm -rf data/*
sudo rm -rf dump/*
#sed -i 's/mongod\ --port\ 27017.*/mongod\ --port\ 27017\ --dbpath\ \/data\/db/' docker-compose.yml

# criacao de usuario
docker-compose run --entrypoint python3 --name aaa_manager aaa_manager -m db_scripts.create_mongo_user

# Gerar dump do banco de dados
docker exec mongo_test mongodump

#sed -i 's/mongod\ --port\ 27017.*/mongod\ --port\ 27017\ --clusterAuthMode\ x509\ --sslMode\ requireSSL\ --sslPEMKeyFile\ \/certs\/mongo_crt\.pem --sslCAFile\ \/certs\/root_ca\.pem\ --dbpath\ \/data\/db/' docker-compose.yml
