from django.urls import path
from core.views import *
from admin.views import assign_role

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='user_logout'),
    path("reset-password/", UserPasswordResetView.as_view(), name="password_reset"),
    path("reset-password/done/", UserPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset-password/confirm/<uidb64>/<token>/", UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset-password/complete/", UserPasswordResetCompleteView.as_view(), name="password_reset_complete"),

    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", EditProfileView.as_view(), name="edit_profile"),
    path("profile/change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("profile/change/done/", ChangePasswordDone.as_view(), name="password_change_done"),
    
    path('dashboard/', role_dash, name='dashboard'),
    path('admindashboard/', admin_dashboard, name='admin_dashboard'),
    path('organizerdashboard/', organizer_dashboard, name='organizer_dashboard'),
    path('participantdashboard/', participant_dashboard, name='participant_dashboard'),
    
    path("categorylist/", category_read, name="category_read"),
    path("categories_create/", category_create, name="category_create"),
    path("categories_update/<int:id>", category_update, name="category_update"),
    path("categories_delete/<int:id>", category_delete, name="category_delete"),

    path('eventlist/', EventRead.as_view(), name="eventlist"),
    path('event_create/', EventCreate.as_view(), name="event_create"),
    path('event_delete/<int:id>', EventDelete.as_view(), name="event_delete"),
    path('event_update/<int:id>', Event_update.as_view(), name="event_update"),
    path("event/<int:id>/", Event_detail.as_view(), name="event_detail"),
    path('join_event/<int:event_id>/', join_event, name='join_event'),
    path('leave_event/<int:event_id>/', leave_event, name='leave_event'),

    path('user_list/', user_list, name='user_list'),
    path('assign_role/<int:user_id>/', assign_role, name='assign_role'),

    path('', event_home, name="home")
]
