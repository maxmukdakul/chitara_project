from django.db import models

# --- Enumerations (Value Types) ---
class Mood(models.TextChoices):
    HAPPY = 'Happy', 'Happy'
    SAD = 'Sad', 'Sad'
    CHILL = 'Chill', 'Chill'
    ROMANTIC = 'Romantic', 'Romantic'
    ENERGETIC = 'Energetic', 'Energetic'

class Genre(models.TextChoices):
    POP = 'Pop', 'Pop'
    ROCK = 'Rock', 'Rock'
    LOFI = 'Lofi', 'Lofi'
    ROMANTIC = 'Romantic', 'Romantic'
    ENERGETIC = 'Energetic', 'Energetic'

class VoiceType(models.TextChoices):
    MALE = 'Male', 'Male'
    FEMALE = 'Female', 'Female'

class Occasion(models.TextChoices):
    BIRTHDAY = 'Birthday', 'Birthday'
    WEDDING = 'Wedding', 'Wedding'
    PARTY = 'Party', 'Party'

class GenerateStatus(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    SUCCESS = 'Success', 'Success'
    FAIL = 'Fail', 'Fail'

class NotificationType(models.TextChoices):
    CREATED_SUCCESS = 'Created success', 'Created success'
    CREATED_FAIL = 'Created fail', 'Created fail'
    DELETED = 'Deleted', 'Deleted'
    SHARED = 'Shared', 'Shared'
    DOWNLOADED = 'Downloaded', 'Downloaded'


# --- Domain Classes ---

class User(models.Model):
    name = models.CharField(max_length=255) # [cite: 37]
    email = models.EmailField(unique=True) # [cite: 38]
    daily_generate_count = models.IntegerField(default=0) # [cite: 43]
    last_generate_date = models.DateField(null=True, blank=True) # [cite: 47]

    def __str__(self):
        return self.name

class Song(models.Model):
    # Relationship: Each Song belongs to exactly one User. [cite: 17]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='songs')
    
    title = models.CharField(max_length=255)
    occasion = models.CharField(max_length=50, choices=Occasion.choices)
    genre = models.CharField(max_length=50, choices=Genre.choices)
    voice_type = models.CharField(max_length=50, choices=VoiceType.choices)
    mood = models.CharField(max_length=50, choices=Mood.choices)
    duration_time = models.DurationField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    generation_status = models.CharField(max_length=50, choices=GenerateStatus.choices, default=GenerateStatus.PENDING)
    task_id = models.CharField(max_length=255, blank=True, null=True)
    shared_link = models.URLField(max_length=500, blank=True, null=True)
    
    # Optional Fields
    story_text = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} by {self.user.name}"

class Notification(models.Model):
    # Relationship: Notification records user actions [cite: 21]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    action_type = models.CharField(max_length=50, choices=NotificationType.choices) # [cite: 39]
    message = models.TextField() # [cite: 42]
    timestamp = models.DateTimeField(auto_now_add=True) # [cite: 44]

    def __str__(self):
        return f"{self.get_action_type_display()} - {self.user.name}"