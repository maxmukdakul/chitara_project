from django.db import models
from .user import User
from .choices.notification_type import NotificationType

class Notification(models.Model):
    # Relationship: Notification records user actions
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    action_type = models.CharField(max_length=50, choices=NotificationType.choices) 
    message = models.TextField() 
    timestamp = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.get_action_type_display()} - {self.user.name}"