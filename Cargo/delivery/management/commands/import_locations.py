import csv
from django.core.management.base import BaseCommand
from delivery.models import Location


class Command(BaseCommand):
    help = 'Import locations information from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to the CSV file')

    def handle(self, *args, **options):
        file_path = options['file_path']
        self.import_location_data(file_path)

    def import_location_data(self, file_path):
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[0] == 'zip':
                    continue
                city = row[3]
                state = row[4]
                zip_code = row[0]
                latitude = float(row[1])
                longitude = float(row[2])

                location = Location(
                    city=city,
                    state=state,
                    zip_code=zip_code,
                    latitude=latitude,
                    longitude=longitude
                )

                location.save()

        self.stdout.write(self.style.SUCCESS('Locations data imported successfully.'))
