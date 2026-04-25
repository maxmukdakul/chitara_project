from django.db import models

class Occasion(models.TextChoices):
    BIRTHDAY = 'Birthday', 'Birthday'
    WEDDING = 'Wedding', 'Wedding'
    PARTY = 'Party', 'Party'