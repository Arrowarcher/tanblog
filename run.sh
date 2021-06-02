#!/bin/sh
mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.bak
nginx
python3 manage.py migrate
python3 manage.py collectstatic --noinput
gunicorn tanblog.wsgi:application -w 2 -k gthread -b 0.0.0.0:8080 --chdir=/app