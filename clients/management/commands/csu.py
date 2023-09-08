from django.core.management import BaseCommand

from clients.models import Author


class Command(BaseCommand):

    def handle(self, *args, **options):
        author = Author.objects.create(
            email='admin@mail.tu',
            full_name='Sergei Ronaldo',
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        author.set_password('123')
        author.save()