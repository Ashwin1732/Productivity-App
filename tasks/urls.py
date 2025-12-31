from django.urls import path
from . import views


urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("add/", views.add_task, name="add_task"),
    path("toggle/<int:task_id>/", views.toggle_task, name="toggle_task"),
]


