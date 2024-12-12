#ifndef BANK_ACCOUNT_H
#define BANK_ACCOUNT_H

#include <string>

class __declspec(dllexport) AccountCalculate {
private:
    std::string card_number;
    double amount_money;
    std::string currency;

public:
    AccountCalculate(std::string card_number, double amount_money, std::string currency);
    void addMoney(double amount, double multipler);
    void reduceMoney(double amount);
    bool notEnoughtMoney(double amount) const;
    bool isCardNumberEqual(std::string card_number) const;
    double calculateCurrencyTransfer(std::string sender, std::string recipient) const;
};

extern "C" {
    __declspec(dllexport) AccountCalculate* AccountCalculate_new(const char* card_number, double amount_money, const char* currency);
    __declspec(dllexport) void AccountCalculate_addMoney(AccountCalculate* account, double amount, double multipler);
    __declspec(dllexport) void AccountCalculate_reduceMoney(AccountCalculate* account, double amount);
    __declspec(dllexport) double AccountCalculate_getBalance(AccountCalculate* account);
    __declspec(dllexport) bool AccountCalculate_notEnoughtMoney(AccountCalculate* account, double amount);
    __declspec(dllexport) bool AccountCalculate_isCardNumberEqual(AccountCalculate* account, std::string card_number);
    __declspec(dllexport) double AccountCalculate_calculateCurrencyTransfer(AccountCalculate* account, const char* sender, const char* recipient);
}

#endif // BANK_ACCOUNT_H