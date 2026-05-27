from django.core.management.base import BaseCommand
from faker import Faker
from hangarinapp.models import Priority, Category, Task, SubTask, Note
from django.utils import timezone

class Command(BaseCommand):
    help = 'Create initial date for the application'

    def handle(self, *args, **kwargs):
        self.create_task(10)
        self.create_notes(15)
        self.create_subtask(10)

    def create_task(self, count):
        fake = Faker()

        for _ in range(count):
            Task.objects.create(
                title = fake.sentence(nb_words=5),
                description = fake.paragraph(nb_sentences=3),
                deadline = timezone.make_aware(fake.date_time_this_month()),
                status = fake.random_element(elements=["Pending", "In Progress", "Completed"]),
                category = Category.objects.order_by('?').first(),
                priority = Priority.objects.order_by('?').first()
            )
        self.stdout.write(self.style.SUCCESS(
            'Inital data for TASK created successfully.'
        ))

    def create_subtask(self, count):
        fake = Faker()

        for _ in range(count):
            SubTask.objects.create(
                parent_task = Task.objects.order_by('?').first(),
                subtask_title = fake.sentence(nb_words=5),
                subtask_status = fake.random_element(elements=["Pending", "In Progress", "Completed"])
            )
        self.stdout.write(self.style.SUCCESS(
                'Initial data for SubTask created successfully.'
            ))
        

    def create_notes(self,count):
        fake = Faker()
        for _ in range(count):
            Note.objects.create(
                task = Task.objects.order_by('?').first(),
                content = fake.paragraph(nb_sentences=3)
            )
        self.stdout.write(self.style.SUCCESS(
            'Intial data for Note created successfully.'
        ))