# ON PC:
#   Modify SRC v /Repositories/mtg-labels
#   Commit and Push to Git
# ON SERVER: 
#   rm -rf mtg-labels
#   git pull
#   docker BUILD
#   docker PUSH
#   docker-compose RESTART mtg-labels

# 1. On server:
rm -rf /home/picluster/Configs/mtg-labels/*
sudo docker-compose stop mtglabels
sudo docker image rm mtglabels

# 2. On PC:
scp mtg-labels picluster@192.168.88.245:/home/picluster/Configs/mtg-labels

# 3. On Server
sudo docker login
sudo docker build --tag valgrut/latest .
sudo docker push valgrut/latest
sudo docker-compose up -d mtglabels

