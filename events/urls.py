from django.contrib import admin
from django.urls import path, include
from events.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('eventlist/', event_read, name="eventlist"),
    path("categorylist/", category_read, name="category_read"),
    path("categories_create/", category_create, name="category_create"),
    path("categories_update/<int:id>", category_update, name="category_update"),
    path("categories_delete/<int:id>", category_delete, name="category_delete"),
    path("participentlist", participent_read, name="participent_read"),
    path('', event_home)
]