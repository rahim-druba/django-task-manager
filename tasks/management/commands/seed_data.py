from datetime import date, timedelta

from django.core.management.base import BaseCommand

from tasks.models import Category, Priority, Task


class Command(BaseCommand):
    help = "Insert sample categories, priorities, and tasks."

    def handle(self, *args, **options):
        categories = [
            Category.objects.get_or_create(name="Study")[0],
            Category.objects.get_or_create(name="Personal")[0],
            Category.objects.get_or_create(name="Work")[0],
        ]

        priorities = [
            Priority.objects.get_or_create(label="Low", level=1)[0],
            Priority.objects.get_or_create(label="Medium", level=2)[0],
            Priority.objects.get_or_create(label="High", level=3)[0],
        ]

        sample_tasks = [
            ("Finish Django assignment", "Complete models, views, templates and test.", categories[0], priorities[2], 2),
            ("Prepare presentation", "Create simple slides for class demo.", categories[0], priorities[1], 4),
            ("Buy groceries", "Milk, bread, rice, and vegetables.", categories[1], priorities[0], 1),
            ("Clean workspace", "Organize notes and desk before weekend.", categories[1], priorities[0], 5),
            ("Reply to internship email", "Send updated CV and availability.", categories[2], priorities[2], 3),
        ]

        created_count = 0
        for title, description, category, priority, days_from_now in sample_tasks:
            _, created = Task.objects.get_or_create(
                title=title,
                defaults={
                    "description": description,
                    "category": category,
                    "priority": priority,
                    "deadline": date.today() + timedelta(days=days_from_now),
                    "is_completed": False,
                },
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed complete. Categories: {Category.objects.count()}, "
                f"Priorities: {Priority.objects.count()}, Tasks: {Task.objects.count()}, "
                f"New tasks added: {created_count}."
            )
        )
