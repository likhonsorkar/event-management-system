from django.urls import path
from core.views import *
from admin.views import assign_role

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='user_logout'),
    
    path('dashboard/', role_dash, name='dashboard'),
    path('admindashboard/', admin_dashboard, name='admin_dashboard'),
    path('organizerdashboard/', organizer_dashboard, name='organizer_dashboard'),
    path('participantdashboard/', participant_dashboard, name='participant_dashboard'),
    
    path("categorylist/", category_read, name="category_read"),
    path("categories_create/", category_create, name="category_create"),
    path("categories_update/<int:id>", category_update, name="category_update"),
    path("categories_delete/<int:id>", category_delete, name="category_delete"),

    path('eventlist/', event_read, name="eventlist"),
    path('event_create/', event_create, name="event_create"),
    path('event_delete/<int:id>', event_delete, name="event_delete"),
    path('event_update/<int:id>', event_update, name="event_update"),
    path("event/<int:id>/", event_detail, name="event_detail"),
    path('join_event/<int:event_id>/', join_event, name='join_event'),
    path('leave_event/<int:event_id>/', leave_event, name='leave_event'),

    path('user_list/', user_list, name='user_list'),
    path('assign_role/<int:user_id>/', assign_role, name='assign_role'),

    path('', event_home, name="home")
]
