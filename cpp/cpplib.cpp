#include <iostream>
#include <string>
#include <vector>

// Структура для конвертації валют
struct CurrencyConversion {
    std::string from_currency;
    std::string to_currency;
    double multiplier;
};

// Список конвертацій валют
std::vector<CurrencyConversion> conversions = {
        {"UAH", "UAH", 1.0},
        {"UAH", "Долар (USD)", 0.027},
        {"UAH", "EUR", 0.025},
        {"USD", "UAH", 37.037},
        {"USD", "USD", 1.0},
        {"USD", "EUR", 0.926},
        {"EUR", "UAH", 40.0},
        {"EUR", "USD", 1.081},
        {"EUR", "EUR", 1.0}
};

// Клас банківського рахунку з методами для керування коштами
class AccountCalculate {
    // Дані
private:
    std::string card_number;
    double amount_money;
    std::string currency;

    // Методи
public:

    // Конструктор
    AccountCalculate(std::string card_number, double amount_money, std::string currency)
        : card_number(card_number), amount_money(amount_money), currency(currency) {
    }

    // Збільшенння грошей
    void addMoney(double amount, double multipler) {
        this->amount_money += amount * multipler;
    }

    // Зменшення грошей
    void reduceMoney(double amount) {
        this->amount_money -= amount;
    }

    // Отримання кількості грошей на рахунку
    double getBalance() {
        return this->amount_money;
    }

    // Перевірка чи достатньо коштів
    bool notEnoughtMoney(double amount) const {
        return this->amount_money < amount;
    }

    // Перевірка, чи збігається номер рахунку з номером іншого рахунку
    bool isCardNumberEqual(std::string card_number) const {
        return this->card_number == card_number;
    }

    // Обчислення множника для конвертації валют
    double calculateCurrencyTransfer(std::string sender, std::string recipient) const {
        double multiplier = 0.0;

        for (const auto& conversion : conversions) {
            if (conversion.from_currency == sender && conversion.to_currency == recipient) {
                multiplier = conversion.multiplier;
                break;
            }
        }

        return multiplier;
    }

};

// Функції для роботи з класом рахунку
extern "C" {
    __declspec(dllexport) AccountCalculate* AccountCalculate_new(const char* card_number, double amount_money, const char* currency) {
        return new AccountCalculate(card_number, amount_money, currency);
    }

    __declspec(dllexport) void AccountCalculate_addMoney(AccountCalculate* account, double amount, double multipler) {
        account->addMoney(amount, multipler);
    }

    __declspec(dllexport) void AccountCalculate_reduceMoney(AccountCalculate* account, double amount) {
        account->reduceMoney(amount);
    }

    __declspec(dllexport) double BankAccount_getBalance(AccountCalculate* account) {
        return account->getBalance();
    }

    __declspec(dllexport) bool BankAccount_notEnoughtMoney(AccountCalculate* account, double amount) {
        return account->notEnoughtMoney(amount);
    }

    __declspec(dllexport) bool BankAccount_isCardNumberEqual(AccountCalculate* account, const char* card_number) {
        return account->isCardNumberEqual(card_number);
    }

    __declspec(dllexport) double BankAccount_calculateCurrencyTransfer(AccountCalculate* account, const char* sender, const char* recipient) {
        return account->calculateCurrencyTransfer(sender, recipient);
    }
}