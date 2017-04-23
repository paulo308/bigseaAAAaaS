docker stop $(docker ps -q -a)
docker rm $(docker ps -q -a)
sudo rm -rf dump/*
docker-compose run --entrypoint python3 --name aaa_manager aaa_manager -m db_scripts.create_mongo_user
docker exec mongo_test mongodump
