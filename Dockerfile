

ARG PYTHON_VERSION=3.11.4
FROM python:${PYTHON_VERSION}-slim as base


ENV PYTHONDONTWRITEBYTECODE=1


ENV PYTHONUNBUFFERED=1

WORKDIR /app


ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

COPY requirements.txt ./

RUN python -m pip install -r requirements.txt

USER appuser

COPY . .

EXPOSE 8000

CMD  python main.py
