generate-conf:
	@echo "======================================================================"
	@echo "Build telegraf configuration files from template"
	@echo "======================================================================"
	python generate_telegraf_configuration.py
	ls tig_configuration/telegraf-*.conf -l
	@echo "======================================================================"
	@echo "Build SaltStack configuration files from template"
	@echo "======================================================================"
	python generate_saltstack_configuration.py
	ls saltstack_configuration -l

up:	
	@echo "======================================================================"
	@echo "Start all containers"
	@echo "======================================================================"
	docker-compose up -d
	@echo "======================================================================"
	@echo "Start SaltStack daemons"
	@echo "======================================================================"
	python start_saltstack.py

down:
	@echo "======================================================================"
	@echo "stop docker containers, remove docker containers, remove docker networks"
	@echo "======================================================================"
	docker-compose -f ./docker-compose.yml down

grafana-cli:
	@echo "======================================================================"
	@echo "start a shell session in the grafana container"
	@echo "======================================================================"
	docker exec -i -t grafana /bin/bash

master-cli:
	@echo "======================================================================"
	@echo "start a shell session in the saltstack master container"
	@echo "======================================================================"
	docker exec -i -t master bash

minion-cli:
	@echo "======================================================================"
	@echo "start a shell session in the saltstack minion container"
	@echo "======================================================================"
	docker exec -i -t minion1 bash

telegraf-openconfig-cli:
	@echo "======================================================================"
	@echo "start a shell session in the telegraf container for Openconfig"
	@echo "======================================================================"
	docker exec -i -t telegraf-openconfig /bin/bash

telegraf-snmp-cli:
	@echo "======================================================================"
	@echo "start a shell session in the telegraf container for SNMP"
	@echo "======================================================================"
	docker exec -i -t telegraf-snmp /bin/bash

influxdb-cli:
	@echo "======================================================================"
	@echo "start a shell session in the influxb container"
	@echo "======================================================================"
	docker exec -it influxdb bash

influxdb-logs:
	@echo "======================================================================"
	@echo "fetch the 100 last lines of logs of the influxb container"
	@echo "======================================================================"
	docker logs influxdb --tail 100

grafana-logs:
	@echo "======================================================================"
	@echo "fetch the 100 last lines of logs of the grafana container"
	@echo "======================================================================"
	docker logs grafana --tail 100

telegraf-snmp-logs:
	@echo "======================================================================"
	@echo "fetch the 100 last lines of logs of the telegraf-snmp container"
	@echo "======================================================================"
	docker logs telegraf-snmp --tail 100

telegraf-openconfig-logs:
	@echo "======================================================================"
	@echo "fetch the 100 last lines of logs of the telegraf-openconfig container"
	@echo "======================================================================"
	docker logs telegraf-openconfig --tail 100

