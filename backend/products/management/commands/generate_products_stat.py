import random
from django.core.management.base import BaseCommand
from products.models import ProductView, Product
from users.models import User

class Command(BaseCommand):
    help = "Generate product views"

    def handle(self, *args, **options):
        user_ids = list(User.objects.values_list("id", flat=True))
        product_ids = list(Product.objects.values_list("id", flat=True))

        views = []
        seen = set()

        for _ in range(800_000):
            pair = (
                random.choice(product_ids),
                random.choice(user_ids)
            )

            if pair in seen:
                continue

            seen.add(pair)
            views.append(
                ProductView(
                    product_id=pair[0],
                    user_id=pair[1]
                )
            )

        ProductView.objects.bulk_create(views, batch_size=10_000)

        self.stdout.write(
            self.style.SUCCESS(f"✅ Generated {len(views)} product views")
        )
