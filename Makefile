infra:
	docker-compose -f docker-compose.yml up -d --build

ugc2: ugc2_dir
	$(MAKE) infra
	docker-compose -f docker-compose.yml \
	-f ugc2/docker-compose.yml -f ugc2/docker-compose.override.yml \
	up -d --build
	docker logs -f ugc_sprint_2-ugc2-1

ugc2_dir:
	@:


all:
	$(MAKE) infra
	$(MAKE) ugc2


stop:
	docker-compose -f docker-compose.yml \
	-f ugc2/docker-compose.yml  down

status:
	docker-compose ps

lint:
	pre-commit install
