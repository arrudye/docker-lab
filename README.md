# Библиотека
Библиотечная система на Python (FastAPI) + PostgreSQL в отдельных Docker-контейнерах. 

Каждый компонент запускается в Docker-контейнере в пределах Docker-сети. Доступ извне можно получить только к API. 

## Запуск:
### Файл `.env`:
```POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=library
POSTGRES_USER=admin
POSTGRES_PASSWORD=secret

API_HOST=0.0.0.0
API_PORT=8000
```

### Запуск контейнеров:
`docker-compose up --build`

### Документация:
http://localhost:8000/docs


