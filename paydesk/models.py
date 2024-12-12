from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Типи валюти
CURRENCY_CHOICES = [
    ('USD', 'Долар США'),
    ('EUR', 'Євро'),
    ('UAH', 'Гривня')
]

# Клас особи операції
class PersonOperation(models.Model):
    name          = models.CharField(max_length=192)
    card_number   = models.CharField(max_length=16)
    card_currency = models.CharField(choices=CURRENCY_CHOICES, max_length=64)

# Клас операції
class Operation(models.Model):
    name      = models.CharField(max_length=20)
    date      = models.DateTimeField()
    sender    = models.ForeignKey(PersonOperation, on_delete=models.CASCADE, related_name='sended_operations')
    recipient = models.ForeignKey(PersonOperation, on_delete=models.CASCADE, related_name='received_operations', null=True, blank=True)
    amount    = models.FloatField()

# Клас банківського рахунку
class Account(models.Model):
    card_number  = models.CharField(max_length=16)
    pin          = models.CharField(max_length=4)
    cvv          = models.CharField(max_length=3)
    currency     = models.CharField(choices=CURRENCY_CHOICES, max_length=64)
    amount_money = models.FloatField(default=0)
    operations   = models.ForeignKey(Operation, on_delete=models.CASCADE, blank=True, null=True)
    
class Person(models.Model):
    itn          = models.CharField(max_length=10)
    first_name   = models.CharField(max_length=64)
    last_name    = models.CharField(max_length=64)
    age          = models.IntegerField(validators=[MinValueValidator(14), MaxValueValidator(122)])
    phone_number = models.CharField(max_length=14)
    accounts = models.ManyToManyField('Account', related_name='persons', blank=True)
    
    # Метод для отримання повного ім'я особи
    def person_fullname(self):
        return f"{self.first_name} {self.last_name}"
    
     # Метод для видалення рахунків при видаленні особи
    def delete_accounts(self):
        self.accounts.all().delete()

    # Переопределення методу видалення
    def delete(self, *args, **kwargs):
        self.delete_accounts()  # Видалити всі рахунки перед видаленням особи
        super().delete(*args, **kwargs)  # Викликати стандартну логіку видалення