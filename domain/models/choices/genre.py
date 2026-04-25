from django.db import models

class Genre(models.TextChoices):
    POP = 'Pop', 'Pop'
    ROCK = 'Rock', 'Rock'
    LOFI = 'Lofi', 'Lofi'
    ROMANTIC = 'Romantic', 'Romantic'
    ENERGETIC = 'Energetic', 'Energetic'