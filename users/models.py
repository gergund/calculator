from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Results(models.Model):
    nickname = models.ForeignKey(User, db_column="user", on_delete=models.CASCADE)
    time = models.CharField(max_length=100)
    score = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nickname} ({self.time})"