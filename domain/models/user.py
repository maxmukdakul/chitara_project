from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255) 
    email = models.EmailField(unique=True) 
    daily_generate_count = models.IntegerField(default=0) 
    last_generate_date = models.DateField(null=True, blank=True) 

    def __str__(self):
        return self.name