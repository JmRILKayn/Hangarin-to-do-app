import os
import django
import random
from faker import Faker
from django.utils import timezone

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectsite.settings')
django.setup()

from hangarin.models import Priority, Category, Task, SubTask, Note

fake = Faker()

def seed_data():
    # 1. Fetch existing Priorities and Categories (Assumes you added them manually)
    priorities = list(Priority.objects.all())
    categories = list(Category.objects.all())

    if not priorities or not categories:
        print("Please add Priorities and Categories via Admin first!")
        return

    print("Seeding Tasks...")
    for _ in range(10):  # Creates 10 tasks
        # Requirements: sentence() for title, paragraph() for description [cite: 1, 96, 97]
        task = Task.objects.create(
            title=fake.sentence(nb_words=5),
            description=fake.paragraph(nb_sentences=3),
            deadline=timezone.make_aware(fake.date_time_this_month()), # Requirement [cite: 1, 42, 44]
            status=fake.random_element(elements=["Pending", "In Progress", "Completed"]), # Requirement [cite: 1, 98, 102]
            priority=random.choice(priorities),
            category=random.choice(categories)
        )

        # 2. Create SubTasks for each Task
        for _ in range(random.randint(1, 3)):
            SubTask.objects.create(
                parent_task=task,
                title=fake.sentence(nb_words=3),
                status=fake.random_element(elements=["Pending", "In Progress", "Completed"])
            )

        # 3. Create a Note for each Task
        Note.objects.create(
            task=task,
            content=fake.paragraph(nb_sentences=2)
        )

    print("Seeding complete!")

if __name__ == '__main__':
    seed_data()