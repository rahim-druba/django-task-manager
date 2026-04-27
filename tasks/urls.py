from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("tasks/", views.task_list, name="task_list"),
    path("tasks/create/", views.task_create, name="task_create"),
    path("tasks/<int:task_id>/", views.task_detail, name="task_detail"),
    path("tasks/<int:task_id>/update/", views.task_update, name="task_update"),
    path("tasks/<int:task_id>/delete/", views.task_delete, name="task_delete"),
    path("categories/", views.category_list, name="category_list"),
]
