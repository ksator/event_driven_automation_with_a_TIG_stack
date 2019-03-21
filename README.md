# What is a TIG stack

A TIG stack uses:
- Telegraf to collect data and to write the collected data in Influxdb
- Influxdb to store the data collected
- Grafana to visualize the data stored in Influxdb

# About this repository

This repository is about Event driven automation with a TIG stack and SaltStack.   

Junos devices (spines and leaves IP fabric)  

One Ubuntu VM: 
- Telegraf collects data from Junos devices. 
- The data collected is stored in Influxdb. 
- Grafana queries Influxdb and displays graphs.  
- Grafana is configured with alerts. When there is an alert, Grafana sends a webhook notification to SaltStack (http post with a json body)
- SaltStack reacts to this webhook, and creates a new ticket (or update an existing ticket) on request tracker. 

This repository provides a [docker-compose.yml](docker-compose.yml) file for: 
- telegraf 
- influxdb
- grafana
- SaltStack master
- SatStack minion 
- request tracker 

It also has: 
-  a python script [upgrade_junos.py](upgrade_junos.py) to upgrade Junos with `network-agent` and `openconfig` packages 
-  a python script [configure_junos.py](configure_junos.py) to configure Junos devices (IP Fabric with EBGP)
-  a python script [audit_junos.py](audit_junos.py) to audit BGP sessions state 
-  a python script [generate_telegraf_configuration.py](generate_telegraf_configuration.py) to generate Telegraf configuration files from templates.  
-  a python script [generate_saltstack_configuration.py](generate_saltstack_configuration.py) to generate SaltStack files from templates.  
-  a python script [start_saltstack.py](start_saltstack.py) to start Saltstack services (master and minion) and proxies (one daemon Junos device)

It has also a [Makefile](makefile) to simplify the demo. 

This repository has been tested with an Ubuntu host running 16.04 release.

# Building blocks 

## Telegraf

Telegraf is an open source collector written in GO.
Telegraf collects data and writes them into a database.
It is plugin-driven (it has input plugins, output plugins, ...)

To monitor Junos, we can use the telegraf input plugin jti_openconfig_telemetry (grpc client to collect telemetry on junos devices) and the telegraf input plugin snmp

Telegraf has an output plugin to write the data collected to Influxdb. It supports others output plugins as well.

## Influxdb
Influxdb is an open source time series database written in GO.

## Grafana
Grafana is an open source tool used to visualize time series data.
It supports InfluxDB and other backends.
It runs as a web application.
It is written in GO.

## Request Tracker

Request Tracker (RT) is an open source issue tracking system.

## SaltStack

Salt is a remote execution tool and configuration management system:
- remote execution: run commands on various machines in parallel with a flexible targeting system (salt execution modules)
- configuration management: establishes a client-server model to bring infrastructure components in line with a given policy (salt state modules in sls files)

SaltStack supports event driven infrastructure 

SaltStack competes primarily with Puppet, Chef, StackStorm, and Ansible. 

# requirements on the Ubuntu host

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

# requirements on Junos devices

In this demo Telegraf will use Openconfig telemetry to collect data from Junos devices.  

## Junos packages

In order to collect data from Junos using openconfig telemetry, the devices require the Junos packages ```openconfig``` and ```network agent```  
Starting with Junos OS Release 18.3R1, the Junos OS image includes these 2 packages; therefore, you do not need anymore to install them separately on your device.  
If you are using an older Junos release, it is required to install these two packages separately.  

Run this command to verify:
```
jcluser@vMX1> show version | match "Junos:|openconfig|na telemetry"
```

You can use the python script [upgrade-junos.py](upgrade-junos.py) to install these 2 packages on your Junos devices: 
- `git clone https://github.com/ksator/event_driven_automation_with_a_TIG_stack.git`
- `cd event_driven_automation_with_a_TIG_stack`
- download the Junos packages ```openconfig``` and ```network agent``` from ```http://download.juniper.net/``` and save them in the `event_driven_automation_with_a_TIG_stack` directory  
- Update the file [variables.yml](variables.yml]) with your devices details `vi variables.yml`
- Execute the python script [upgrade-junos.py](upgrade-junos.py) `python ./upgrade-junos.py`


## Junos configuration 

This sort of configuration is required when you use the telegraf input plugin `snmp`
```
jcluser@vMX-1> show configuration snmp
community public;
```
This sort of configuration is required when you use the telegraf input plugin `jti_openconfig_telemetry`
```
jcluser@vMX-1> show configuration system services extension-service | display set
set system services extension-service request-response grpc clear-text port 32768
set system services extension-service request-response grpc skip-authentication
set system services extension-service notification allow-clients address 0.0.0.0/0
```
This sort of configuration is required if you use NETCONF
```
jcluser@vMX-1> show configuration system services netconf | display set
set system services netconf ssh
```




# Usage

## clone the repository
```
git clone https://github.com/ksator/saltstack_junos_docker_compose.git
cd saltstack_junos_docker_compose
```

## Update the variables

```
vi variables.yml
```

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
```
docker exec -it minion1 salt-proxy -d --proxyid=dc-vmx-4
docker exec -it master salt dc-vmx-4 junos.cli 'show chassis hardware'
```
```
docker exec -it master salt-key -L
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
