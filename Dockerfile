FROM node:20 AS frontend-builder
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim
WORKDIR /app/backend

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./
RUN rm -rf static/frontend
COPY --from=frontend-builder /app/backend/static/frontend ./static/frontend

RUN SECRET_KEY=build-only-placeholder python manage.py collectstatic --no-input --clear
EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && exec gunicorn config.wsgi:application --workers ${WEB_CONCURRENCY:-2} --bind 0.0.0.0:${PORT:-8000}"]
