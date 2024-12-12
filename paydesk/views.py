from django.shortcuts import render, get_object_or_404, redirect
from .forms import PersonForm, PersonSearchForm, AccountSearchForm, AccountForm, OperationForm, TransferForm
from .models import Account, Person, Operation
from .card import Card
# Функція для завантаження головної сторінки
def index(request):
    return render(request, 'main/main_menu.html')

# Функція для завантаження сторінки списку осіб
def persons(request):
    form = PersonSearchForm(request.GET or None)  # Ініціалізація форми пошуку
    queryset = Person.objects.all()  # Отримуємо всі записи моделі `Person`
    
    # Перевіряємо валідність форми і застосовуємо фільтри
    if form.is_valid():
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')

        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)

    # Рендеримо шаблон і передаємо відфільтровані дані та форму
    return render(request, 'data/person/persons.html', {
        'persons': queryset,
        'form': form,
    })

# Функція для завантаження сторінки особи
def person(request, person_id):
    # Отримання необхідних даних
    person = get_object_or_404(Person, id=person_id)
    accounts = Account.objects.filter(persons=person)
    form = AccountSearchForm(request.GET or None)
    
    # Використання даних форми для фільтрації рахунків
    if form.is_valid():
        card_number = form.cleaned_data.get('card_number', '').strip()
        if card_number:
            accounts = accounts.filter(card_number__icontains=card_number)

    # Завантаження сторінки списку рахунків для особи
    return render(request, 'data/person/person.html', {
        'person': person,
        'accounts': accounts,
        'form': form,
    })

# Функція для завантаження сторінки створення чи редагування особи
def add_person(request):
    if request.method == "POST":
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()  # Зберігаємо нову особу в базі даних
            return redirect('persons')  # Перенаправляємо на список усіх осіб
    else:
        form = PersonForm()  # Порожня форма для введення даних

    # Завантаження сторінки створення нової особи
    return render(request, 'data/person/add_person.html', {'form': form,})


# Функція для завантаження сторінки списку всіх рахунків
def list_accounts(request):
    form = AccountSearchForm(request.GET or None)
    
    # Отримуємо всі рахунки
    accounts = Account.objects.all()

    # Фільтруємо рахунки за критеріями
    if form.is_valid():
        card_number = form.cleaned_data.get('card_number')

        if card_number:
            accounts = accounts.filter(card_number__icontains=card_number)

    account_data_list = []
    for account in accounts:
        account_data = {
            'account': account,
        }

        # Отримуємо єдину особу, пов'язану з рахунком
        try:
            person = account.persons.get()  # Використовуємо get() для однозначного доступу
            account_data['person'] = person
        except Person.DoesNotExist:
            pass  # Якщо особи немає, просто пропускаємо

        account_data_list.append(account_data)

    return render(request, 'data/account/list_accounts.html', {
        'form': form,
        'account_data_list': account_data_list,
    })

# Функція для завантаження сторінки із списком всіх операцій
def list_operations(request):
    operations = Operation.objects.all().order_by('-date')
    return render(request, 'operations/list_operations.html', {'operations': operations})

