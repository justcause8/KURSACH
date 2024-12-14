from django.contrib import admin

from carsales.models import Dealer, DealerCenter, Car, Sale, Customer

@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'headquarters_location']

@admin.register(DealerCenter)
class DealerCenterAdmin(admin.ModelAdmin):
    list_display = ['id', 'dealer_FK', 'headquarters_location', 'contact', 'manager']

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['id', 'dealer_center_FK', 'dealer_FK', 'car_model', 'year', 'price']

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'car_FK', 'customer_FK', 'sale_data', 'sale_price']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'car_FK', 'name', 'contact_info']