from django.urls import path, include
from core.views import *
from admin.views import assign_role

urlpatterns = [
    path('register/', register, name='register'),
    path('activate/<uidb64>/<token>/', active_account, name='activate'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='user_logout'),
    path("reset-password/", UserPasswordResetView.as_view(), name="password_reset"),
    path("reset-password/confirm/<uidb64>/<token>/", UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),

    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", EditProfileView.as_view(), name="edit_profile"),
    path("profile/change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("profile/change/done/", ChangePasswordDone.as_view(), name="password_change_done"),
    
    # Dashboard Nested URLs
    path('dashboard/', include([
        path('', dashboard_view, name='dashboard'),
        path('events/approve/<int:event_id>/', approve_event, name='approve_event'),
        
        path('categories/', category_read, name="category_read"),
        path("categories/create/", category_create, name="category_create"),
        path("categories/update/<int:id>/", category_update, name="category_update"),
        path("categories/delete/<int:id>/", category_delete, name="category_delete"),

        path('events/manage/', ManageEvents.as_view(), name="manage_events"),
        path('events/create/', EventCreate.as_view(), name="event_create"),
        path('events/delete/<int:id>/', EventDelete.as_view(), name="event_delete"),
        path('events/update/<int:id>/', Event_update.as_view(), name="event_update"),
        
        path('users/', user_list, name='user_list'),
        path('users/assign-role/<int:user_id>/', assign_role, name='assign_role'),
    ])),

    path('eventlist/', EventRead.as_view(), name="eventlist"),
    path("event/<int:id>/", Event_detail.as_view(), name="event_detail"),
    path('join_event/<int:event_id>/', join_event, name='join_event'),
    path('leave_event/<int:event_id>/', leave_event, name='leave_event'),

    path('', event_home, name="home")
]
