from django.db import models

class NotificationType(models.TextChoices):
    CREATED_SUCCESS = 'Created success', 'Created success'
    CREATED_FAIL = 'Created fail', 'Created fail'
    DELETED = 'Deleted', 'Deleted'
    SHARED = 'Shared', 'Shared'
    DOWNLOADED = 'Downloaded', 'Downloaded'