FROM python:3.14-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY bot.py config.py ./
COPY cogs ./cogs
COPY services ./services

RUN mkdir -p /app/data \
    && groupadd --system bot \
    && useradd --system --gid bot --home-dir /app bot \
    && chown -R bot:bot /app

USER bot

ENV DB_PATH=/app/data/warns.db

CMD ["uv", "run", "--frozen", "--no-dev", "python", "bot.py"]
