# About this repository

This repository provides a docker-compose file for SaltStack master and minion, including the dependencies to use Junos modules and Junos syslog engine.  

This repository has been tested with an Ubuntu host running 16.04 release.

# requirements

You first need to install Docker and Docker-compose on your Ubuntu host 

## install these dependencies
```
sudo apt-get update
sudo apt-get install python-pip -y
pip install pyyaml jinja2
pip list
```

## install docker 

Check if Docker is already installed 
```
$ docker --version
```

If it was not already installed, install it. Here's how to install in on Ubuntu 16.04:  
```
$ sudo apt-get update
```
```
$ sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
```
```
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```
```
$ sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
```
```
$ sudo apt-get update
```
```
$ sudo apt-get install docker-ce
```
```
$ sudo docker run hello-world
```
```
$ sudo groupadd docker
```
```
$ sudo usermod -aG docker $USER
```

Exit the ssh session to your ubuntu and open an new ssh session to your ubuntu and run these commands to verify you installed Docker properly:  
```
$ docker run hello-world

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/engine/userguide/
```
```
$ docker --version
Docker version 18.03.1-ce, build 9ee9f40
```


## install docker-compose 

```
sudo curl -L https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
```
```
sudo chmod +x /usr/local/bin/docker-compose
```
```
docker-compose --version
```
# Usage

## clone the repository
```
git clone https://github.com/ksator/saltstack_junos_docker_compose.git
cd saltstack_junos_docker_compose
```

## Update the variables

vi variables.yml

## Generate SaltStack files

Run this script to generate SaltStack files.  
It uses your variables to create saltstack files (pillars, minion and proxy configurartion files, ...)
```
python render.py
```

## run these commands to start the containers

```
docker-compose -f docker-compose.yml up -d
docker images
docker ps
```

## If you want to connect to a running container cli, run these commands:
```
docker exec -it master bash
exit
```
```
docker exec -it minion1 bash
exit
```

## Start the salt service
Run these commands to start the salt service
```
docker exec -it master service salt-master start
docker exec -it minion1 service salt-minion start
```
## Verify the setup works
```
docker exec -it master salt-key -L
```
```
docker exec -it master salt minion1 test.ping
docker exec -it master salt "minion1" cmd.run "pwd"
```
```
docker exec -it minion1 salt-proxy -d --proxyid=dc-vmx-3
docker exec -it master salt dc-vmx-3 junos.cli 'show chassis hardware'
```

## Verify the junos syslog engine 
```
docker exec -it master salt 'dc-vmx-3' state.apply syslog
```
Connect to the master cli and watch the event bus:  
```
docker exec -it master bash
salt-run state.event pretty=True
```
ssh the junos device and commit a configuration change and watch the event bus on the master

## run these commands to stop the containers
```
docker-compose -f docker-compose.yml down
docker images
docker ps
docker ps -a
```
