run:
	docker-compose -f docker-compose.yml up -d

stop:
	docker-compose -f docker-compose.yml down --rmi local -v --remove-orphans
