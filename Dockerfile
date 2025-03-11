FROM python:3.13-slim-bookworm AS base
 
FROM base AS builder
COPY --from=ghcr.io/astral-sh/uv:0.6.5 /uv /bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev
 
 
FROM base
COPY --from=builder /app /app

ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8501

ENTRYPOINT []
CMD ["streamlit", "run", "/app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
 