from django.db import models

# Create your models here.
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
    def __str__(self):
        return f"{self.name} at {self.location} on {self.date}"
class Participant(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    events = models.ManyToManyField(Events, related_name="participants", blank=True)
    def __str__(self):
        return self.name