from django.core.management.base import BaseCommand

import random
import string

from delivery.models import Location, Car


class Command(BaseCommand):
    help = 'Generates random cars'

    def add_arguments(self, parser):
        parser.add_argument('cars_count', type=int, help='Number of cars to generate')

    def handle(self, *args, **options):
        cars_count = options['cars_count']
        self.import_location_data(cars_count)

    def import_location_data(self, cars_count):
        for i in range(cars_count):
            number = random.randint(1000, 9999)
            letter = random.choice(string.ascii_uppercase)
            unique_number = str(number) + letter
            location_id = random.randint(1, 33788)  # location id from range of ids
            payload_capacity = random.randint(1, 1000)

            car = Car(
                unique_number=unique_number,
                current_location=Location.objects.get(id=location_id),
                payload_capacity=payload_capacity
            )

            car.save()

        self.stdout.write(self.style.SUCCESS('Cars created successfully.'))
