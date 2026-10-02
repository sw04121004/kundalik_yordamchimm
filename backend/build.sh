#!/usr/bin/env bash
set -o errexit

cd /app/frontend || cd frontend
npm install
npm run build

cd /app/backend || cd backend
pip install -r requirements.txt
python manage.py collectstatic --no-input --clear
python manage.py migrate

gunicorn config.wsgi:application \
    --workers ${WEB_CONCURRENCY:-2} \
    --bind 0.0.0.0:${PORT:-8000}
