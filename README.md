# activate venv
python -m venv venv
venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# Apply Database Migrations
python manage.py makemigrations domain
python manage.py migrate

# create an admin superuser
python manage.py createsuperuser

# run
python manage.py runserver