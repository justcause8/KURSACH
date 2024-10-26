from rest_framework.viewsets import GenericViewSet
from rest_framework import viewsets, mixins
from carsales.models import Dealer, DealerCenter, Car, Sale, Customer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg, Max, Min
from rest_framework.permissions import IsAuthenticated
from carsales.serializers import (
    DealerSerializer, DealerCenterSerializer,
    CarSerializer, SaleSerializer, CustomerSerializer
)
from rest_framework import serializers

# Базовый ViewSet для создания фильтрации по пользователю
class BaseUserViewSet(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.UpdateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.DestroyModelMixin,
        GenericViewSet
    ):

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            # Если есть фильтрация по пользователю, то применяем её
            user_id = self.request.query_params.get("user_id")
            if user_id:
                qs = qs.filter(user_id=user_id)
        else:
            # Обычные пользователи видят только свои данные
            qs = qs.filter(user=user)
        return qs

# ViewSet для модели Dealer
class DealerViewSet(BaseUserViewSet):
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer
    permission_classes = [IsAuthenticated]

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, *args, **kwargs):
        stats = Dealer.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id"),
        )

        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)

# ViewSet для модели DealerCenter
class DealerCenterViewSet(BaseUserViewSet):
    queryset = DealerCenter.objects.all()
    serializer_class = DealerCenterSerializer

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, *args, **kwargs):
        stats = DealerCenter.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id"),
        )

        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)

# ViewSet для модели Car
class CarViewSet(BaseUserViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, *args, **kwargs):
        stats = Car.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id"),
        )

        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)

# ViewSet для модели Customer
class CustomerViewSet(BaseUserViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, *args, **kwargs):
        stats = Customer.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id"),
        )

        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)

# ViewSet для модели Sale
class SaleViewSet(BaseUserViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, *args, **kwargs):
        stats = Sale.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id"),
        )

        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)