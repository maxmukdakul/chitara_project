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

## Setup & Installation
# git clone
```cmd
git clone https://github.com/maxmukdakul/chitara_project.git
```
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
