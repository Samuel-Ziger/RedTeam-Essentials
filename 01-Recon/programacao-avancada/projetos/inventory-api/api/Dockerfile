FROM python:3.14-slim@sha256:51dafde81dbdb6ebde285137a295cf18a47ca95234fe388a343719cb97305b3d

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --requirement /app/requirements.txt \
    && useradd --create-home --uid 10001 app

COPY src /app/src

USER 10001:10001
EXPOSE 8000

CMD ["uvicorn", "inventory_api.main:app", "--app-dir", "/app/src", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]
