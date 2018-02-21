release: python manage.py migrate
web: gunicorn -b :$PORT rea_schedule_site.wsgi