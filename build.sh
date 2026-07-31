#!/usr/bin/env bash
set -o errexit

# Устанавливаем зависимости
pip install -r requirements.txt

# Собираем статику (CSS, JS)
python manage.py collectstatic --no-input

# Применяем миграции (создаем таблицы в БД)
python manage.py migrate
