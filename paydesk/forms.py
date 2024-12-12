from django import forms
from .models import Person, Account, Operation

# Типи осіб
PERSON_CHOICES = [
    ('Фізична особа', 'Фізична особа'),
    ('Юридична особа', 'Юридична особа')
]

# Типи валюти
CURRENCY_CHOICES = [
    ('USD', 'Долар США'),
    ('EUR', 'Євро'),
    ('UAH', 'Гривня')
]

# Типи статей
GENDER_CHOICES = [
    ('Чоловік', 'Чоловік'),
    ('Жінка', "Жінка")
]

PAYMENT_SOURCE_CHOICES = [
    ('Кредитні кошти', 'Кредитні кошти'),
    ('Власні кошти', 'Власні кошти')
]

# Клас форми для створення особи
class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['itn', 'first_name', 'last_name', 'age', 'phone_number']

# Клас форми для пошуку особи
class PersonSearchForm(forms.ModelForm):
    class Meta:
        model   = Person
        fields  = ['first_name', 'last_name']
        widgets = {
            'first_name' : forms.TextInput(attrs={'placeholder': 'Введіть ім’я'}),
            'last_name'  : forms.TextInput(attrs={'placeholder': 'Введіть прізвище'}),
        }

# Клас форми для пошуку рахунку
class AccountSearchForm(forms.ModelForm):
    class Meta:
        model   = Account
        fields  = ['card_number']
        widgets = {
            'card_number': forms.TextInput(attrs={'placeholder': 'Введіть номер карти'})
        }

# Клас форми для створення рахунку
class AccountForm(forms.ModelForm):
    class Meta:
        model   = Account
        fields  = ['card_number', 'pin', 'cvv', 'currency']
        widgets = {
            'currency' : forms.Select(choices=CURRENCY_CHOICES),
        }


# Клас форми для проведення операціії
class OperationForm(forms.ModelForm):
    class Meta:
        model = Operation
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput()
        }

# Клас форми для переказу коштів без вибору джерела коштів
class TransferForm(forms.ModelForm):
    card_number = forms.CharField(max_length=16)
    
    class Meta:
        model = Operation
        fields = ['amount', 'card_number']
        widgets = {
            'amount': forms.NumberInput(),
            'card_number': forms.TextInput()
        }