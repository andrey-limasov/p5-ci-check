"""Все параметры конфигурации приложения — в одном месте."""
from dotenv import load_dotenv

load_dotenv()   # не перезаписывает переменные, уже заданные в окружении

import os
import sys

REQUIRED = ("DATABASE_URL",)
missing = [name for name in REQUIRED if not os.environ.get(name)]
if missing:
    sys.exit(f"Не заданы обязательные переменные окружения: {', '.join(missing)}")

APP_ENV = os.environ.get("APP_ENV", "dev")
if APP_ENV not in ("dev", "prod"):
    sys.exit(f"APP_ENV должна быть dev или prod, получено: {APP_ENV}")

DATABASE_URL = os.environ["DATABASE_URL"]
DB_CONNECT_TIMEOUT = int(os.environ.get("DB_CONNECT_TIMEOUT", "3"))
