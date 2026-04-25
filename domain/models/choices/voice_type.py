from django.db import models

class VoiceType(models.TextChoices):
    MALE = 'Male', 'Male'
    FEMALE = 'Female', 'Female'