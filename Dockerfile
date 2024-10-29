FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

RUN apt update && apt install -y curl

WORKDIR /app

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

HEALTHCHECK CMD curl --fail http://localhost:80/v1/health || exit 1

COPY ./ /app/

RUN uv sync --frozen

ENTRYPOINT ["uv", "run", "fastapi", "run", "src/bs/main.py", "--port", "80"]
