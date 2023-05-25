from django.core.management.base import BaseCommand

import random

from delivery.models import Location, Car


class Command(BaseCommand):
    help = 'Updates car locations'

    def handle(self, *args, **options):
        self.update_car_locations()

    def update_car_locations(self):
        cars = Car.objects.all()
        for car in cars:
            # Update the car's location logic
            new_locations = Location.objects.exclude(id=car.current_location_id).all()
            new_location = random.choice(new_locations)
            car.current_location = new_location
            car.save()

        self.stdout.write(self.style.SUCCESS('Locations updated successfully.'))
