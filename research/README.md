Для работы с postgres устанавливаем `asyncpg==0.30.0`, для работы с mongo достаточно поставить зависимости из ugc2/app/requirements.txt

запускаем postgres, пример
``` bash
docker-compose -f docker-compose.yml -f research/docker-compose.yml up postgres -d
```

запускаем mongo, пример
```bash
make infra
```


Запуск генерации данных Postgres
```
python postgres.py
```


Запуск генерации данных Mongo
```
python mongo.py
```
