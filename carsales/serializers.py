from rest_framework import serializers
from carsales.models import Dealer, DealerCenter, Car, Sale, Customer

# Вложенный сериализатор для модели Dealer
class DealerSerializer(serializers.ModelSerializer):
    def create(self, validated_data): 
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    class Meta:
        model = Dealer
        fields = ['id', 'name', 'headquarters_location', 'picture', 'user']

# Вложенный сериализатор для модели DealerCenter
class DealerCenterSerializer(serializers.ModelSerializer):
    dealer_FK = DealerSerializer(read_only=True)
    dealer_FK_id = serializers.PrimaryKeyRelatedField(queryset=Dealer.objects.all(), write_only=True, source="dealer_FK")

    def create(self, validated_data): 
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = DealerCenter
        fields = ['id', 'headquarters_location', 'contact', 'manager', 'dealer_FK', 'dealer_FK_id', 'user']


# Вложенный сериализатор для модели Car
class CarSerializer(serializers.ModelSerializer):
    dealer_FK = DealerSerializer(read_only=True)
    dealer_FK_id = serializers.PrimaryKeyRelatedField(queryset=Dealer.objects.all(), write_only=True, source="dealer_FK")
    dealer_center_FK = DealerCenterSerializer(read_only=True)
    dealer_center_FK_id = serializers.PrimaryKeyRelatedField(queryset=DealerCenter.objects.all(), write_only=True, source="dealer_center_FK")

    def create(self, validated_data): 
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = Car
        fields = ['id', 'dealer_center_FK', 'dealer_FK', 'dealer_FK_id', 'car_model', 'year', 'price', 'dealer_center_FK_id', 'picture', 'user']

# Вложенный сериализатор для модели Customer
class CustomerSerializer(serializers.ModelSerializer):
    car_FK = CarSerializer(read_only=True)
    car_FK_id = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all(), write_only=True, source="car_FK")

    def create(self, validated_data): 
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = Customer
        fields = ['id', 'car_FK', 'name', 'contact_info', 'car_FK_id', 'user']

# Вложенный сериализатор для модели Sale
class SaleSerializer(serializers.ModelSerializer):
    car_FK = CarSerializer(read_only=True)
    car_FK_id = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all(), write_only=True, source="car_FK")
    customer_FK = CustomerSerializer(read_only=True)
    customer_FK_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), write_only=True, source="customer_FK")

    def create(self, validated_data): 
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = Sale
        fields = ['id', 'car_FK', 'customer_FK', 'sale_data', 'sale_price', 'car_FK_id', 'customer_FK_id', 'user']

