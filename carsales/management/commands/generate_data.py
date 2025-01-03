from django.core.management.base import BaseCommand
from faker import Faker
from carsales.models import Dealer, DealerCenter, Car, Customer, Sale
from django.contrib.auth.models import User
from random import choice
import random
from datetime import datetime

class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])

        # Создание пользователей
        users = []
        for _ in range(20):
            user = User.objects.create_user(username=fake.user_name(), password="password123")
            users.append(user)

        city_names = ["Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань", 
                      "Нижний Новгород", "Челябинск", "Самара", "Омск", "Ростов-на-Дону", 
                      "Уфа", "Красноярск", "Пермь", "Воронеж", "Волгоград"]

        # Создание дилеров
        dealer_name = ["Toyota", "Subaru", "Honda",  "Ford", "Chevrolet", "Nissan", "Hyundai", "Kia", "Volkswagen", "Mazda" ]
        dealers = []
        for _ in range(20):
            choise_name = choice(dealer_name)
            city = choice(city_names)
            dealer = Dealer.objects.create(
                name=choise_name,
                headquarters_location=f"г. {city}",
                user=choice(users)
            )
            dealers.append(dealer)

        # Создание дилерских центров
        dealer_centers = []
        for _ in range(20):
            dealer_center = DealerCenter.objects.create(
                dealer_FK=choice(dealers),
                headquarters_location=f"г. {fake.city()}, ул. {fake.street_name()}, {fake.building_number()}",
                contact=f"+7 ({random.randint(300, 999)}) {random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}",
                manager=fake.name(),
                user=choice(users)
            )
            dealer_centers.append(dealer_center)

        # Словарь с брендами и моделями
        car_brands_models = {
            "Toyota": ["Camry", "Corolla", "RAV4", "Highlander", "Yaris"],
            "Subaru": ["Impreza", "Forester", "Outback", "Legacy", "XV"],
            "Honda": ["Civic", "Accord", "CR-V", "Fit", "Pilot", "HR-V", "Ridgeline", "Insight", "Odyssey", "Element"],
            "Ford": ["F-150", "Escape", "Explorer", "Mustang", "Focus"],
            "Chevrolet": ["Silverado", "Equinox", "Malibu", "Tahoe", "Camaro"],
            "Nissan": ["Altima", "Sentra", "Rogue", "Murano", "Pathfinder"],
            "Hyundai": ["Sonata", "Elantra", "Tucson", "Santa Fe", "Kona"],
            "Kia": ["Optima", "Sorento", "Sportage", "Forte", "Soul"],
            "Volkswagen": ["Golf", "Passat", "Jetta", "Tiguan", "Beetle"],
            "Mazda": ["Mazda3", "Mazda6", "CX-5", "CX-30", "MX-5 Miata"],
        }

         # Создание автомобилей
        cars = []
        for dealer in dealers:
            dealer_name = dealer.name
            if dealer_name in car_brands_models:
                brand_models = car_brands_models[dealer_name]
                for _ in range(20):
                    model = choice(brand_models)
                    year = random.randint(2010, 2024)
                    car = Car.objects.create(
                        dealer_center_FK=choice(dealer_centers),
                        dealer_FK=dealer,
                        car_model=model,
                        year=str(year),
                        price=str(fake.random_int(min=800000, max=3000000)),
                        user=choice(users)
                    )
                    cars.append(car)

        # Создание клиентов
        customers = []
        for _ in range(20):
            customer = Customer.objects.create(
                car_FK=choice(cars),
                name=fake.name(),
                contact_info=fake.phone_number(),
                user=choice(users)
            )
            customers.append(customer)

        # Создание продаж
        for _ in range(20):
            # Генерация даты продажи (не раньше 2023 года)
            sale_date = fake.date_between(start_date=datetime(2023, 1, 1), end_date=datetime(2024, 10, 26))
            
            Sale.objects.create(
                car_FK=choice(cars),
                customer_FK=choice(customers),
                sale_data=sale_date,  # Устанавливаем дату продажи
                sale_price=str(fake.random_int(min=800000, max=3000000)),
                user=choice(users)
            )



        self.stdout.write(self.style.SUCCESS("Записи для каждой модели успешно сгенерированы!"))

        # # Удаляем все записи
        # Dealer.objects.all().delete()
        # DealerCenter.objects.all().delete()
        # Car.objects.all().delete()
        # Customer.objects.all().delete()
        # Sale.objects.all().delete()

        # print("Все записи в таблицах Dealer, DealerCenter, Car, Customer, и Sale были успешно удалены.")

        # users_to_delete = User.objects.exclude(username__in=["dmitr", "user2"])
        # users_to_delete.delete()
        # self.stdout.write(self.style.SUCCESS("Все пользователи, кроме 'dmitr' и 'user2', были удалены."))