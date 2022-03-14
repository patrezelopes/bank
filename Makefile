.DEFAULT_GOAL := all

COMPOSE=docker-compose $(COMPOSE_OPTS)


# target: help - display callable targets.
help:
	@egrep "^# target:" [Mm]akefile

# target: up-db - Starts db
up-db:
	$(COMPOSE) up -d bank-db

# target: up-api - Starts api
up-api:
	$(COMPOSE) up -d bank-api

# target: up-worker - Starts worker
up-worker:
	$(COMPOSE) up -d worker-bank

#Starts all apps
start: up-db up-api up-worker

# target: up-worker - Starts worker
up-all:
	$(COMPOSE) up --build -d

# target: stop - Stop all apps
down:
	$(COMPOSE) stop

stop: down

# target: build - Builds docker images
build-no-cache:
	$(COMPOSE) build --no-cache

# target: bash - Runs /bin/bash in App container for development
bash:
	$(COMPOSE) exec api bash

# target: clean - Stops and removes all containers
clean:
	$(COMPOSE) down -v

# target: logs - Shows logs for db, frontend and app
logs-all:
	$(COMPOSE) logs --follow

logs-api:
	$(COMPOSE) logs -f api