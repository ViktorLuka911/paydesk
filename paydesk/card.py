from django.utils.timezone import now
from .models import Operation, PersonOperation, Account, Person
from .cpp_lib import lib

class Card:
    # Ініціалізація класу, що відповідає за операції з банківським рахунком
    def __init__(self, account, person):
        self.account = account
        self.person = person
        
        # Використання C++ бібліотеки для створення об'єкта банківського рахунку
        self.account_сalculate = lib.BankAccount_new(
            self.account.card_number.encode('utf-8'),
            self.account.amount_money,
            self.account.currency.encode('utf-8')
        )
        
    # Метод для отримання даних відправника
    def get_sender(self):
        sender, _ = PersonOperation.objects.get_or_create(
            name=self.person.person_fullname(),
            card_number=self.account.card_number,
            card_currency=self.account.currency
        )
        return sender
    
    # Метод для створення операції
    def create_operation(self, name, amount, recipient=None):
        Operation.objects.create(
            name=name,
            date=now(),
            sender=self.get_sender(),
            recipient=recipient,
            amount=amount,
        )

    # Метод для поповнення рахунку
    def replenish_account(self, amount):
        # Додавання коштів до рахунку через C++ бібліотеку
        lib.BankAccount_addMoney(self.account_сalculate, amount, 1.0)
        
        # Оновлення балансу рахунку після операції
        self.account.amount_money = lib.BankAccount_getBalance(self.account_сalculate)
    
        self.account.save()
        self.create_operation("Поповнення рахунку", amount)
        
    # Метод для видачі готівки
    def issuance_cash(self, amount):
        if lib.BankAccount_notEnoughtMoney(self.account_сalculate, amount):
            raise ValueError("Недостатньо коштів на рахунку для виконання операції")

        # Списання коштів з рахунку через метод бібліотеки
        lib.BankAccount_reduceMoney(self.account_сalculate, amount)
        self.account.amount_money = lib.BankAccount_getBalance(self.account_сalculate)

        self.account.save()
        self.create_operation("Видача готівки", amount)

    # Метод для переказу коштів на іншу картку
    def transfer_funds(self, amount, recipient_card):
        recipient_card_num = (recipient_card).encode('utf-8')
        if lib.BankAccount_notEnoughtMoney(self.account_сalculate, amount):
            raise ValueError("Недостатньо коштів на рахунку для виконання операції")

        try:
            recipient_account = Account.objects.get(card_number=recipient_card)
        except Account.DoesNotExist:
            raise ValueError("Картка отримувача не знайдена")

        if lib.BankAccount_isCardNumberEqual(self.account_сalculate, recipient_card_num):
            raise ValueError("Картки відправника та отримувача не можуть бути однаковими")

        # Ініціалізація об'єкта рахунку отримувача через C++ бібліотеку
        recipient_acc = lib.BankAccount_new(
            self.account.card_number.encode('utf-8'),
            recipient_account.amount_money,
            recipient_account.currency.encode('utf-8')
        )

        recipient_person = Person.objects.get(accounts=recipient_account)

        # Створення або отримання об'єкта PersonOperation для отримувача
        recipient, _ = PersonOperation.objects.get_or_create(
            name=recipient_person.person_fullname(),
            card_number=recipient_card,
            card_currency=recipient_account.currency
        )

        # Списання коштів із рахунку відправника
        lib.BankAccount_reduceMoney(self.account_сalculate, amount)
        self.account.amount_money = lib.BankAccount_getBalance(self.account_сalculate)
        self.account.save()
        
        # Розрахунок коефіцієнта для конвертації валют
        currency_multipler = lib.BankAccount_calculateCurrencyTransfer(self.account_сalculate, self.account.currency.encode('utf-8'), recipient_account.currency.encode('utf-8'))

        # Поповнення рахунку отримувача
        lib.BankAccount_addMoney(recipient_acc, amount, currency_multipler)
        recipient_account.amount_money = lib.BankAccount_getBalance(recipient_acc)
        recipient_account.save()

        self.create_operation("Переказ коштів", amount, recipient)