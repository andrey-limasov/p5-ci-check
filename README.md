# Учёт заявок на ремонт оборудования

Веб-сервис, через который сотрудники подают заявки на ремонт офисного и лабораторного оборудования, а инженеры принимают их в работу и закрывают. Приложение для сотрудников организации и инженеров административно-хозяйственного отдела.

## Команда

- Иван Петров (@ivan-petrov) — Team Lead, Backend Developer
- Мария Соколова (@maria-sokolova) — Tech Lead, Backend Developer
- Олег Ким (@oleg-kim) — Backend Developer, документация

## Стек технологий

- Python 3.14
- FastAPI
- PostgreSQL
- Docker
- GitHub Actions

## Статус

Проект в разработке.

## Запуск через Docker Compose

Нужно: Docker с Compose v2 или новее (`docker compose version` отвечает), свободные порты 8000 и 5432 (порт базы опубликован в `compose.yaml` для подключения из IDE).

1. Создать файл с переменными окружения из примера:

   ```bash
   cp .env.example .env            # Windows PowerShell: Copy-Item .env.example .env
   ```

   Открыть `.env` и заменить `changeme` на свой пароль базы (латинские буквы и цифры).

2. Поднять стек:

   ```bash
   docker compose up --build
   ```

3. Проверить — во втором окне терминала или в браузере: `http://localhost:8000/health` отвечает `{"status":"healthy","database":"ok"}`.

   ```bash
   curl http://localhost:8000/health        # Windows PowerShell: curl.exe http://localhost:8000/health
   ```

Порт 8000 занят — задайте в `.env` `APP_PORT=8001` и проверяйте `http://localhost:8001/health`.

Режим `prod` (без `/docs`): `APP_ENV=prod` в `.env` и `docker compose up -d`.

Остановить: `Ctrl+C` или `docker compose down`. Удалить вместе с данными базы: `docker compose down -v`.

## Локальная разработка без Docker

Приложение проверяет настройки при старте: без `DATABASE_URL` оно не запускается и пишет `database_url Field required`.

1. Поднять только базу: `docker compose up -d db`
2. Скопировать из `.env.example` в `.env` строку `# DATABASE_URL=...localhost...` и убрать `#` в её начале
3. Запустить:

   ```bash
   uv sync
   uv run uvicorn main:app --reload
   ```

`http://localhost:8000/health` отвечает `{"status":"healthy","database":"ok"}`.

## Предметная область

- **Основная сущность:** заявка на ремонт оборудования (ticket): что сломалось, где, кто подал, статус
- **Пользователи:** сотрудники организации подают заявки и следят за статусом; инженеры АХО принимают заявки в работу и закрывают их
- **Планируемые эндпоинты:**
  - `POST /tickets` — создать заявку
  - `GET /tickets` — список заявок
  - `GET /tickets/{id}` — одна заявка
  - `PUT /tickets/{id}` — изменить заявку (статус, исполнитель)
  - `DELETE /tickets/{id}` — удалить заявку

## API

| Метод и путь | Ответ | Назначение |
|---|---|---|
| `GET /` | `{"message": "Hello World"}` | Проверка, что приложение отвечает |
| `GET /health` | `{"status": "healthy", "database": "ok"}`; база недоступна — `503` | Health-check: приложение живо и база данных отвечает |
| `GET /version` | `{"version": "0.2.0", "team": "repair-requests"}` | Версия приложения и команда-владелец. Пример: `curl http://localhost:8000/version` |
| `GET /docs` | Страница Swagger UI; при `APP_ENV=prod` — `404` | Документация API, FastAPI генерирует её автоматически; только при `APP_ENV=dev` |

Проба: PR в develop при обязательных проверках (workflow запускается только для main).
