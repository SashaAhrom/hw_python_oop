import datetime as dt
from typing import Optional

DATE_FORMAT = '%d.%m.%Y'


class Record:
    """Processing of the received data."""
    amount: int
    comment: str
    date: Optional[str]

    def check_date(self) -> None:
        """Check date."""
        if type(self.date) == str:
            try:
                self.date = (dt.datetime.strptime
                             (self.date, DATE_FORMAT).date())
            except ValueError:
                self.date = dt.datetime.now().date()
                print('Введен некорректный формат даты. '
                      f'Установлено date = {self.date}')
        else:
            self.date = dt.datetime.now().date()

    def check_amount(self) -> None:
        """Check amount."""
        if type(self.amount) != int:
            self.amount = 0
            print('Введено некорректное значение калорий(денег). '
                  'Установлено amount = 0')

    def __init__(self, amount: int, comment: str,
                 date: Optional[str] = None) -> None:
        self.amount = amount
        self.comment = comment
        self.date = date
        self.check_date()
        self.check_amount()


class Calculator:
    """Add data and sum it."""
    limit: int

    def check_limit(self) -> None:
        """Check limit."""
        if type(self.limit) != (int or float) or self.limit < 0:
            self.limit = 0
            print('Введено некорректное значение лимита. '
                  'Установлено limit = 0')
        else:
            self.limit = int(self.limit)

    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.records = []
        self.check_limit()

    def add_record(self, record) -> None:
        """Add date to the list."""
        self.records.append(record)

    def get_today_stats(self) -> int:
        """Sum per day."""
        day_naw = dt.datetime.now().date()
        return sum([i.amount for i in self.records if i.date == day_naw])

    def get_limit_dotay(self) -> int:
        """Calculate the daily limit."""
        return self.limit - self.get_today_stats()

    def get_week_stats(self) -> int:
        """Sum per week."""
        seven_days = dt.timedelta(days=7)
        day_naw = dt.datetime.now().date()
        last_week = day_naw - seven_days
        return sum([i.amount for i in self.records
                    if i.date >= last_week and i.date <= day_naw])


class CaloriesCalculator(Calculator):
    """Total daily calories consumption."""
    TODAY_CALORIES = ('Сегодня можно съесть что-нибудь ещё, '
                      'но с общей калорийностью не более '
                      '{balance} кКал')

    def get_calories_remained(self) -> str:
        """Returns information about consumed colories for the day."""
        if self.get_limit_dotay() > 0:
            return self.TODAY_CALORIES.format(balance=self.get_limit_dotay())
        return 'Хватит есть!'


class CashCalculator(Calculator):
    """Daily spending calculator with currency selection."""
    POSITIVE_BALANCE = 'На сегодня осталось {balance} {currency}'
    NEGATIVE_BALANCE = 'Денег нет, держись: твой долг - {balance} {currency}'
    USD_RATE = 60.0                             # Чтобы пройти тестирование
    EURO_RATE = 70.0                            # Чтобы пройти тестирование
    currencies = {'usd': ('USD', USD_RATE),
                  'eur': ('Euro', EURO_RATE),
                  'rub': ('руб', 1)}

    def check_currency(self):
        """Check currency."""
        if self.currency not in self.currencies:
            self.currency = 'rub'
            print('Валюта задана некорректна. Утановлена валюта руб')

    def get_today_cash_remained(self, currency: str) -> str:
        """Information about daily spending."""
        if self.get_limit_dotay() == 0:
            return 'Денег нет, держись'
        else:
            self.currency = currency.lower()
            self.check_currency()
            name_currency, rate = self.currencies[self.currency]
            waste_currency = self.get_limit_dotay() / rate
            return (self.POSITIVE_BALANCE if waste_currency > 0
                    else self.NEGATIVE_BALANCE).format(balance=round(abs(
                        waste_currency), 2), currency=name_currency)
