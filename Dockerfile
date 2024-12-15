FROM python:3.13-alpine

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

COPY ./src/ /app/

RUN apk update && \
    apk add --no-cache \
        gcc \
        python3-dev && \
    pip install poetry==1.7.1 && \
    pip install gunicorn && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root --only main && \
    rm -rf /root/.cache/pip && \
    rm -rf /root/.cache/poetry

CMD ["gunicorn", "-b", "0.0.0.0:8000", "infrastructure.project.wsgi:application"]

EXPOSE 8000
