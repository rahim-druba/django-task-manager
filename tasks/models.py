from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Priority(models.Model):
    label = models.CharField(max_length=50, unique=True)
    level = models.PositiveSmallIntegerField(unique=True)

    class Meta:
        ordering = ["level"]
        verbose_name_plural = "Priorities"

    def __str__(self):
        return f"{self.label} (L{self.level})"


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="tasks")
    priority = models.ForeignKey(Priority, on_delete=models.PROTECT, related_name="tasks")
    deadline = models.DateField() #stores only date, not time
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["is_completed", "deadline", "-created_at"]

    def __str__(self):
        return self.title
