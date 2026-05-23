from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    favorite_position = models.CharField(max_length=20, blank=True)
    height = models.FloatField(null=True, blank=True)

    total_made_shots = models.IntegerField(default=0)
    total_attempts = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
