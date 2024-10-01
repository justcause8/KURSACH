from rest_framework.viewsets import GenericViewSet
from rest_framework import viewsets, mixins
from carsales.models import Dealer, DealerCenter, Car, Sale, Customer

from carsales.serializers import (
    DealerSerializer, DealerCenterSerializer,
    CarSerializer, SaleSerializer, CustomerSerializer
)

# ViewSet для модели Dealer
class DealerViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer

# ViewSet для модели DealerCenter
class DealerCenterViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = DealerCenter.objects.all()
    serializer_class = DealerCenterSerializer

# ViewSet для модели Car
class CarViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

# ViewSet для модели Customer
class CustomerViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


# ViewSet для модели Sale
class SaleViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer