from django.urls import path
from .views import user_list, assign_role

urlpatterns = [
    path("users/", user_list, name="user_list"),
    path("users/assign-role/<int:user_id>/", assign_role, name="assign_role"),
]