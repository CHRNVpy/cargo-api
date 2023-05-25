from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models


class Location(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.city


class Cargo(models.Model):
    pick_up_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='pick_up_cargos')
    delivery_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='delivery_cargos')
    weight = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(1000)])
    description = models.TextField()

    def __str__(self):
        return f"Cargo {self.description}"


class Car(models.Model):
    unique_number = models.CharField(max_length=5, unique=True, validators=[RegexValidator(regex='^[0-9]{4}[A-Z]$')])
    current_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='cars')
    payload_capacity = models.PositiveIntegerField(default=1,
                                                   validators=[MinValueValidator(1), MaxValueValidator(1000)])

    def __str__(self):
        return f"Car {self.unique_number}"
