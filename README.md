# create venv
python -m venv venv
# Activate the virtual environment
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```
   - **Windows:**
     ```cmd
     .\venv\Scripts\activate
     ```

# install dependencies
pip install -r requirements.txt

# apply Database Migrations
python manage.py makemigrations domain
python manage.py migrate

# create an admin superuser
python manage.py createsuperuser

# run
python manage.py runserver

# go to
http://127.0.0.1:8000/admin/
