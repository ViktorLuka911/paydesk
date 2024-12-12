#include <iostream>
#include <string>
#include <vector>

// ��������� ��� ����������� �����
struct CurrencyConversion {
    std::string from_currency;
    std::string to_currency;
    double multiplier;
};

// ������ ����������� �����
std::vector<CurrencyConversion> conversions = {
        {"UAH", "UAH", 1.0},
        {"UAH", "����� (USD)", 0.027},
        {"UAH", "EUR", 0.025},
        {"USD", "UAH", 37.037},
        {"USD", "USD", 1.0},
        {"USD", "EUR", 0.926},
        {"EUR", "UAH", 40.0},
        {"EUR", "USD", 1.081},
        {"EUR", "EUR", 1.0}
};

// ���� ����������� ������� � �������� ��� ��������� �������
class AccountCalculate {
    // ���
private:
    std::string card_number;
    double amount_money;
    std::string currency;

    // ������
public:

    // �����������
    AccountCalculate(std::string card_number, double amount_money, std::string currency)
        : card_number(card_number), amount_money(amount_money), currency(currency) {
    }

    // ���������� ������
    void addMoney(double amount, double multipler) {
        this->amount_money += amount * multipler;
    }

    // ��������� ������
    void reduceMoney(double amount) {
        this->amount_money -= amount;
    }

    // ��������� ������� ������ �� �������
    double getBalance() {
        return this->amount_money;
    }

    // �������� �� ��������� �����
    bool notEnoughtMoney(double amount) const {
        return this->amount_money < amount;
    }

    // ��������, �� �������� ����� ������� � ������� ������ �������
    bool isCardNumberEqual(std::string card_number) const {
        return this->card_number == card_number;
    }

    // ���������� �������� ��� ����������� �����
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

// ������� ��� ������ � ������ �������
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