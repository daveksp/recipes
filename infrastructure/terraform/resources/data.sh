#!/bin/bash

sudo yum update -y
sudo yum search docker
sudo yum info docker
sudo yum install docker -y

sudo usermod -a -G docker ec2-user
id ec2-user
newgrp docker


sudo service docker start
sudo chkconfig docker on
docker pull daveksp/recipe
docker run -d -p 8089:8089 daveksp/recipe
