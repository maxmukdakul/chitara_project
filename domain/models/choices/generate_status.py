from django.db import models

class GenerateStatus(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    SUCCESS = 'Success', 'Success'
    FAIL = 'Fail', 'Fail'