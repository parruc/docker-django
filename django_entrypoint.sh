python manage.py makemigrations             # Create migrations
python manage.py migrate                    # Apply database migrations
python manage.py collectstatic --noinput    # Collect static files
python manage.py createsuperuser
uwsgi --ini /project/uwsgi.ini
