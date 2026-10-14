# Версия Python проекта (README, .python-version) — одна на обе стадии
ARG PYTHON_VERSION=3.14

# ---------- Стадия 1: сборка окружения с зависимостями ----------
FROM python:${PYTHON_VERSION}-slim AS builder

# Версия uv — вывод uv --version на ноутбуке, где на шаге 1.1 обновлён uv.lock
COPY --from=ghcr.io/astral-sh/uv:0.12.7 /uv /bin/uv

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

# ---------- Стадия 2: финальный образ ----------
FROM python:${PYTHON_VERSION}-slim

# Непривилегированный пользователь, от которого работает приложение
RUN useradd --create-home appuser

WORKDIR /app

# Из стадии сборки берётся только готовое окружение
COPY --from=builder /app/.venv /app/.venv
COPY . .

ENV PATH="/app/.venv/bin:$PATH"

USER appuser

EXPOSE 8000

# Контейнер здоров, если /health отвечает 200 (приложение живо и база доступна)
HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health', timeout=4)"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
