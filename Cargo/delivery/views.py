from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cargo, Location, Car
from .serializers import CargoSerializer, LocationSerializer, CargoDataSerializer, CarSerializer, CarSerializerEditor, \
    CargoSerializerEditor
from geopy import distance


class CreateCargoAPIView(APIView):
    def post(self, request):
        pick_up_zip = str(request.query_params.get('pick_up_location'))
        delivery_zip = str(request.query_params.get('delivery_location'))
        weight = request.query_params.get('weight')
        description = request.query_params.get('description')

        # Get the pick-up location
        try:
            pick_location = Location.objects.get(zip_code=pick_up_zip)
        except Location.DoesNotExist:
            pick_location = None

        # Get the delivery location
        try:
            delivery_location = Location.objects.get(zip_code=delivery_zip)
        except Location.DoesNotExist:
            delivery_location = None

        # Create the cargo
        serializer = CargoSerializer(data=request.query_params)
        if serializer.is_valid():
            serializer.save(pick_up_location=pick_location, delivery_location=delivery_location,
                            weight=weight, description=description)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocationsListAPIView(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class CargoListAPIView(generics.ListAPIView):
    serializer_class = CargoDataSerializer

    def get_queryset(self):
        # Retrieve the weight and miles parameters from the request
        weight = self.request.query_params.get('weight', None)
        miles_to_cars = self.request.query_params.get('miles_to_cars', None)

        cargos = Cargo.objects.all()
        cars = Car.objects.all()
        cargo_ids = list(cargos.values_list('pick_up_location_id', flat=True))
        car_ids = list(cars.values_list('current_location_id', flat=True))
        locations = Location.objects.filter(id__in=set(cargo_ids + car_ids))

        cargo_locations = {location.id: (location.latitude, location.longitude) for location in locations if
                           location.id in cargo_ids}
        car_locations = {location.id: (location.latitude, location.longitude) for location in locations if
                         location.id in car_ids}

        cargo_info = []
        for cargo in cargos:
            cargo_location = cargo_locations.get(cargo.pick_up_location_id)
            if cargo_location is None:
                continue

            cars_list = []
            for car in cars:
                car_location = car_locations.get(car.current_location_id)
                if car_location is None:
                    continue

                # Check if the car's distance is within the specified miles
                if miles_to_cars is not None:
                    if distance.distance(cargo_location, car_location).miles > float(miles_to_cars):
                        continue
                    else:
                        cars_list.append(car)
                else:
                    if distance.distance(cargo_location, car_location).miles <= 450:
                        cars_list.append(car)

            cargo_data = {
                'cargo': {'id': cargo.id,
                          'pick_up_location': cargo.pick_up_location,
                          'delivery_location': cargo.delivery_location},
                # Include other cargo fields as needed
                'nearest_cars': len(cars_list),
            }

            # Check if the cargo's weight is within the specified weight
            if weight is not None:
                if cargo.weight > float(weight):
                    continue

            cargo_info.append(cargo_data)

        return cargo_info


class CargoDetailAPIView(APIView):
    def get(self, request, cargo_id):
        cargo = get_object_or_404(Cargo, id=cargo_id)

        pick_up_location = cargo.pick_up_location
        delivery_location = cargo.delivery_location
        pick_up_location = LocationSerializer(pick_up_location).data
        delivery_location = LocationSerializer(delivery_location).data
        weight = cargo.weight
        description = cargo.description

        cars = Car.objects.all()
        cars_list = []

        for car in cars:
            car_location = (Location.objects.get(id=car.current_location_id).latitude,
                            Location.objects.get(id=car.current_location_id).longitude)
            cargo_location = (pick_up_location['latitude'], pick_up_location['longitude'])
            distance_to_cargo = distance.distance(car_location, cargo_location).miles
            cars_list.append({'car_id': car.id, 'car_number': car.unique_number,
                              'distance_to_cargo': distance_to_cargo})

        cargo_info = {
            'pick_up_location': pick_up_location,
            'delivery_location': delivery_location,
            'weight': weight,
            'description': description,
            'nearest_cars': cars_list,
        }

        return Response(cargo_info, status=status.HTTP_200_OK)


class CarUpdateView(APIView):
    def put(self, request, car_id):
        try:
            car = Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            return Response({'error': 'Car not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CarSerializerEditor(car, data=request.query_params, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CargoUpdateView(APIView):
    def put(self, request, cargo_id):
        try:
            car = Cargo.objects.get(id=cargo_id)
        except Cargo.DoesNotExist:
            return Response({'error': 'Cargo not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CargoSerializerEditor(car, data=request.query_params, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CargoDeleteView(APIView):
    def delete(self, request, cargo_id):
        try:
            cargo = Cargo.objects.get(id=cargo_id)
        except Cargo.DoesNotExist:
            return Response({'error': 'Cargo not found'}, status=status.HTTP_404_NOT_FOUND)

        cargo.delete()
        return Response({'message': 'Cargo deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
