# How to Update the live Docker container on Server

# 1. On server:
rm -rf /home/picluster/Configs/mtg-labels/*
sudo docker-compose stop mtglabels
sudo docker rm mtglabels
sudo docker image rm mtglabels
sudo docker image rm valgrut/mtg-labels
sudo docker ps -a

# 2. On PC:
scp -r mtg-labels picluster@192.168.88.245:/home/picluster/Configs/mtg-labels
##TODO: Why? I can just pull the new version of Repository...

# 3. On Server
sudo docker login
sudo docker build --tag valgrut/mtg-labels .
sudo docker push valgrut/mtg-labels
sudo docker-compose up -d mtglabels

