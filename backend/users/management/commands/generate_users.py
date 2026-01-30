import random
from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = "Generate users with random ages"

    def add_arguments(self, parser):
        parser.add_argument(
            "--total",
            type=int,
            default=50000,
            help="Total number of users to generate",
        )

    def handle(self, *args, **options):
        total = options["total"]

        users = []
        for i in range(total):
            users.append(
                User(
                    username=f"user_{i}",
                    age=random.randint(18, 80),
                )
            )

        User.objects.bulk_create(users, batch_size=1000)

        self.stdout.write(
            self.style.SUCCESS(f"✅ Generated {total} users")
        )
