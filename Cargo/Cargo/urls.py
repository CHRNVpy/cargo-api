"""
URL configuration for Cargo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from delivery.views import LocationsListAPIView, CreateCargoAPIView, CargoListAPIView, CargoDetailAPIView, CarUpdateView, \
    CargoUpdateView, CargoDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/cargo_add/', CreateCargoAPIView.as_view(), name='create-cargo'),
    path('api/locations/', LocationsListAPIView.as_view(), name='locations-list'),
    path('api/cargo_list/', CargoListAPIView.as_view(), name='cargo-list'),
    path('api/cargo/<int:cargo_id>/', CargoDetailAPIView.as_view(), name='cargo-detail'),
    path('api/cargo_update/<int:cargo_id>/', CargoUpdateView.as_view(), name='cargo-update-weight-description'),
    path('api/cargo_delete/<int:cargo_id>/', CargoDeleteView.as_view(), name='cargo-delete'),
    path('api/car_update/<int:car_id>/', CarUpdateView.as_view(), name='car-update-location'),

]
