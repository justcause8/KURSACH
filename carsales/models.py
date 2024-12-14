from django.db import models

class Dealer(models.Model):
    name = models.TextField("Название дилера")
    headquarters_location  = models.TextField("Местоположение главного офиса")
    picture = models.ImageField("Изображение", null=True, upload_to="dealers")
    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Дилер"
        verbose_name_plural = "Дилеры"

    def __str__(self) -> str:
        return self.name

class DealerCenter(models.Model):
    dealer_FK = models.ForeignKey(Dealer, on_delete=models.CASCADE, null=True, verbose_name="Дилерский центр")
    headquarters_location  = models.TextField("Местоположение центра")
    contact  = models.TextField("Контактная информация")
    manager = models.TextField("Имя управляющего")
    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)


    class Meta:
        verbose_name = "Дилерский центр"
        verbose_name_plural = "Дилерские центры"

    def __str__(self) -> str:
        return self.headquarters_location

class Car(models.Model):
    dealer_center_FK = models.ForeignKey(DealerCenter, on_delete=models.CASCADE, null=True, verbose_name="Дилерский центр")
    dealer_FK = models.ForeignKey(Dealer, on_delete=models.CASCADE, null=True, verbose_name="Дилерский центр")
    car_model = models.TextField("Модель")
    year = models.TextField("Год")
    price = models.TextField("Цена")
    picture = models.ImageField("Изображение", null=True, blank=True)
    image_url = models.URLField("URL изображения", null=True, blank=True)
    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"

    def __str__(self) -> str:
        return self.car_model


class Customer(models.Model):
    car_FK = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, verbose_name="Автомобиль")
    name = models.TextField("ФИО")
    contact_info = models.TextField("Контактная информация")
    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self) -> str:
        return self.name


class Sale(models.Model):
    car_FK = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, verbose_name="Автомобиль")
    customer_FK = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, verbose_name="Клиент")
    sale_data = models.DateField("Дата продажи")
    sale_price = models.TextField("Цена продажи")
    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Продажа"
        verbose_name_plural = "Продажи"
    
    def __str__(self) -> str:
        return str(self.sale_data)