run:
	docker-compose -f app/docker-compose.yml up -d

stop:
	docker-compose -f app/docker-compose.yml down --rmi local -v --remove-orphans
