from django.core.management.base import BaseCommand

import random

from delivery.models import Location, Cargo


class Command(BaseCommand):
    help = 'Generates randon cargo'

    def add_arguments(self, parser):
        parser.add_argument('cargo_count', type=int, help='Number of cargos to generate')

    def handle(self, *args, **options):
        cargo_count = options['cargo_count']
        self.cargo_generator(cargo_count)

    def cargo_generator(self, cargo_count):
        for i in range(cargo_count):
            pick_up_location = random.randint(1, 33788)  # location id from range of ids
            delivery_location = random.randint(1, 33788)  # location id from range of ids
            weight = random.randint(1, 1000)
            description = random.choice(['Home Decor', 'Toys', 'Appliances', 'Jewelry', 'Musical Instruments',
                                         'Kitchenware', 'Electronics', 'Furniture', 'Cosmetics', 'Automotive Parts',
                                         'Books', 'Sporting Goods', 'Office Supplies', 'Clothing'])

            cargo = Cargo(
                pick_up_location=Location.objects.get(id=pick_up_location),
                delivery_location=Location.objects.get(id=delivery_location),
                weight=weight,
                description=description
            )

            cargo.save()

        self.stdout.write(self.style.SUCCESS('Cargos created successfully.'))
