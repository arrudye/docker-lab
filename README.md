# Библиотека
Библиотечная система на Python (FastAPI) + PostgreSQL в отдельных Docker-контейнерах. 

Каждый компонент запускается в Docker-контейнере в пределах Docker-сети. Доступ извне можно получить только к API. 

CI/CD настроен через GitHub Actions.

## Запуск:
### 1. Создайте файл `.env` в корне проекта:
```POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=library
POSTGRES_USER=admin
POSTGRES_PASSWORD=secret

API_HOST=0.0.0.0
API_PORT=8000
```

### 2. Запустите контейнеры:
`docker-compose up --build`

### 3. Документация:
http://localhost:8000/docs

### 4. Локальный запуск тестов и линтера:
1. Установите зависимости: 
```cd app
pip install -r requirements.txt
```
2. Запустите линтер:
`ruff check src/`

3. Запустите тесты с проверкой покрытия:
`pytest tests/ -v --cov=src --cov-report=term --cov-fail-under=50`
либо с HTML отчетом:
`pytest tests/ --cov=src --cov-report=html`

## CI/CD

GitHub Actions: build -> lint -> test (coverage >=50%) > docker-build > docker-push


