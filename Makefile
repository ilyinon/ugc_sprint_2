infra:
	docker-compose -f docker-compose.yml up -d --build

ugc: ugc_dir
	$(MAKE) infra
	docker-compose -f docker-compose.yml \
	-f ugc2/docker-compose.yml -f ugc2/docker-compose.override.yml \
	up -d --build
	docker logs -f ugc_sprint_2-ugc2-1

ugc_dir:
	@:

elk: elk_dir
	docker-compose -f elk/docker-compose.yml up -d --build

elk_dir:
	@:

all:
	$(MAKE) infra
	$(MAKE) ugc
	$(MAKE) elk


stop:
	docker-compose -f docker-compose.yml \
	-f ugc2/docker-compose.yml  down

status:
	docker-compose ps

lint:
	pre-commit install
