# About this repository

# requirements

## install docker 

## install docker-compose 

on Ubuntu 16.04
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

```
docker-compose -f docker-compose.yml up -d
docker images
docker ps
```
```
docker-compose -f docker-compose.yml down
docker images
docker ps
```


