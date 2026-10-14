"""Все параметры конфигурации приложения — в одном месте.

Значения берутся из переменных окружения, при локальном запуске — ещё и из файла .env.
Переменная окружения побеждает значение из .env.
"""
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",   # при запуске без Docker; в контейнере .env нет (.dockerignore)
        extra="ignore",    # в .env лежат и переменные Compose: POSTGRES_PASSWORD, APP_PORT
        hide_input_in_errors=True,  # не выводить значения (в том числе пароли) в сообщение об ошибке
    )

    # Окружение: dev — ноутбук разработчика, prod — сервер
    app_env: Literal["dev", "prod"] = "dev"

    # Секрет: без значения по умолчанию, пустая строка не принимается
    database_url: str = Field(min_length=1)

    # Несекретные параметры — с умолчанием
    db_connect_timeout: int = 3


settings = Settings()