# Функція для видалення особи
def delete_person(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    person.delete()
    
    # Список осіб після видалення
    persons = Person.objects.all()

    # Завантаження сторінки списку осіб
    return render(request, 'data/person/persons.html', {'persons': persons,})

# Функція для завантаження сторінки рахунку
def account(request, person_id, account_id):
    # Отримання об'єкта особи за ID
    person = get_object_or_404(Person, id=person_id)
    
    # Отримання об'єкта рахунку, прив'язаного до цієї особи
    account = get_object_or_404(Account, id=account_id, persons=person)
    
    # Отримання операцій, пов'язаних з рахунком
    operations = Operation.objects.filter(sender__card_number=account.card_number) | Operation.objects.filter(recipient__card_number=account.card_number)

    # Завантаження сторінки рахунку
    return render(request, 'data/account/account.html', {
        'person': person,
        'account': account,
        'operations': operations,
    })
    
# Функція для підтвердження видалення рахунку
def delete_account(request, person_id, account_id):
    # Отримання об'єкта особи за ID
    person = get_object_or_404(Person, id=person_id)
    
    # Отримання рахунку, прив'язаного до цієї особи
    account = get_object_or_404(Account, id=account_id, persons=person)
    
    # Видалення рахунку
    account.delete()
    
    accounts = Account.objects.filter(persons=person)
    # Завантаження сторінки особи
    return render(request, 'data/person/person.html', {
        'person': person,
        'accounts': accounts,
    })

# Функція для створення нового рахунку
def add_account(request, person_id):
    # Отримання особи за її ID
    person = get_object_or_404(Person, id=person_id)

    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            # Створення нового банківського рахунку
            account = form.save(commit=False)
            account.amount_money = 0  # Новий рахунок починається з нульовим балансом
            account.save()
            person.accounts.add(account)

            person.save()

            # Перенаправлення на сторінку особи після створення рахунку
            return redirect('person', person_id=person.id)
    form = AccountForm()  # Порожня форма для створення рахунку

    # Рендеринг сторінки створення нового рахунку
    return render(request, 'data/account/add_account.html', {
        'form': form,
        'person': person,
    })

# Функція для завантаження сторінки із видачею готівки
def issuance_cash(request, account_id):
    # Отримання необхідних даних
    account = get_object_or_404(Account, id=account_id)

    # Визначення типу особи на основі account
    person = get_object_or_404(Person, accounts=account)
    
    # Створення картки для операцій
    card = Card(account, person)
    
    # Завантаження на даних та сторінки на основі даних форми і типу рахунку
    if request.method == 'POST':
        form = OperationForm(request.POST)
            
        if form.is_valid():
            try:
                operation_data = form.cleaned_data
                amount = operation_data['amount']
                
                # Виконання операції видачі готівки
                card.issuance_cash(amount)

                # Повернення результату з успішним повідомленням
                return render(
                    request,
                    'operations/issuance_cash.html', {
                        'account': account,
                        'person': person,
                        'form': form,
                        'message': 'Готівку успішно видано!',
                    })
            except ValueError as e:
                # Обробка помилок, якщо не вдалося видати готівку
                return render(
                    request,
                    'operations/issuance_cash.html', {
                        'account': account,
                        'person': person,
                        'form': form,
                        'message': f'Помилка: {str(e)}',
                    })
    else:
        form = OperationForm()

    # Рендеринг сторінки
    return render(
        request,
        'operations/issuance_cash.html', {
            'account': account,
            'person': person,
            'form': form,
        })

# Функція для завантаження сторінки із поповненням рахунку
def account_replenishment(request, account_id):
    # Отримання необхідних даних
    account = get_object_or_404(Account, id=account_id)

    # Визначення типу особи на основі account
    person = get_object_or_404(Person, accounts=account)
    
    # Створення картки для операцій
    card = Card(account, person)

    # Завантаження на даних та сторінки на основі даних форми і типу рахунку 
    if request.method == 'POST':
        form = OperationForm(request.POST)
        if form.is_valid():
            try:
                operation_data = form.cleaned_data
                amount = operation_data['amount']
                card.replenish_account(amount)
            
                return render(
                    request,
                    'operations/account_replenishment.html',
                    {
                        'account': account,
                        'person': person,
                        'form': form,
                        'message': 'Рахунок успішно поповнено!',
                    }
                )
            except ValueError as e:
                return render(
                    request,
                    'operations/account_replenishment.html', {
                        'account': account,
                        'person': person,
                        'form': form,
                        'message': str(e),
                    })
    else:
        form = OperationForm()
    return render(
        request,
        'operations/account_replenishment.html', {
            'account': account,
            'person': person,
            'form': form,
        })

# Функція для завантаження сторінки із переказом коштів
def transfer_funds(request, account_id):
    # Отримання необхідних даних
    account = get_object_or_404(Account, id=account_id)

    # Визначення типу особи на основі account
    person = get_object_or_404(Person, accounts=account)
    
    # Створення картки для операцій
    card = Card(account, person)

    # Завантаження на даних та сторінки на основі даних форми та типу рахунку
    if request.method == 'POST':
        form = TransferForm(request.POST)

        if form.is_valid():
            try:
                data = form.cleaned_data
                amount = data['amount']
                recipient_card_number = data['card_number']
                
                card.transfer_funds(amount, recipient_card_number)
                    
                return render(
                    request,
                    'operations/transfer_funds.html',
                    {
                        'form': form,
                        'account': account,
                        'person': person,
                        'message': 'Транзакцію успішно проведено!',
                    }
                )
            except ValueError as e:
                return render(
                    request,
                    'operations/transfer_funds.html',{
                        'form': form,
                        'account': account,
                        'person': person,
                        'message': str(e),
                    })
    else:
        form = TransferForm()
    return render(request, 'operations/transfer_funds.html', {
            'form': form,
            'account': account,
            'person': person,
    })