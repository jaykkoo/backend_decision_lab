from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = "Generate products and product views"

    def add_arguments(self, parser):
        parser.add_argument(
            "--total_products",
            type=int,
            default=1000000,
            help="Total number of products to generate",
        )

    def handle(self, *args, **options):
        total_products = options["total_products"]

        products = []
        for i in range(total_products):
            products.append(Product(name=f"Product_{i}"))

        Product.objects.bulk_create(products, batch_size=1000)
        self.stdout.write(
            self.style.SUCCESS(f"✅ Generated {total_products} products")
        )

