# uv docker image based on Debian bookworm
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim
#FROM python:3.13-slim

# python env variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# make your code available within image at /app
ADD . /app
WORKDIR /app
# install dependencies
RUN uv sync --locked
# place installed packages at front of path
ENV PATH="/app/.venv/bin:$PATH"

# reset entrypoint 
ENTRYPOINT []
# expose port
EXPOSE 9000

# set env variables
# see https://docs.docker.com/compose/how-tos/environment-variables/set-environment-variables/
ENV DEBUG=true 

RUN uv run python manage.py collectstatic --noinput

RUN uv run python manage.py collectstatic --noinput

# run application
CMD ["gunicorn", "config.wsgi", "-b", "0.0.0.0:9000"]