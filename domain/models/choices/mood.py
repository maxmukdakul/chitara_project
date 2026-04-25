from django.db import models

class Mood(models.TextChoices):
    HAPPY = 'Happy', 'Happy'
    SAD = 'Sad', 'Sad'
    CHILL = 'Chill', 'Chill'
    ROMANTIC = 'Romantic', 'Romantic'
    ENERGETIC = 'Energetic', 'Energetic'