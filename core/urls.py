from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='user_logout'),
    path('dashboard/', role_dash, name='dashboard'),
    path('admindashboard/', admin_dash, name='admin_dashboard'),
    
    path("categorylist/", category_read, name="category_read"),
    path("categories_create/", category_create, name="category_create"),
    path("categories_update/<int:id>", category_update, name="category_update"),
    path("categories_delete/<int:id>", category_delete, name="category_delete"),

    path('eventlist/', event_read, name="eventlist"),
    path('event_create/', event_create, name="event_create"),
    path('event_delete/<int:id>', event_delete, name="event_delete"),
    path('event_update/<int:id>', event_update, name="event_update"),
    path("event/<int:id>/", event_detail, name="event_detail"),


    path("participentlist", participent_read, name="participent_read"),
    path("participent_create", participent_create, name="participent_create"),
    path('participent_delete/<int:id>', participen_delete, name="paricipent_delete"),
    path('participent_update/<int:id>', participent_update, name="participent_update"),

    path('', event_home, name="home")
]
