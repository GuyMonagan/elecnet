# RU

# elecnet

REST API и админ-панель для управления структурой торговой сети по продаже электроники.  
Позволяет создавать иерархические звенья сети (заводы, розничные точки, ИП), управлять продуктами, следить за задолженностью.


## Описание

elecnet — это API на основе Django REST Framework, 
моделирующий трехуровневую сеть продаж электроники:

- Завод
- Розничная сеть
- Индивидуальный предприниматель

Каждое подразделение:
- Имеет одного поставщика (самостоятельно иерархическая структура)
- Хранит контактную информацию
- Ведет учет задолженности перед поставщиками
- Управляет продукцией

Доступ к API ограничен для активных пользователей из числа сотрудников.

---

## 🛠 Стэк

- Python 3.11
- Django 5.0
- Django REST Framework
- PostgreSQL 17 (10+ compatible)
- JWT Authentication
- Swagger (drf-yasg)
- Docker & Docker Compose
- Pytest

---

## Запуск проекта через Docker

### 1. Создайте .env файл

скопируйте `.env.example` в `.env` и подставьте актуальные значения:

```bash
cp .env.example .env
```
Или скопируйте вручную.

### 2. Создайте и запустите докер-контейнер

```
docker compose up --build
```

### 3. Создайте миграции (если требуется)

```
docker compose exec web python manage.py migrate
```
Но как правило миграции создаются автоматически при запуске контейнера.

### 4. Создайте суперюзера (для доступа к админке)

```
docker compose exec web python manage.py createsuperuser

```

API будет доступен на локальном хосте:
```
http://localhost:8000/
```
Swagger документация:
``` 
http://localhost:8000/swagger/
```
---

## Аутентификация

API использует JWT-аутентификацию.

1. Создайте пользователя через админку.
2. Получите токен:

`POST /api/token/`

3. Передавайте access-токен в заголовке:

Authorization: Bearer <access_token>

Доступ к API имеют только активные сотрудники (is_active=True, is_staff=True).

---

## Запуск тестов

```
docker compose exec web pytest

```
---

## Структура проекта

- users – кастомная модель и права доступа (реализована регистрация по электронной почте)
- network – бизнес-логика и API 
- config – настройки проекта

---

## Примечания

- Поле «задолженность» доступно только для чтения через API. 
- задолженность можно погасить с помощью действий администратора (требуются права суперюзера). 
- Глубина иерархии рассчитывается динамически.

---

---

## EN

---

# elecnet

A REST API and admin panel for managing the structure of an electronics retail chain.

It allows you to create hierarchical network units (factories, retail outlets, individual entrepreneurs), manage products, and track outstanding balances.

---

## Description

elecnet is an API based on the Django REST Framework,
modeling a three-tier electronics retail chain:

- Factory
- Retail network
- Individual entrepreneur

Each business unit:
- Has a single supplier (self-referencing hierarchy)
- Stores contact information
- Maintains debt to supplier
- Manages products

Access to the API is restricted to active staff users.

---

## 🛠 Stack

- Python 3.11
- Django 5.0
- Django REST Framework
- PostgreSQL 17 (10+ compatible)
- JWT Authentication
- Swagger (drf-yasg)
- Docker & Docker Compose
- Pytest

---

## Running the project via Docker

### 1. Create a .env file

Copy `.env.example` to `.env` and substitute the relevant values:

```bash
cp .env.example .env
```
Or copy it manually.

### 2. Create and run a Docker container

```
docker compose up --build
```

### 3. Create migrations (if required)

```
docker compose exec web python manage.py migrate
```
As a rule, migrations are created automatically when the container starts.

### 4. Create a superuser (for access to the admin panel)

```
docker compose exec web python manage.py createsuperuser

```

The API will be available on the localhost:
```
http://localhost:8000/
```
Swagger documentation:
```
http://localhost:8000/swagger/
```
---
## Authentication

Obtain JWT token:

```
POST /api/token/

```

Use token in header:
`Authorization: Bearer <access_token>`

Only active staff users have API access.

---

## Running tests

```
docker compose exec web pytest

```

---

## Project structure

- users – custom user model and permissions (registration by email has been implemented)
- network – business logic and API 
- config – project settings

---

## Notes

- Debt field is read-only via API.
- Debt can be cleared via admin action.
- Hierarchy depth is calculated dynamically.
