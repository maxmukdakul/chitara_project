# Chitara - AI Music Generation App (Domain Layer)

This repository contains the Django domain layer implementation for **Chitara**, an AI music generation web application. This project focuses strictly on the core business entities and database persistence as outlined in the system requirements.

## Domain Model Justification (Design Decisions)
This implementation translates the provided Domain Model into Django ORM models following these specific design decisions:

* **Core Entities:** The main domain classes (`User`, `Song`, `Notification`) were implemented as standard Django models.
* **Value Types (Enumerations):** Attributes that represent fixed, predefined sets (`Mood`, `Genre`, `VoiceType`, `Occasion`, `GenerateStatus`, `NotificationType`) were implemented using Django's `models.TextChoices` to enforce data integrity at the database level.
* **Relationships & Rules:**
    * **User & Song Lifecycle:** A `ForeignKey` was used on the `Song` model to link it to a `User`, enforcing the rule that each song belongs to exactly one user. Additionally, `SongGenerationRequest` was merged into the `Song` model to reflect that the generation input and the generated output belong to the same lifecycle entity.
    * **Notifications:** A `ForeignKey` was used on the `Notification` model to associate it with a `User`, allowing the system to properly record user actions (generation success/fail, delete, share, download).
    * **Playback:** Playback ("plays") is treated as a simple association rather than a stored database model because no playback history is stored in the system.
* **System Exclusions:** UI components, technical implementations, and external systems (like Google OAuth) were intentionally excluded from the domain models to keep the focus strictly on the business core.

---

# Setup & Installation
## git clone
```cmd
git clone https://github.com/maxmukdakul/chitara_project.git
```
```cmd
cd chitara_project
```

## create venv
```cmd
python -m venv venv
```
## Activate the virtual environment
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```
   - **Windows:**
     ```cmd
     .\venv\Scripts\activate
     ```

## install dependencies
```cmd
pip install -r requirements.txt
```

## apply Database Migrations
```cmd
python manage.py makemigrations domain
```
```
python manage.py migrate
```

## create an admin superuser
```cmd
python manage.py createsuperuser
```

## run
```cmd
python manage.py runserver
```

## go to
http://127.0.0.1:8000/admin/


# Exercise 4: Strategy Pattern (Song Generation)

This phase of the project implements the Strategy Design Pattern to support multiple interchangeable song generation behaviors without altering the core domain logic

## 1. Environment Setup & Security
To run the generation strategies, you must create a `.env` file in the root directory (next to `manage.py`).

Create your `.env` file with this structure:
```python
GENERATOR_STRATEGY=mock
SUNO_API_KEY=your_real_api_key_here
```

## 2. How to Run Mock Mode
The Mock strategy simulates song generation locally. It is deterministic and does not call any external APIs .

### Open your .env file and set:    
```
GENERATOR_STRATEGY=mock.
```
### Open the terminal and launch the Django shell: python 
```
manage.py shell
```

Paste the Demonstration Script 
```
from domain.models import Song, User
from domain.generation.factory import get_generator_strategy

# 1. Setup a dummy user and song request
user = User.objects.first()
song = Song.objects.create(user=user, title="Test Strategy Song", genre="Pop", mood="Happy", occasion="Party")

# 2. Load the active strategy (automatically determined by .env)
generator = get_generator_strategy()

# 3. Generate the song task (creates task ID)
print(generator.generate(song))

# 4. Verify the task ID and status saved in the database
song.refresh_from_db()
print(f"Task ID: {song.task_id}")
print(f"Status: {song.generation_status}")

# 5. Poll the API for status updates (e.g., PENDING, SUCCESS)
print(generator.check_status(song))
```

### this is the example output of mock
![alt text](image-1.png)

## 3. How to Run Suno API Mode
The Suno strategy integrates with SunoApi.org to trigger live AI music generation tasks using Bearer Token authentication.

### Open your .env file and set: 
```
GENERATOR_STRATEGY=suno
```

### Add your valid Suno API Token: 
```python
# you can go find the token at https://sunoapi.org/ (you have to login this first)
# then go to https://sunoapi.org/api-key and then go to API Key page and get it amd paste it instead <your_token>
SUNO_API_KEY=<your_token>
```

### Open the terminal and launch the Django shell: 
```
python manage.py shell
```

### Paste the Demonstration Script
```
from domain.models import Song, User
from domain.generation.factory import get_generator_strategy

# 1. Setup a dummy user and song request
user = User.objects.first()
song = Song.objects.create(user=user, title="Test Strategy Song", genre="Pop", mood="Happy", occasion="Party")

# 2. Load the active strategy (automatically determined by .env)
generator = get_generator_strategy()

# 3. Generate the song task (creates task ID)
print(generator.generate(song))

# 4. Verify the task ID and status saved in the database
song.refresh_from_db()
print(f"Task ID: {song.task_id}")
print(f"Status: {song.generation_status}")

# 5. Poll the API for status updates (e.g., PENDING, SUCCESS)
print(generator.check_status(song))
```

![alt text](image.png)
