# go to project directory
```cmd
cd chitara_project
```

# create venv
```cmd
python -m venv venv
```
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
```cmd
pip install -r requirements.txt
```

# apply Database Migrations
```cmd
python manage.py makemigrations domain
```
```
python manage.py migrate
```

# create an admin superuser
```cmd
python manage.py createsuperuser
```

# run
```cmd
python manage.py runserver
```

# go to
http://127.0.0.1:8000/admin/
