from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Parametre_vocal(models.Model):
    text = models.TextField()
    language = models.CharField(max_length=10)
    selected_voice = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request for {self.language} - {self.text[:50]}..."
