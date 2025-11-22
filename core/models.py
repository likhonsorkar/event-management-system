from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to="profile/",
        default='default/user.png'
    )

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null= True)
    def __str__(self):
        return self.name

class Events(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="events")
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="organized_events")
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="participated_events", blank=True)

    def __str__(self):
        return f"{self.name} at {self.location} on {self.date}"