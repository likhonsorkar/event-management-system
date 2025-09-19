from django.contrib import admin
from .models import Category, Events, Participant

# Register your models here.
admin.site.register(Category)
admin.site.register(Events)
admin.site.register(Participant)