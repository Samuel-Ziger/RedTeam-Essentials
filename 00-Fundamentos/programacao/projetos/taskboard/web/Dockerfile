FROM nginx:1.29.1-alpine@sha256:42a516af16b852e33b7682d5ef8acbd5d13fe08fecadc7ed98605ba5e3b26ab8

LABEL org.opencontainers.image.title="TaskBoard Gateway" \
      org.opencontainers.image.description="Frontend estático e reverse proxy local do TaskBoard"

RUN rm -f /etc/nginx/conf.d/default.conf \
    && chown -R nginx:nginx /usr/share/nginx/html

COPY --chown=nginx:nginx nginx.conf /etc/nginx/nginx.conf
COPY --chown=nginx:nginx index.html app.js taskboard-core.mjs styles.css /usr/share/nginx/html/

RUN nginx -t \
    && chmod -R a-w /etc/nginx/nginx.conf /usr/share/nginx/html

USER nginx
EXPOSE 8080
STOPSIGNAL SIGQUIT
HEALTHCHECK --interval=10s --timeout=3s --start-period=3s --retries=5 \
    CMD ["wget", "-q", "--spider", "http://127.0.0.1:8080/health"]
