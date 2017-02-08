python manage.py makemigrations             # Create migrations
python manage.py migrate                    # Apply database migrations
python manage.py collectstatic --noinput    # Collect static files
uwsgi --ini /project/uwsgi.ini
