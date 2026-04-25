from django.db import models
from .user import User
from .choices.occasion import Occasion
from .choices.genre import Genre
from .choices.voice_type import VoiceType
from .choices.mood import Mood
from .choices.generate_status import GenerateStatus

class Song(models.Model):
    # Relationship: Each Song belongs to exactly one User.
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

    # Metadata fields for the Final Project
    audio_url = models.URLField(max_length=500, blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.title} by {self.user.name}"