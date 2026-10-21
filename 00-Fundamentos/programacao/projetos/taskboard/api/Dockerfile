FROM python:3.14-slim@sha256:51dafde81dbdb6ebde285137a295cf18a47ca95234fe388a343719cb97305b3d

LABEL org.opencontainers.image.title="TaskBoard API" \
      org.opencontainers.image.description="API educacional HTTP e SQLite, sem dependências externas"

ENV APP_HOST=0.0.0.0 \
    APP_PORT=8000 \
    APP_DB_PATH=/data/tasks.db

RUN groupadd --gid 10001 app \
    && useradd --uid 10001 --gid app --no-create-home --shell /usr/sbin/nologin app \
    && mkdir -p /app /data \
    && chown -R app:app /app /data

WORKDIR /app
COPY --chown=app:app server.py /app/server.py

# Falha cedo no build se o exemplo Python não puder ser compilado.
RUN python -m py_compile /app/server.py

USER 10001:10001
EXPOSE 8000
STOPSIGNAL SIGTERM
HEALTHCHECK --interval=10s --timeout=3s --start-period=3s --retries=5 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/ready', timeout=2).read()"]
CMD ["python", "-I", "-u", "-B", "/app/server.py"]
