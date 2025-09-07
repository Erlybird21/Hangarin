import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.utils import timezone
from Hangarin_app.models import Category, Priority, Task, SubTask, Note

class Command(BaseCommand):
    help = 'Populates the database with initial and fake data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        # Clear existing data to prevent duplicates
        Note.objects.all().delete()
        SubTask.objects.all().delete()
        Task.objects.all().delete()
        Priority.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write("Creating initial data...")
        # 1. Manually add records for Priority and Category
        priorities_data = ["High", "Medium", "Low", "Critical", "Optional"]
        priorities = [Priority.objects.create(name=p) for p in priorities_data]

        categories_data = ["Work", "School", "Personal", "Finance", "Project"]
        categories = [Category.objects.create(name=c) for c in categories_data]

        self.stdout.write("Creating fake data...")
        # 2. Use faker to generate data
        fake = Faker()
        task_status_choices = ["Pending", "In Progress", "Completed"]
        
        # Create 20 fake tasks
        for _ in range(20):
            task = Task.objects.create(
                title=fake.sentence(nb_words=5).replace('.', ''),
                description=fake.paragraph(nb_sentences=3),
                deadline=timezone.make_aware(fake.date_time_this_month()),
                status=fake.random_element(elements=task_status_choices),
                category=random.choice(categories),
                priority=random.choice(priorities)
            )

            # Create 1-3 subtasks for each task
            for _ in range(random.randint(1, 4)):
                SubTask.objects.create(
                    title=fake.sentence(nb_words=5).replace('.', ''),
                    status=fake.random_element(elements=task_status_choices),
                    task=task
                )

            # Create 0-2 notes for each task
            for _ in range(random.randint(0, 2)):
                Note.objects.create(
                    content=fake.paragraph(nb_sentences=2),
                    task=task
                )

        self.stdout.write(self.style.SUCCESS("Successfully populated the database!"))