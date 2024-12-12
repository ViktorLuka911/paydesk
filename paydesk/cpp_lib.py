import ctypes

# Завантаження бібліотеки, що містить реалізацію C++ функціоналу
lib = ctypes.CDLL('./cpplib.dll')

# Описуємо структуру BankAccount
class BankAccount(ctypes.Structure):
    _fields_ = [
        ("card_number", ctypes.c_char * 17),
        ("amount_money", ctypes.c_double),
        ("currency", ctypes.c_char * 4),
    ]

# Опис методів, доступних у бібліотеці для роботи з BankAccount
lib.BankAccount_new.argtypes = [ctypes.c_char_p, ctypes.c_double, ctypes.c_char_p]
lib.BankAccount_new.restype = ctypes.POINTER(BankAccount)

lib.BankAccount_addMoney.argtypes = [ctypes.POINTER(BankAccount), ctypes.c_double, ctypes.c_double]
lib.BankAccount_addMoney.restype = None

lib.BankAccount_reduceMoney.argtypes = [ctypes.POINTER(BankAccount), ctypes.c_double]
lib.BankAccount_reduceMoney.restype = None

lib.BankAccount_getBalance.argtypes = [ctypes.POINTER(BankAccount)]
lib.BankAccount_getBalance.restype = ctypes.c_double

lib.BankAccount_notEnoughtMoney.argtypes = [ctypes.POINTER(BankAccount), ctypes.c_double]
lib.BankAccount_notEnoughtMoney.restype = ctypes.c_bool

lib.BankAccount_isCardNumberEqual.argtypes = [ctypes.POINTER(BankAccount), ctypes.c_char_p]
lib.BankAccount_isCardNumberEqual.restype = ctypes.c_bool

lib.BankAccount_calculateCurrencyTransfer.argtypes = [ctypes.POINTER(BankAccount), ctypes.c_char_p, ctypes.c_char_p]
lib.BankAccount_calculateCurrencyTransfer.restype = ctypes.c_double