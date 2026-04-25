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

## Environment Setup & Security
To run the generation strategies, you must create a `.env` file in the root directory (next to `manage.py`).

Create your `.env` file with this structure:
```python
GENERATOR_STRATEGY=mock
# Change to 'suno' to use the real AI generator
SUNO_API_KEY=your_real_api_key_here
```



## How to Test in Postman
To prove both strategies work, start your server by running ```python manage.py runserver``` in your terminal. Leave it running, and open the Postman app.(dont forget to open the venv first)

### Step 1: Create a Domain User (Do this once)
Django superusers do not count as domain users. You must create a user through this API first before generating any songs.

Method: POST

URL: http://127.0.0.1:8000/api/users/

Body (raw JSON):
```
{
    "name": "Testing User4",
    "email": "finaltest999@example.com"
}
```

Send! Make note of the user_id returned (e.g., 1).

### Step 2: Testing MOCK Mode
This mode is offline and simulates a fast generation.

Set up .env: Make sure your .env says ```GENERATOR_STRATEGY=mock```. Restart your Django server if you changed it.

### Generate the Song:

Method: POST

URL: http://127.0.0.1:8000/api/song-forms/

Body (raw JSON):

```
{
    "user_id": 1,
    "title": "Mock Testing Song",
    "occasion": "casual",
    "genre": "pop",
    "mood": "happy"
}
```

Send! It will return a song_id and a mock task ID.

![alt text](image.png)

### Check Status:

Method: GET

URL: http://127.0.0.1:8000/api/song-forms/<your_song_id>/status/

Send! You will immediately see the mock status response confirming it works offline.

![alt text](image-1.png)

### Step 3: Testing SUNO Mode
This mode connects to the real AI and takes a few minutes to render audio.

Set up .env: Change your .env to ```GENERATOR_STRATEGY=suno``` and ensure ```SUNO_API_KEY``` is filled in. Restart your Django server.

### Generate the Song:

Method: POST

URL: http://127.0.0.1:8000/api/song-forms/

Body (raw JSON):

```
{
    "user_id": 1,
    "title": "Morning Vibes",
    "occasion": "casual",
    "genre": "pop",
    "mood": "light and calm"
}
```

Send! It will return a song_id and a status: pending. The AI is now working in the background.(And remember the song_id)

![alt text](image-2.png)

### Check Status (Polling):

Method: GET

URL: http://127.0.0.1:8000/api/song-forms/<your_song_id>/status/

Send! If you check immediately, the Suno API response will say PENDING. Wait about 2-3 minutes and hit Send again. It will eventually change to SUCCESS and return the playable audioUrl links!

![alt text](image-3.png)

![alt text](image-4.png)

### 1. The Domain Model

```mermaid
erDiagram
    USER ||--o{ SONG : "creates / plays"
    USER ||--o{ NOTIFICATION : "receives"
    
    USER {
        String Name
        String Email
        Int Daily_Generate_Count
        Date Last_Generate_Date
    }
    
    SONG {
        String Title
        Occasion Occasion
        Genre Genre
        VoiceType Voice_Type
        Mood Mood
        Duration Duration_Time
        DateTime Created_At
        GenerateStatus GenerationStatus
        String Shared_link
        String Story_Text
        Picture Cover_Image
    }
    
    NOTIFICATION {
        String ActionType
        String Message
        Timestamp Timestamp
    }
```

### 2. The Class Diagram (MVT Architecture)

```mermaid
classDiagram
    %% Models
    class User
    class Song
    class Notification
    
    %% Views & Templates (MVT)
    class Views_API {
        +create_user_api(request)
        +generate_song_api(request)
        +check_song_status_api(request)
    }
    class JSONResponse {
        <<Template Layer>>
    }

    %% Strategy Pattern
    class Factory {
        +get_generator_strategy()
    }
    class SongGeneratorStrategy {
        <<Interface>>
        +generate(song)
        +check_status(song)
    }
    class MockStrategy
    class SunoStrategy

    %% Relationships
    Views_API --> User : reads/writes
    Views_API --> Song : reads/writes
    Views_API --> Notification : logs actions
    Views_API --> JSONResponse : returns as Template
    Views_API --> Factory : asks for strategy
    Factory --> SongGeneratorStrategy : creates
    SongGeneratorStrategy <|.. MockStrategy : implements
    SongGeneratorStrategy <|.. SunoStrategy : implements
```

### 3. The Sequence Diagram

```mermaid
sequenceDiagram
    actor Owner as User (Owner)
    participant View as API View (views.py)
    participant DB as Database (Models)
    participant Factory as Strategy Factory
    participant Strategy as Suno Strategy
    participant Suno as External Suno API

    Owner->>View: POST Form Data (Title, Genre, Mood, etc.)
    View->>DB: Validate User Daily Limit
    View->>DB: Create Song (Status: Pending)
    View->>Factory: get_generator_strategy()
    Factory-->>View: Returns active strategy
    View->>Strategy: generate(song)
    Strategy->>Suno: API Request to Suno
    Suno-->>Strategy: Returns Task ID
    Strategy->>DB: Save Task ID to Song
    View-->>Owner: Return Pending Status & Task ID
    
    Note over Owner, DB: Later Polling for Status...
    Owner->>View: GET /status/
    View->>Strategy: check_status()
    Strategy->>Suno: Fetch generation result
    Suno-->>Strategy: Returns SUCCESS & MP3 URLs
    Strategy->>DB: Update Song to SUCCESS & Save URLs
    View-->>Owner: Return MP3 Links
```
