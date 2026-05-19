from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class TrainingSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    start_time = models.DateTimeField(auto_now_add=True)

    end_time = models.DateTimeField(null=True, blank=True)

    total_shots = models.IntegerField(default=0)

    made_shots = models.IntegerField(default=0)

    @property
    def shooting_percentage(self):
        if self.total_shots == 0:
            return 0

        return round((self.made_shots / self.total_shots) * 100, 2)

    def __str__(self):
        return f"{self.user.username} - {self.start_time}"


class Shot(models.Model):
    training_session = models.ForeignKey(
        TrainingSession,
        on_delete=models.CASCADE,
        related_name='shots'
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    made = models.BooleanField(default=False)

    def __str__(self):
        return f"Shot - {'Made' if self.made else 'Missed'}"
