# Python Auth (Django + DRF + JWT)

Коротко: backend аутентификации и авторизации с JWT, кастомным пользователем (логин по email), ролевой моделью доступа на уровне "бизнес‑элементов". Документация — OpenAPI/Swagger. Демо‑данные — management‑команда.

## Технологии
- Django, Django REST Framework
- JWT: djangorestframework-simplejwt (+ blacklist)
- drf-spectacular (OpenAPI/Swagger)
- PostgreSQL, Docker/Compose
- python-dotenv

## Модель доступа (RBAC на бизнес‑элементы)
- `User` → `role: Role` (FK), `is_active` для мягкого удаления, логин по `email`.
- `Role` — роль пользователя.
- `BusinessElement` — абстракция ресурса (например, `code`, `tests`).
- `AccessRule(role, business_element)` — флаги `read/create/update/delete` (+ *_all для расширения).
- Пермишен `HasAccessToBusinessElement`:
  - Требует аутентификацию.
  - Сопоставляет HTTP‑метод с флагом (`GET`→read, `POST`→create, `PUT/PATCH`→update, `DELETE`→delete).
  - Возвращает 403, если у аутентифицированного нет права; 401 обрабатывается `IsAuthenticated`.

## Запуск
1) Создайте `.env` с переменными для Postgres: `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`.
2) Запустите:
```bash
docker compose up --build
```
3) Примените миграции и (опционально) создайте суперпользователя:
```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```
4) Загрузите демо‑данные:
```bash
docker compose exec web python manage.py populate_db
```
5) Swagger UI: `http://localhost:8000/api/schema/swagger-ui/`

## API (префикс: /api/auth/)
- Публичные:
  - `POST /register/` — регистрация (email, first_name, last_name, password, password2). Возвращает `access`/`refresh`.
  - `POST /login/` — вход, возвращает `access`/`refresh`.
- Требуют JWT:
  - `POST /logout/` — принимает `refresh`, вносит в blacklist.
  - `GET|PATCH /profile/` — профиль текущего пользователя.
  - `DELETE /delete/` — мягкое удаление (`is_active=False`) + очистка OutstandingToken.
- Пример защищённого ресурса:
  - `GET /test-resource/` — `IsAuthenticated` + `HasAccessToBusinessElement` с `business_element_name='test_resource'`.
- Mock‑ресурсы (пример):
  - `GET /mock/code/`, `GET /mock/tests/` — рекомендуется `IsAuthenticated` + `HasAccessToBusinessElement` (для 401/403 как в задании).
- Админ‑CRUD (только для админа):
  - `/admin/roles/`, `/admin/business-elements/`, `/admin/access-rules/`.

## Поведение 401/403
- Неаутентифицированный запрос к защищённому ресурсу → 401 (через `IsAuthenticated`).
- Аутентифицированный без нужного права → 403 (через `HasAccessToBusinessElement`).

## Замечания по безопасности
- `DEBUG=True` и `SECRET_KEY` в коде — только для локальной разработки.