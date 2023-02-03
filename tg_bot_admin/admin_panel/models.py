from django.db import models

class TgUser(models.Model):
    telegram_id = models.IntegerField(verbose_name='Телеграм id')
    user_name = models.CharField(max_length=150, verbose_name='Имя пользователя')
    user_phone_number = models.CharField(max_length=13, verbose_name='Номер телефона')
    user_service = models.CharField(max_length=75, verbose_name='Услуга')

    def __str__(self):
        return self.user_phone_number
class Services(models.Model):
    service_name = models.CharField(max_length=75)
    service_added_name = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.service_name

class TgOrders(models.Model):
    telegram_id = models.ForeignKey(TgUser, on_delete=models.CASCADE)
    user_service = models.ForeignKey(Services, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.telegram_id)

