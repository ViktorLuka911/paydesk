from django.urls import path
from . import views

# Список всіх шляхів застосунку
urlpatterns = [
    
    # Головна сторінка
    path("", views.index, name="index"),
    
    # Сторінка списку
    path('persons/', views.persons, name="persons"),
    
    # Сторінка особи
    path('person/<int:person_id>', views.person, name='person'),
    
    # Сторінка створення особи
    path('add_person/', views.add_person, name='add_person'),
    
    # Сторінка підтвердження видалення особи
    path('delete_person/<int:person_id>', views.delete_person, name="delete_person"),
    
    # Сторінка рахунку
    path('person/<int:person_id>/<int:account_id>/', views.account, name="account"),
    
    # Сторінка списку всіх рахунків
    path('list_accounts', views.list_accounts, name='list_accounts'),
    

    


    # Сторінка підтвердження видалення рахунку
    path('delete_account/<int:person_id>/<int:account_id>', views.delete_account, name="delete_account"),
    
    # Сторінка створення рахунку
    path('add_account/<int:person_id>', views.add_account, name="add_account"),
    
    # Сторінка списку всіх операцій
    path('list_operations', views.list_operations, name='list_operations'),
    
    # Сторінка поповнення рахунку
    path('account_replenishment/<int:account_id>', views.account_replenishment, name='account_replenishment'),
    
    # Сторінка видачі готівки
    path('issuance_cash/<int:account_id>', views.issuance_cash, name='issuance_cash'),
    
    # Сторінка переказу коштів
    path('transfer_funds/<int:account_id>', views.transfer_funds, name='transfer_funds'),
]