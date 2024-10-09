from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker
from carsales.models import Dealer, DealerCenter, Car, Sale, Customer

class DealerCRUDTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    # ----- Dealer CRUD -----
    def test_create_dealer(self):
        dealer = baker.make("carsales.Dealer")
        r = self.client.post("/api/dealers/", {
            "name": "Toyota", 
            "headquarters_location": "Москва"
            })


    def test_get_dealer(self):
        dealer = baker.make("carsales.Dealer") # Создаем экземпляр Dealer с помощью baker
        r = self.client.get('/api/dealers/') # Выполняем GET-запрос на эндпоинт /api/dealers/
        data = r.json() # Преобразуем ответ в JSON
        print(data)

        assert dealer.name == data[0]['name'] # Проверка, что имя дилера в ответе совпадает с созданным
        assert dealer.id == data[0]['id'] # Проверка, что идентификатор дилера совпадает с созданным
        assert dealer.headquarters_location == data[0]['headquarters_location'] # Проверка, что местоположение главного офиса дилера совпадает
        assert len(data) == 1 # Проверка количества дилеров в ответе


    def test_update_dealer(self):
        dealer = baker.make(Dealer) # Создаем объект дилера

        r = self.client.get(f"/api/dealers/{dealer.id}/") # Проверка получения исходных данных дилера
        data = r.json()
        assert data['name'] == dealer.name
        assert data['headquarters_location'] == dealer.headquarters_location

        update_data = { # Обновление данных дилера с использованием PUT
            "name": "Nissan",  # Новое имя дилера
            "headquarters_location": dealer.headquarters_location  # Оставляем старое местоположение
        }

        r = self.client.put(f"/api/dealers/{dealer.id}/", update_data) # Выполняем запрос на обновление данных

        updated_data = r.json() # Проверка, что данные дилера обновлены
        assert updated_data['name'] == "Nissan"
        assert updated_data['headquarters_location'] == dealer.headquarters_location

        dealer.refresh_from_db() # Обновляем объект дилера из базы данных и проверяем его обновленные значения
        assert dealer.name == "Nissan"
        assert dealer.headquarters_location == updated_data['headquarters_location']


    def test_delete_dealer(self):
        dealer = baker.make("Dealer", 10)
        r = self.client.get('/api/dealers/')
        data = r.json()
        assert len(data) == 10
                
        dealer_id_to_delete = dealer[3].id
        self.client.delete(f'/api/dealers/{dealer_id_to_delete}/')

        r = self.client.get('/api/dealers/')
        data = r.json()
        assert len(data) == 9

        assert dealer_id_to_delete not in [i['id'] for i in data]


class DealerCenterCRUDTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    # Тест создания дилерского центра
    def test_create_dealer_center(self):
        dealer = baker.make("carsales.Dealer")
    
        # Выполнение POST-запроса на создание дилерского центра
        r = self.client.post("/api/dealer-centers/", {
            "dealer_FK_id": dealer.id, 
            "headquarters_location": "Новосибирск", 
            "contact": "123-456-7890", 
            "manager": "Иван Иванов"
        })
        
        new_dealercenter_id = r.json()['id']

        carsales = DealerCenter.objects.all()
        assert len(carsales) == 1

        new_dealercenter = DealerCenter.objects.filter(id=new_dealercenter_id).first()

        assert new_dealercenter.headquarters_location == 'Новосибирск'
        assert new_dealercenter.contact == '123-456-7890'
        assert new_dealercenter.manager == 'Иван Иванов'
        assert new_dealercenter.dealer_FK == dealer


    # Тест получения списка дилерских центров
    def test_get_dealer_center(self):
        dealer_center = baker.make("carsales.DealerCenter")
        r = self.client.get('/api/dealer-centers/')
        data = r.json()
        
        assert dealer_center.headquarters_location == data[0]['headquarters_location']
        assert dealer_center.id == data[0]['id']
        assert dealer_center.contact == data[0]['contact']
        assert dealer_center.manager == data[0]['manager']
        assert len(data) == 1


    # Тест обновления дилерского центра
    def test_update_dealer_center(self):
        dealercenter = baker.make(DealerCenter)  # Создаем объект дилерского центра

        r = self.client.get(f"/api/dealer-centers/{dealercenter.id}/")  # Проверка получения исходных данных дилерского центра
        data = r.json()
        assert data['headquarters_location'] == dealercenter.headquarters_location
        assert data['contact'] == dealercenter.contact
        assert data['manager'] == dealercenter.manager

        update_data = {  # Обновление данных дилерского центра с использованием PUT
            "headquarters_location": "Владивосток",  # Новое местоположение
            "contact": "987-654-3210",  # Новый контактный номер
            "manager": dealercenter.manager  # Оставляем старое имя управляющего
        }

        # Используем метод PATCH вместо PUT
        r = self.client.patch(f"/api/dealer-centers/{dealercenter.id}/", update_data)  # Выполняем запрос на обновление данных

        updated_data = r.json()  # Проверка, что данные дилерского центра обновлены
        assert updated_data['headquarters_location'] == "Владивосток"
        assert updated_data['contact'] == "987-654-3210"
        assert updated_data['manager'] == dealercenter.manager

        dealercenter.refresh_from_db()  # Обновляем объект дилерского центра из базы данных и проверяем его обновленные значения
        assert dealercenter.headquarters_location == "Владивосток"
        assert dealercenter.contact == "987-654-3210"
        assert dealercenter.manager == updated_data['manager']



    # Тест удаления дилерского центра
    def test_delete_dealer_center(self):
        dealer_centers = baker.make("DealerCenter", 5)  # Создаем 5 дилерских центров
        r = self.client.get('/api/dealer-centers/')
        data = r.json()
        assert len(data) == 5

        dealer_center_id_to_delete = dealer_centers[2].id
        self.client.delete(f'/api/dealer-centers/{dealer_center_id_to_delete}/')

        r = self.client.get('/api/dealer-centers/')
        data = r.json()
        assert len(data) == 4

        assert dealer_center_id_to_delete not in [i['id'] for i in data]


class CarCRUDTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    # Тест создания автомобиля
    def test_create_car(self):
        dealercenter = baker.make("carsales.DealerCenter")
        dealer = baker.make("carsales.Dealer")
    
        r = self.client.post("/api/cars/", {
            "dealer_center_FK_id": dealercenter.id,
            "dealer_FK_id": dealer.id, 
            "car_model": "Civic", 
            "year": "2019",
            "price": "1500000"
        })
        
        new_car_id = r.json()['id']

        carsales = Car.objects.all()
        assert len(carsales) == 1

        new_car = Car.objects.filter(id=new_car_id).first()

        assert new_car.dealer_center_FK == dealercenter
        assert new_car.dealer_FK == dealer
        assert new_car.car_model == 'Civic'
        assert new_car.year == '2019'
        assert new_car.price == '1500000'


    # Тест получения списка автомобилей
    def test_get_car(self):
        car = baker.make("carsales.Car", dealer_FK=baker.make("carsales.Dealer"), dealer_center_FK=baker.make("carsales.DealerCenter"))
        r = self.client.get('/api/cars/')
        data = r.json()

        assert car.dealer_FK.id == data[0]['dealer_FK']['id']
        assert car.dealer_center_FK.id == data[0]['dealer_center_FK']['id']
        assert car.car_model == data[0]['car_model']
        assert car.year == data[0]['year']
        assert car.price == data[0]['price']
        assert len(data) == 1


    # Тест обновления автомобиля
    def test_update_car(self):
        car = baker.make(Car, dealer_FK=baker.make("carsales.Dealer"), dealer_center_FK=baker.make("carsales.DealerCenter"))

        r = self.client.get(f"/api/cars/{car.id}/")
        data = r.json()
        assert data['dealer_FK']['id'] == car.dealer_FK.id
        assert data['dealer_center_FK']['id'] == car.dealer_center_FK.id
        assert data['car_model'] == car.car_model
        assert data['year'] == car.year
        assert data['price'] == car.price

        update_data = {
            "dealer_FK_id": car.dealer_FK.id,
            "dealer_center_FK_id": car.dealer_center_FK.id,
            "car_model": "Civic",
            "year": "2019",
            "price": car.price
        }

        r = self.client.patch(f"/api/cars/{car.id}/", update_data)

        updated_data = r.json()
        assert updated_data['car_model'] == "Civic"
        assert updated_data['year'] == "2019"
        assert updated_data['price'] == car.price

        car.refresh_from_db()
        assert car.car_model == "Civic"
        assert car.year == "2019"
        assert car.price == updated_data['price']


    # Тест удаления автомобиля
    def test_delete_car(self):
        cars = baker.make("carsales.Car", 5, dealer_FK=baker.make("carsales.Dealer"), dealer_center_FK=baker.make("carsales.DealerCenter"))
        r = self.client.get('/api/cars/')
        data = r.json()
        assert len(data) == 5

        car_id_to_delete = cars[2].id
        self.client.delete(f'/api/cars/{car_id_to_delete}/')

        r = self.client.get('/api/cars/')
        data = r.json()
        assert len(data) == 4

        assert car_id_to_delete not in [i['id'] for i in data]



class CustomerCRUDTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    # Тест создания клиента
    def test_create_customer(self):
        car = baker.make("carsales.Car")
    
        r = self.client.post("/api/customers/", {
            "car_FK_id": car.id, 
            "name": "Дмитрий", 
            "contact_info": "+7 (924) 11-22-32"
        })
        
        new_customer_id = r.json()['id']

        carsales = Customer.objects.all()
        assert len(carsales) == 1

        new_customer = Customer.objects.filter(id=new_customer_id).first()

        assert new_customer.name == 'Дмитрий'
        assert new_customer.contact_info == '+7 (924) 11-22-32'
        assert new_customer.car_FK == car


    # Тест получения списка клиентов
    def test_get_customer(self):
        customer = baker.make("carsales.Customer")
        r = self.client.get('/api/customers/')
        data = r.json()
        
        assert customer.name == data[0]['name']
        assert customer.id == data[0]['id']
        assert customer.contact_info == data[0]['contact_info']
        assert len(data) == 1


    # Тест обновления автомобилей
    def test_update_customer(self):
        customer = baker.make(Customer)

        r = self.client.get(f"/api/customers/{customer.id}/")
        data = r.json()
        assert data['name'] == customer.name
        assert data['contact_info'] == customer.contact_info

        update_data = {
            "name": "Дмитрий",
            "contact_info": customer.contact_info
        }

        r = self.client.patch(f"/api/customers/{customer.id}/", update_data)

        updated_data = r.json()
        assert updated_data['name'] == "Дмитрий"
        assert updated_data['contact_info'] == customer.contact_info

        customer.refresh_from_db()
        assert customer.name == "Дмитрий"
        assert customer.contact_info == updated_data['contact_info']


    # Тест удаления клиента
    def test_delete_customer(self):
        customers = baker.make("Customer", 5)
        r = self.client.get('/api/customers/')
        data = r.json()
        assert len(data) == 5

        customer_id_to_delete = customers[2].id
        self.client.delete(f'/api/customers/{customer_id_to_delete}/')

        r = self.client.get('/api/customers/')
        data = r.json()
        assert len(data) == 4

        assert customer_id_to_delete not in [i['id'] for i in data]



class SaleCRUDTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    # Тест создания продажи
    def test_create_sale(self):
        car = baker.make("carsales.Car")
        customer = baker.make("carsales.Customer")
    
        r = self.client.post("/api/sales/", {
            "car_FK_id": car.id, 
            "customer_FK_id": customer.id, 
            "sale_data": "17.09.2024", 
            "sale_price": "1500000"
        })
        
        new_sale_id = r.json()['id']

        carsales = Sale.objects.all()
        assert len(carsales) == 1

        new_sale = Sale.objects.filter(id=new_sale_id).first()

        assert new_sale.sale_data == '17.09.2024'
        assert new_sale.sale_price == '1500000'
        assert new_sale.car_FK == car
        assert new_sale.customer_FK == customer


    # Тест получения списка продаж
    def test_get_sale(self):
        sale = baker.make("carsales.Sale")
        r = self.client.get('/api/sales/')
        data = r.json()
        
        assert sale.sale_data == data[0]['sale_data']
        assert sale.id == data[0]['id']
        assert sale.sale_price == data[0]['sale_price']
        assert len(data) == 1


    # Тест обновления продаж
    def test_update_sale(self):
        sale = baker.make(Sale)

        r = self.client.get(f"/api/sales/{sale.id}/")
        data = r.json()
        assert data['sale_data'] == sale.sale_data
        assert data['sale_price'] == sale.sale_price

        update_data = {
            "sale_data": "17.09.2024",
            "sale_price": sale.sale_price
        }

        r = self.client.patch(f"/api/sales/{sale.id}/", update_data)

        updated_data = r.json()
        assert updated_data['sale_data'] == "17.09.2024"
        assert updated_data['sale_price'] == sale.sale_price

        sale.refresh_from_db()
        assert sale.sale_data == "17.09.2024"
        assert sale.sale_price == updated_data['sale_price']


    # Тест удаления продажи
    def test_delete_sale(self):
        sale = baker.make("Sale", 5)
        r = self.client.get('/api/sales/')
        data = r.json()
        assert len(data) == 5

        sale_id_to_delete = sale[2].id
        self.client.delete(f'/api/sales/{sale_id_to_delete}/')

        r = self.client.get('/api/sales/')
        data = r.json()
        assert len(data) == 4

        assert sale_id_to_delete not in [i['id'] for i in data]