from rest_framework import serializers
from .models import Cargo, Location, Car


class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = '__all__'


class CargoSerializerSpecial(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ['id', 'pick_up_location', 'delivery_location']


class CargoSerializerEditor(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ['weight', 'description']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'


class CarSerializerEditor(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['current_location']


class CargoDataSerializer(serializers.Serializer):
    cargo = CargoSerializerSpecial()
    nearest_cars = serializers.IntegerField()
