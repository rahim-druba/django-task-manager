from django.contrib import admin

from .models import Category, Priority, Task


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ("label", "level")
    ordering = ("level",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "priority", "deadline", "is_completed")
    list_filter = ("category", "priority", "is_completed")
    search_fields = ("title", "description")
